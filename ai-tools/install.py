#!/usr/bin/env python3
"""Install the FAI MCP server and project-level WorkBuddy skills locally.

The canonical sources live in the tracked ai-tools/ directory. This script only
writes local configuration and a copy of SKILL.md files into the gitignored
.workbuddy/skills/ directory; it never touches tracked content or secrets.

  python ai-tools/install.py
  python ai-tools/install.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MCP_NAME = "fai"


def default_mcp_config() -> Path:
    return Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".workbuddy" / "mcp.json"


def default_skills_dir() -> Path:
    return REPO / ".workbuddy" / "skills"


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise SystemExit(f"cannot parse existing MCP config {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"MCP config {path} must be a JSON object")
    return data


def install(mcp_config: Path, skills_dir: Path, dry_run: bool = False) -> dict[str, object]:
    config = load_config(mcp_config)
    servers = config.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise SystemExit("mcpServers must be a JSON object")
    entry = {
        "command": sys.executable,
        "args": [str(HERE / "mcp_server.py").replace("\\", "/")],
        "env": {"FAI_REPO_ROOT": str(REPO).replace("\\", "/")},
    }
    changed_mcp = servers.get(MCP_NAME) != entry
    if changed_mcp and not dry_run:
        servers[MCP_NAME] = entry
        mcp_config.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(config, ensure_ascii=False, indent=2) + "\n"
        tmp = mcp_config.with_name(mcp_config.name + ".tmp")
        tmp.write_text(payload, encoding="utf-8")
        if mcp_config.exists():
            os.chmod(tmp, stat.S_IMODE(mcp_config.stat().st_mode))
        tmp.replace(mcp_config)

    installed: list[str] = []
    for skill_dir in sorted((HERE / "skills").iterdir()):
        source = skill_dir / "SKILL.md"
        if not source.is_file():
            continue
        target_dir = skills_dir / skill_dir.name
        target = target_dir / "SKILL.md"
        already_same = target.is_file() and target.read_bytes() == source.read_bytes()
        installed.append(skill_dir.name + (" (unchanged)" if already_same else ""))
        if not dry_run and not already_same:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    return {
        "mcp_config": str(mcp_config),
        "mcp_entry": MCP_NAME,
        "mcp_changed": changed_mcp,
        "skills_dir": str(skills_dir),
        "skills": installed,
        "dry_run": dry_run,
        "note": "Restart WorkBuddy to load a newly registered MCP server.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mcp-config", type=Path, default=default_mcp_config())
    parser.add_argument("--skills-dir", type=Path, default=default_skills_dir())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    result = install(args.mcp_config.resolve(), args.skills_dir.resolve(), args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
