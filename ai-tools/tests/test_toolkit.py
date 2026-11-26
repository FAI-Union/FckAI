"""Regression tests for the FAI AI toolkit (stdlib unittest only).

Run: python -m unittest discover -s D:/Git/FAI/ai-tools/tests -v
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))
sys.path.insert(0, str(TOOLS_DIR.parent / "scripts" / "ai-news"))
import core as fai  # noqa: E402
import mcp_server  # noqa: E402
import news_bot  # noqa: E402


class CoreTests(unittest.TestCase):
    def test_repo_shape(self):
        overview = fai.repo_overview()
        self.assertEqual(overview["repository"], "FAI-Union/FckAI")
        self.assertEqual(len(fai.evidence_files()), 21)

    def test_all_cards_validate(self):
        results = [fai.validate_evidence(p.stem) for p in fai.evidence_files()]
        failed = [r["id"] for r in results if not r["ok"]]
        self.assertEqual(failed, [], f"invalid cards: {failed}")

    def test_next_id_and_scaffold(self):
        candidate = fai.next_evidence_id()["id"]
        self.assertRegex(candidate, r"^EV-\d{4}-\d{3}$")
        draft = fai.scaffold_evidence(
            claim_en="Example claim in English.",
            claim_zh="示例中文主张。",
            source_url="https://example.org/report",
            publisher="Example Publisher",
            excerpt="A short verbatim quote from the original report.",
            caveats="Scope limited to one jurisdiction; projection rather than measurement.",
            tags=["example"],
            publication_date="2026-11-26",
        )["draft"]
        result = fai.validate_evidence(text=draft)
        self.assertTrue(result["ok"], result)
        self.assertIn(candidate, draft)

    def test_links_and_chain_clean(self):
        links = fai.validate_links()
        self.assertTrue(links["ok"], links["broken"])
        chain = fai.check_evidence_chain()
        self.assertTrue(chain["ok"], chain)

    def test_translation_status(self):
        status = fai.translation_status()
        self.assertIn("zh-CN", status["locale_dirs"])
        self.assertEqual(len(status["priority_tags"]), 10)
        bad = fai.validate_translation("es", title="add Spanish translation", changed_files=["LANGUAGES.md"])
        self.assertFalse(bad["ok"])
        good = fai.validate_translation(
            "zh-CN",
            title="i18n(zh-CN): add Chinese translation",
            changed_files=["LANGUAGES.md", "locales/zh-CN/README.md"],
        )
        self.assertTrue(good["ok"], good)

    def test_preflight_rules(self):
        blocked = fai.preflight_submission(files=["RESEARCH/EV-2026-022.md"], body="see attached")
        self.assertEqual(blocked["decision"], "block")
        passed = fai.preflight_submission(
            files=["RESEARCH/EV-2026-022.md"], body="Source: https://example.org"
        )
        self.assertEqual(passed["decision"], "pass")
        bot = fai.preflight_submission(author_type="Bot")
        self.assertEqual(bot["decision"], "bot")
        newbie = fai.preflight_submission(account_age_days=1, followers=0, public_repos=0)
        self.assertEqual(newbie["decision"], "needs-review")

    def test_no_secret_leak_in_status(self):
        payload = json.dumps(fai.news_status(), ensure_ascii=False)
        self.assertNotIn("github_pat_", payload)
        self.assertNotIn("ghp_", payload)

    def test_rank_snapshot(self):
        snapshot = fai.rank_snapshot()
        rows = {r["query"]: r for r in snapshot["rows"]}
        self.assertEqual(rows["AI accountability evidence"]["baseline"], "24")
        self.assertEqual(rows["AI accountability evidence"]["current"], "4")


class McpProtocolTests(unittest.TestCase):
    def test_stdio_handshake_and_tools(self):
        proc = subprocess.Popen(
            [sys.executable, str(TOOLS_DIR / "mcp_server.py")],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        messages = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}},
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "repo_overview", "arguments": {}},
            },
        ]
        try:
            for msg in messages:
                proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
            proc.stdin.flush()
            proc.stdin.close()
            replies = [json.loads(line) for line in proc.stdout.read().splitlines() if line.strip()]
            by_id = {r.get("id"): r for r in replies}
            self.assertEqual(by_id[1]["result"]["serverInfo"]["name"], "fai")
            self.assertGreaterEqual(len(by_id[2]["result"]["tools"]), 15)
            content = by_id[3]["result"]["content"][0]["text"]
            self.assertIn("FAI-Union/FckAI", content)
            self.assertEqual(proc.wait(timeout=10), 0)
        finally:
            if proc.poll() is None:
                proc.kill()
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                if stream and not stream.closed:
                    stream.close()
            proc.wait(timeout=10)

    def test_tool_registry_is_unique(self):
        names = [tool["name"] for tool in mcp_server.TOOLS]
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(tool["inputSchema"]["type"] == "object" for tool in mcp_server.TOOLS))


class SecurityRegressionTests(unittest.TestCase):
    def test_scaffold_rejects_frontmatter_injection(self):
        kwargs = dict(
            claim_en="Benign claim.",
            claim_zh="良性主张。",
            source_url="https://example.org/original",
            publisher="Example",
            excerpt="Quote.",
            caveats="Scope note long enough to pass validation checks.",
            evidence_id="EV-2026-999",
        )
        with self.assertRaises(ValueError):
            fai.scaffold_evidence(**kwargs, tags=["ok]\nstatus: injected"])
        bad_url = dict(kwargs, source_url="http://example.org/original")
        with self.assertRaises(ValueError):
            fai.scaffold_evidence(**bad_url)

    def test_redact_live_environment_secret(self):
        os.environ["GH_PAT"] = "test_secret_123456"
        try:
            self.assertEqual(
                fai.redact("value=test_secret_123456"), "value=[REDACTED]"
            )
            self.assertEqual(
                news_bot.redact("value=test_secret_123456"), "value=[REDACTED]"
            )
        finally:
            del os.environ["GH_PAT"]

    def test_news_fields_are_single_line_and_links_are_whitelisted(self):
        self.assertEqual(
            news_bot.clean_field("hello\n## injected", 100), "hello ## injected"
        )
        self.assertEqual(news_bot.safe_link("javascript:alert(1)"), "")
        self.assertEqual(
            news_bot.safe_link("https://example.org/a?b=1"),
            "https://example.org/a?b=1",
        )
        body = news_bot.discussion_body({
            "company": "OpenAI",
            "title": "hello\n## injected [x](https://evil.example)",
            "source": "RSS",
            "published": "2026-01-01",
            "url": "javascript:alert(1)",
        })
        headline = next(line for line in body.splitlines() if "Headline:" in line)
        self.assertTrue(headline.startswith("- **Headline:** `"))
        self.assertTrue(headline.endswith("`"))
        self.assertIn("_unavailable_", body)

    def test_paths_outside_root_are_rejected(self):
        outside = fai.root().parent / "README.md"
        with self.assertRaises(ValueError):
            fai._ensure_readable(outside)

    def test_mcp_argument_validation(self):
        with self.assertRaises(ValueError):
            mcp_server._validate_args("search_repo", {"query": 123})
        with self.assertRaises(ValueError):
            mcp_server._validate_args("search_repo", {"query": "x", "limit": 1000})
        with self.assertRaises(ValueError):
            mcp_server._validate_args("search_repo", {"query": "x", "extra": 1})
        self.assertEqual(
            mcp_server._validate_args("search_repo", {"query": "x", "limit": 20}),
            {"query": "x", "limit": 20},
        )


if __name__ == "__main__":
    unittest.main()
