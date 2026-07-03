import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "check_ledger.py"


def run_hook(home: Path, payload: dict, env: dict | None = None) -> subprocess.CompletedProcess:
    full_env = {"FESTACK_HOME": str(home), "PATH": "/usr/bin:/bin"}
    if env:
        full_env.update(env)
    return subprocess.run(
        ["python3", str(HOOK)],
        input=json.dumps(payload),
        env=full_env,
        capture_output=True,
        text=True,
        timeout=10,
    )


def make_ledger(home: Path, log_lines: list[str]) -> Path:
    eng = home / "engagements"
    slug = eng / "dbs-sg-eval"
    slug.mkdir(parents=True)
    (eng / "ENGAGEMENTS.md").write_text(
        "| slug | account | status | last-touched | next step | aliases |\n"
        "| dbs-sg-eval | DBS Bank Singapore | active | 2026-06-10 | review | dbs |\n",
        encoding="utf-8",
    )
    (slug / "brief.md").write_text("# brief\n", encoding="utf-8")
    (slug / "log.md").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return slug / "log.md"


class LastLookHookTests(unittest.TestCase):
    def test_warns_on_unreviewed_artifact_and_appends_outbound_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, ["2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted"])
            result = run_hook(home, {"text": "sending dbs-onepager to the client", "channel": "gmail", "external": True})
            self.assertEqual(result.returncode, 0)
            self.assertIn("no review on record", result.stdout)
            log_text = log.read_text(encoding="utf-8")
            self.assertIn("outbound", log_text)
            self.assertIn("review state at send: unreviewed", log_text)

    def test_silent_pass_when_reviewed(self) -> None:
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, [
                "2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted",
                "2026-06-10 | /review-work | artifact: dbs-onepager v2 | reviewed: 0 blockers",
            ])
            result = run_hook(home, {"text": "sending dbs-onepager v2", "channel": "gmail", "external": True})
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("no review on record", result.stdout)
            self.assertIn("review state at send: reviewed", log.read_text(encoding="utf-8"))

    def test_no_artifact_match_is_silent_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, ["2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted"])
            before = log.read_text(encoding="utf-8")
            result = run_hook(home, {"text": "lunch at 12?", "channel": "slack", "external": True})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")
            self.assertEqual(before, log.read_text(encoding="utf-8"))

    def test_silent_and_no_receipt_when_externality_unknown(self) -> None:
        # Adapter could not tell internal from external: hook must stay silent
        # and write nothing, even though the artifact matches.
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, ["2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted"])
            before = log.read_text(encoding="utf-8")
            result = run_hook(home, {"text": "sending dbs-onepager v2", "channel": "slack"})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")
            self.assertEqual(before, log.read_text(encoding="utf-8"))

    def test_second_send_of_unreviewed_artifact_still_warns(self) -> None:
        # Regression (C1): the outbound receipt's "review state at send: unreviewed"
        # tail must not be misread as a review on the next send.
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, ["2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted"])
            payload = {"text": "sending dbs-onepager to the client", "channel": "gmail", "external": True}
            first = run_hook(home, payload)
            self.assertEqual(first.returncode, 0)
            self.assertIn("no review on record", first.stdout)
            second = run_hook(home, payload)
            self.assertEqual(second.returncode, 0)
            self.assertIn("no review on record", second.stdout)
            log_text = log.read_text(encoding="utf-8")
            self.assertEqual(log_text.count("review state at send: unreviewed"), 2)
            self.assertNotIn("review state at send: reviewed", log_text)

    def test_longer_artifact_name_is_not_shadowed_by_shorter_prefix(self) -> None:
        # Regression (C2): mentioning only "dbs-onepager-final" must not also
        # match "dbs-onepager" and log a phantom outbound receipt for it.
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, [
                "2026-06-10 | /doc | artifact: dbs-onepager v1 | drafted",
                "2026-06-10 | /review-work | artifact: dbs-onepager v1 | reviewed: 0 blockers",
                "2026-06-10 | /doc | artifact: dbs-onepager-final v1 | drafted",
            ])
            result = run_hook(home, {"text": "sending dbs-onepager-final to the client", "channel": "gmail", "external": True})
            self.assertEqual(result.returncode, 0)
            self.assertIn("no review on record for dbs-onepager-final", result.stdout)
            self.assertEqual(len(result.stdout.strip().splitlines()), 1)
            log_text = log.read_text(encoding="utf-8")
            self.assertEqual(log_text.count("| outbound |"), 1)
            self.assertIn("outbound | artifact: dbs-onepager-final v1", log_text)

    def test_claude_code_payload_adapter_gmail_externality(self) -> None:
        # Regression (I1): raw Claude Code PreToolUse payloads must be translated.
        # With FESTACK_ORG_DOMAIN set and an outside-org recipient: warn + receipt.
        # Without the env var, externality is unknowable: silent, no write.
        payload = {
            "tool_name": "mcp__google__gmail_message_send",
            "tool_input": {"to": ["x@dbs.com"], "body": "dbs-onepager v2 attached"},
        }
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, ["2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted"])
            result = run_hook(home, payload, env={"FESTACK_ORG_DOMAIN": "databricks.com"})
            self.assertEqual(result.returncode, 0)
            self.assertIn("no review on record", result.stdout)
            log_text = log.read_text(encoding="utf-8")
            self.assertIn("sent via gmail", log_text)
            self.assertIn("review state at send: unreviewed", log_text)
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            log = make_ledger(home, ["2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted"])
            before = log.read_text(encoding="utf-8")
            result = run_hook(home, payload)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")
            self.assertEqual(before, log.read_text(encoding="utf-8"))

    def test_fail_open_on_corrupt_home(self) -> None:
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            (home / "engagements").mkdir()
            (home / "engagements" / "ENGAGEMENTS.md").write_text("not | a | table", encoding="utf-8")
            result = run_hook(home, {"text": "anything", "external": True})
            self.assertEqual(result.returncode, 0)

    def test_fail_open_on_garbage_stdin(self) -> None:
        with tempfile.TemporaryDirectory() as home_str:
            result = subprocess.run(
                ["python3", str(HOOK)], input="not json", env={"FESTACK_HOME": home_str, "PATH": "/usr/bin:/bin"},
                capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
