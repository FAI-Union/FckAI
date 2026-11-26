# FAI 仓库安全复查报告

日期：2026-11-26
范围：`D:/Git/FAI` 全仓库（工作区 + 全部 git 历史）
性质：在 `5b68ff4`（安全加固）与 `b2efc94`（文档收尾）之后的独立复核，重点是**验证上轮修复是否真的生效**，并寻找遗漏项。

---

## 1. 结论摘要

| 项 | 结果 |
|---|---|
| 远程 RCE / SQL 注入 / 命令注入 | 未发现 |
| 凭据入库（工作区 + 全历史） | 0 命中 |
| 上轮 15 项修复有效性 | 14 项动态或静态确认；1 项因 Windows 权限仅静态确认（符号链接） |
| 本轮新发现 | 4 项（MCP 协议崩溃 ×1、RSS DTD 检查偏移绕过 ×1、CI 链接农场绕过 ×1、MCP 字符串无上限 ×1） |
| 本轮处置 | 4 项全部修复并加入回归测试 |
| 测试 | `py_compile` 通过；`unittest` **18/18** 通过 |

**总体判断**：仓库当前无高危可利用漏洞。上一轮修复方向正确且基本到位；本轮补齐了 4 个纵深防御缺口。

---

## 2. 上轮修复复核（逐项）

| ID | 上轮问题 | 复核方式 | 结果 |
|---|---|---|---|
| G-1 | `ai-tools/` 未纳入版本控制 | `git ls-files ai-tools` | 已跟踪，18 个文件随 `5b68ff4` 入库 |
| M-1 | RSS 内容注入公开 Discussion | PoC：Markdown 链接/图片/script/@ 提醒/换行 | 全部被渲染为 inline code；URL 白名单拒绝 `javascript:`/`data:`/协议相对/含 `<>"'` |
| M-2 | PAT 明文与脱敏不全 | `icacls` + 环境变量 PoC | ACL 仅当前用户 + SYSTEM + Administrators；`redact` 同时覆盖 token 正则与实时环境变量值 |
| M-3 | 草稿 frontmatter 注入 | PoC：`tags` 换行、`id` 换行、`publisher` 换行、逗号/方括号、重复 `## Source` | 除重复章节被前缀 `- ` 中和外，其余全部拒绝；解析后 `status` 仍为 `verified`、来源 URL 未被覆盖 |
| M-4 | 符号链接/越界读取 | PoC：`..` 与绝对路径 | 均抛出 `path escapes the repository root`；`validate_links` 能报告越界链接。Windows 无法创建符号链接，该分支仅静态确认 |
| M-5 | `pull_request_target` + 可变 tag | `ls-remote` + workflow 审阅 | SHA `f28e40c7f34bde8b3046d885e986cb6290c5673b` 与 v7 一致；无 checkout；权限按 job 拆分 |
| P2 | RSS 大小/实体、MCP 参数、install 原子写、URL 农场、日志尾部、去重重长尾 | 代码审阅 + PoC | 除下述 3 项遗留外均到位；去重已扩至最多 2000 条 Discussion |

---

## 3. 本轮新发现与修复

### N-1（低危，已修复）：畸形 MCP 消息导致服务进程退出

- **复现**：
  - `{"method":"tools/call","params":{"name":[]}}` → `TypeError: unhashable type: 'list'`，退出码 1
  - `{"method":"initialize","params":[1]}` → `AttributeError`，退出码 1
  - `{"method":"tools/call","params":[1]}` → `AttributeError`，退出码 1
- **影响**：本地 stdio 客户端发送畸形 JSON-RPC 即可让 MCP server 崩溃（DoS），不影响数据机密性。
- **修复**：`mcp_server.py` 在分派前校验 `params` 必须为对象、`name` 必须为字符串，统一返回 `-32602`。
- **复测**：上述三类消息均返回 JSON-RPC error，退出码 0，stderr 为空。

### N-2（低危，已修复）：RSS DTD/实体检查只覆盖前 8192 字节

- **复现**：构造 9000 字节填充后再放 `<!DOCTYPE>`，原检查不命中。
- **影响**：不可信 RSS 可在偏移位置声明实体；Python ElementTree 不解析外部实体，但内部实体展开仍可能造成资源消耗。
- **修复**：`has_dtd()` 对完整（已限制 ≤5 MiB）响应做检查并用于 `fetch_rss`。
- **复测**：偏移 9000 字节的实体声明现被检出；新增单元测试。

### N-3（低危，已修复）：CI 链接农场检查可因 patch 缺失被绕过

- **复现路径**：GitHub REST 对超大 diff 会省略/截断 `patch`；旧逻辑仅对 *新增* Markdown 读完整 blob，对 *修改* 的 Markdown 只 warning，因此向已有大文件塞入大量链接可绕过 `urlCount > 12` 检查。
- **修复**：`content-validation.yml` 改为对全部新增/修改 Markdown 读取 head 与 base 完整 blob，按 URL 总数差值计算新增链接；blob 不可读时 **fail closed**。
- **复测**：Node harness 模拟 `patch: null`、head 含 13 个链接、base 无链接 → 正确失败：`Too many new links (13)`。5 段 workflow 内嵌 JS 语法校验通过。

### N-4（信息级，已修复）：MCP 字符串/数组参数无长度上限

- **问题**：`limit/tail/per_run/timeout` 已有边界，但 `query`、`text`、`excerpt`、`changed_files` 等无上限，超大 payload 可造成内存与响应膨胀。
- **修复**：`_validate_args` 增加字符串 100,000 字符上限、数组 1000 元素上限（远大于正常证据卡需求）。
- **复测**：100,001 字符 `query` 被干净拒绝，服务不崩溃。

---

## 4. 残余风险与加固建议（未修改）

| 级别 | 项 | 说明 |
|---|---|---|
| 低 | Windows 符号链接分支未动态验证 | 本机无创建符号链接权限；`_is_symlink_path` 逻辑已静态审阅，路径逃逸部分已动态验证。建议在有权限的环境补一条 symlink 回归。 |
| 低 | `install.py` 未校验 skills 目标目录是否为符号链接 | `.workbuddy/skills` 由本地用户控制，非远程攻击面；若担心可加目标边界校验。 |
| 低 | `track_search_rank.py` 的 `json.load(response)` 无响应体上限 | 目标固定为 GitHub Search API，风险可接受。 |
| 低 | `safe_link` 允许 `http` | 仅用于第三方新闻链接的展示，非凭据或跳转端点；如需更严格可改为 https-only。 |
| 低 | `redact` 只覆盖已知环境变量名与常见 token 模式 | 自定义名称的 secret 环境变量不会被自动脱敏。 |
| 信息 | `main` 领先 `origin/main`，尚未推送 | 安全修复目前只在本地；需推送后才对远端/CI 生效。 |

---

## 5. 验证证据

- `python -m py_compile`（6 个 Python 文件）：通过。
- `python -m unittest discover -s ai-tools/tests -v`：**18/18 OK**。
- 凭据模式（GitHub PAT、gh token、AWS、Google API、Slack、私钥、JWT）扫描：工作区 0 命中，全部 git 历史 0 命中。
- `actions/github-script` 固定 SHA 与 `v7` 标签一致。
- `git diff --check`：通过。
- 工作流内嵌 JS 语法：5/5 通过。
- 新闻机器人 `dry-run`：正常，无 ACL 告警。

---

## 6. 后续动作

1. 将本轮 4 项修复与本报告提交。
2. 推送 `main` 到远端，使 CI 修复生效。
3. MCP server 已重新安装过；本次 `mcp_server.py` 的变更需**重启 WorkBuddy** 才会被客户端加载。
