#!/usr/bin/env python3
"""FAI MCP server (stdio, JSON-RPC 2.0, standard library only).

Register in ~/.workbuddy/mcp.json as:
  {"mcpServers": {"fai": {"command": "python", "args": ["D:/Git/FAI/ai-tools/mcp_server.py"]}}}

All tools are read-only or generate drafts in memory. No tool writes tracked files,
and no tool prints secrets. Set FAI_REPO_ROOT to point at another checkout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import core as fai  # noqa: E402

SERVER_INFO = {"name": "fai", "version": "1.0.0"}


def _obj(props: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "object", "properties": props}
    if required:
        schema["required"] = required
    return schema


S = {"type": "string"}
B = {"type": "boolean"}
I = {"type": "integer"}
SA = {"type": "array", "items": S}

TOOLS: list[dict[str, Any]] = [
    {
        "name": "repo_overview",
        "description": "Get the FAI repo mission, canonical docs, data dirs, content counts and human-gated actions. Start here when unsure where content lives.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.repo_overview(),
    },
    {
        "name": "repo_status",
        "description": "Inspect branch, last commit, working-tree cleanliness, content counts and RUNBOOK pending-item counts.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.repo_status(),
    },
    {
        "name": "search_repo",
        "description": "Case-insensitive full-text search over tracked text files. Returns file:line snippets; redacts any token-looking strings.",
        "inputSchema": _obj(
            {
                "query": S,
                "path_filter": {**S, "description": "Optional substring of the relative path, e.g. RESEARCH/"},
                "limit": I,
            },
            ["query"],
        ),
        "handler": lambda a: fai.search_repo(a.get("query", ""), a.get("path_filter"), int(a.get("limit", 50))),
    },
    {
        "name": "list_evidence",
        "description": "List evidence cards with ID, bilingual title, status, tags and source URL. Filter by tag or free-text query.",
        "inputSchema": _obj({"tag": S, "query": S}),
        "handler": lambda a: fai.list_evidence(a.get("tag"), a.get("query")),
    },
    {
        "name": "get_evidence",
        "description": "Read one evidence card in full, including frontmatter, all sections and the verbatim excerpt.",
        "inputSchema": _obj({"evidence_id": S}, ["evidence_id"]),
        "handler": lambda a: fai.get_evidence(a["evidence_id"]),
    },
    {
        "name": "validate_evidence",
        "description": "Check a card (by ID) or a draft (raw text) against the FAI schema: ID, frontmatter, bilingual claim, source URL, quote, caveats, index row and ID uniqueness.",
        "inputSchema": _obj({"evidence_id": S, "text": S}),
        "handler": lambda a: fai.validate_evidence(a.get("evidence_id"), a.get("text")),
    },
    {
        "name": "next_evidence_id",
        "description": "Return the next unused EV-YYYY-NNN ID based on existing cards and the research index.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.next_evidence_id(),
    },
    {
        "name": "scaffold_evidence",
        "description": "Generate a schema-valid evidence-card draft in memory (never writes files). Supply the claim in English and Chinese plus an original source URL and a verbatim quote.",
        "inputSchema": _obj(
            {
                "claim_en": S,
                "claim_zh": S,
                "source_url": S,
                "publisher": S,
                "excerpt": S,
                "caveats": S,
                "tags": SA,
                "evidence_id": S,
                "verified_by": S,
                "publication_date": S,
                "report": S,
            },
            ["claim_en", "claim_zh", "source_url", "publisher", "excerpt", "caveats"],
        ),
        "handler": lambda a: fai.scaffold_evidence(
            claim_en=a.get("claim_en", ""),
            claim_zh=a.get("claim_zh", ""),
            source_url=a.get("source_url", ""),
            publisher=a.get("publisher", ""),
            excerpt=a.get("excerpt", ""),
            caveats=a.get("caveats", ""),
            tags=a.get("tags"),
            evidence_id=a.get("evidence_id"),
            verified_by=a.get("verified_by", "web-research-agent"),
            publication_date=a.get("publication_date", ""),
            report=a.get("report", ""),
        ),
    },
    {
        "name": "check_evidence_chain",
        "description": "Verify the EV -> POLICY/CAMPAIGNS chain: dangling EV references and cards whose Used by section lacks a backlink.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.check_evidence_chain(),
    },
    {
        "name": "validate_links",
        "description": "Lint all relative Markdown links across tracked files and report broken targets with file and line number.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.validate_links(),
    },
    {
        "name": "translation_status",
        "description": "Summarise LANGUAGES.md rows, locale directories, priority languages not started, and claimed languages missing a directory.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.translation_status(),
    },
    {
        "name": "validate_translation",
        "description": "Check a translation contribution: BCP 47 tag, i18n(<tag>) PR title, LANGUAGES.md update and the four core translated documents with links to the English originals.",
        "inputSchema": _obj(
            {"tag": S, "title": S, "changed_files": SA}, ["tag"]
        ),
        "handler": lambda a: fai.validate_translation(a["tag"], a.get("title"), a.get("changed_files")),
    },
    {
        "name": "runbook_backlog",
        "description": "Extract all pending/in-progress items from RUNBOOK.md with their section and status symbol.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.runbook_backlog(),
    },
    {
        "name": "rank_snapshot",
        "description": "Combine the search baseline and rank-*.md reports into a before/after table. Offline only; does not query GitHub.",
        "inputSchema": _obj({}),
        "handler": lambda a: fai.rank_snapshot(),
    },
    {
        "name": "news_status",
        "description": "Summarise the hourly AI-company news bot state (dedupe counts, rotation index, sanitised log tail). Never reads or prints the PAT.",
        "inputSchema": _obj({"tail": I}),
        "handler": lambda a: fai.news_status(int(a.get("tail", 12))),
    },
    {
        "name": "news_dry_run",
        "description": "Run scripts/ai-news/news_bot.py in dry-run mode to preview unseen headlines without publishing. Requires network; output is token-redacted.",
        "inputSchema": _obj({"per_run": I, "timeout": I}),
        "handler": lambda a: fai.news_dry_run(int(a.get("per_run", 3)), int(a.get("timeout", 90))),
    },
    {
        "name": "preflight_submission",
        "description": "Simulate the contribution-triage and content-validation checks before opening a PR. Advisory only: humans are marked for review, never auto-rejected.",
        "inputSchema": _obj(
            {
                "title": S,
                "body": S,
                "files": SA,
                "author_type": S,
                "account_age_days": I,
                "followers": I,
                "public_repos": I,
            }
        ),
        "handler": lambda a: fai.preflight_submission(
            title=a.get("title", ""),
            body=a.get("body", ""),
            files=a.get("files"),
            author_type=a.get("author_type", ""),
            account_age_days=a.get("account_age_days"),
            followers=a.get("followers"),
            public_repos=a.get("public_repos"),
        ),
    },
]

BY_NAME: dict[str, dict[str, Any]] = {tool["name"]: tool for tool in TOOLS}

BOUNDS: dict[str, dict[str, tuple[int, int]]] = {
    "search_repo": {"limit": (1, 200)},
    "news_status": {"tail": (1, 200)},
    "news_dry_run": {"per_run": (1, 20), "timeout": (1, 300)},
}


def _validate_args(name: str, args: Any) -> dict[str, Any]:
    """Enforce inputSchema types and numeric bounds before calling a tool."""
    if not isinstance(args, dict):
        raise ValueError("arguments must be a JSON object")
    tool = BY_NAME[name]
    schema = tool["inputSchema"]
    props: dict[str, Any] = schema.get("properties", {})
    for key in schema.get("required", []):
        if key not in args:
            raise ValueError(f"missing required argument: {key}")
    for key, value in args.items():
        spec = props.get(key)
        if spec is None:
            raise ValueError(f"unexpected argument: {key}")
        expected = spec.get("type")
        valid = {
            "string": lambda v: isinstance(v, str),
            "boolean": lambda v: isinstance(v, bool),
            "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
            "array": lambda v: isinstance(v, list),
        }.get(expected)
        if valid is None or not valid(value):
            raise ValueError(f"{key} must be {expected}")
        if expected == "array" and "items" in spec:
            item_type = spec["items"].get("type")
            for item in value:
                ok = isinstance(item, str) if item_type == "string" else True
                if not ok:
                    raise ValueError(f"{key} items must be {item_type}")
    for key, (low, high) in BOUNDS.get(name, {}).items():
        if key in args and not low <= args[key] <= high:
            raise ValueError(f"{key} must be between {low} and {high}")
    return args


def _reply(msg_id: Any, result: dict[str, Any]) -> None:
    sys.stdout.write(
        json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}, ensure_ascii=False) + "\n"
    )
    sys.stdout.flush()


def _error(msg_id: Any, code: int, message: str) -> None:
    sys.stdout.write(
        json.dumps(
            {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}},
            ensure_ascii=False,
        )
        + "\n"
    )
    sys.stdout.flush()


def dispatch(msg: dict[str, Any]) -> None:
    msg_id = msg.get("id")
    method = msg.get("method", "")
    if "id" not in msg:  # notification
        return
    if method == "initialize":
        params = msg.get("params") or {}
        _reply(
            msg_id,
            {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
            },
        )
    elif method == "ping":
        _reply(msg_id, {})
    elif method == "tools/list":
        _reply(
            msg_id,
            {
                "tools": [
                    {k: v for k, v in tool.items() if k in ("name", "description", "inputSchema")}
                    for tool in TOOLS
                ]
            },
        )
    elif method in ("resources/list", "prompts/list"):
        _reply(msg_id, {"resources": [], "prompts": []})
    elif method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name", "")
        args = params.get("arguments") or {}
        tool = BY_NAME.get(name)
        if not tool:
            _error(msg_id, -32602, f"unknown tool: {name}")
            return
        handler: Callable[[dict[str, Any]], Any] = tool["handler"]
        try:
            payload = handler(_validate_args(name, args))
            text = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
            _reply(msg_id, {"content": [{"type": "text", "text": text}]})
        except Exception as exc:  # noqa: BLE001 - MCP must surface tool errors, not die
            _reply(
                msg_id,
                {
                    "content": [
                        {"type": "text", "text": f"{type(exc).__name__}: {fai.redact(str(exc))}"}
                    ],
                    "isError": True,
                },
            )
    else:
        _error(msg_id, -32601, f"method not found: {method}")


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            if isinstance(msg, dict):
                dispatch(msg)
        except json.JSONDecodeError as exc:
            _error(None, -32700, f"parse error: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
