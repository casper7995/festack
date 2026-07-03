# festack Engagement Ledger v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give festack persistent per-engagement state (two-tier ledger), a `/handoff` packager, a never-blocking last-look hook with outbound audit trail, automatic lifecycle, and a claim-grounded client-persona reviewer.

**Architecture:** Plain-Markdown ledgers under `$FESTACK_HOME/engagements/` written by the existing closeout-receipt convention; one new authoritative prose reference (`ledger-lifecycle.md`) that every touched skill points at; one Python core script for the hook with thin host adapters. Code only for state-awareness (the hook); judgment stays prose.

**Tech Stack:** Markdown skills (Cursor/Claude Code `SKILL.md`), Python 3 stdlib (hook + tests via `unittest`), bash installer, plugin manifests.

**Spec:** `docs/superpowers/specs/2026-06-10-festack-engagement-ledger-design.md`

**Branch note:** Work on branch `ledger-v2` off `claude-code-port` (Task 0). The port branch is unmerged; do not touch `main`.

---

### Task 0: Branch

**Files:** none (git only)

- [ ] **Step 1: Create the branch**

```bash
cd <path-to-festack-repo>
git checkout claude-code-port && git checkout -b ledger-v2 && git status -sb
```

Expected: `## ledger-v2`, clean tree.

---

### Task 1: Contract tests for v2 prose invariants (TDD — all failing)

**Files:**
- Modify: `tests/test_contracts.py` (append a new class at the end)

- [ ] **Step 1: Append the test class**

```python
class LedgerV2ContractTests(unittest.TestCase):
    """Invariants from docs/superpowers/specs/2026-06-10-festack-engagement-ledger-design.md."""

    def test_ledger_lifecycle_reference_exists_with_required_sections(self) -> None:
        text = read("skills/festack/references/ledger-lifecycle.md")
        for required in (
            "ENGAGEMENTS.md", "brief.md", "log.md", "## Head and annex",
            "superseded", "## Statuses", "dormant", "## Compaction",
            "## Auto-create", "## Receipt format", "archive/",
        ):
            self.assertIn(required, text, f"ledger-lifecycle.md missing: {required}")

    def test_router_announces_pick_and_hard_asks_collisions(self) -> None:
        text = read("skills/festack/SKILL.md")
        self.assertIn("ledger-lifecycle.md", text)
        self.assertIn("announce", text.lower())
        self.assertIn("collision", text.lower())

    def test_handoff_skill_exists(self) -> None:
        text = read("skills/handoff/SKILL.md")
        self.assertIn("name: handoff", text)
        for required in ("brief", "open gates", "next Monday", "paste", "coverage"):
            self.assertIn(required, text, f"handoff SKILL.md missing: {required}")
        self.assertIn("/handoff", read("skills/festack/references/routing-table.md"))

    def test_closeout_convention_appends_to_ledger(self) -> None:
        # Every public skill closeout must carry the ledger-append line.
        missing = []
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            if "## Closeout receipt" in text and "log.md" not in text:
                missing.append(str(path.relative_to(ROOT)))
        self.assertEqual(missing, [], "closeout sections missing the ledger append line")

    def test_hook_never_blocks(self) -> None:
        text = read("hooks/check_ledger.py")
        self.assertIn("sys.exit(0)", text)
        self.assertNotIn("sys.exit(1)", text)
        self.assertNotIn("sys.exit(2)", text)
        self.assertIn("fail-open", text)

    def test_review_work_persona_seat_is_claim_grounded(self) -> None:
        text = read("skills/review-work/SKILL.md")
        self.assertIn("persona", text.lower())
        self.assertIn("claim inventory", text)
```

- [ ] **Step 2: Run to verify all 6 fail**

Run: `python3 -m unittest tests.test_contracts.LedgerV2ContractTests -v`
Expected: 6 failures/errors (missing files/strings). Pre-existing classes still pass: `python3 -m unittest tests.test_contracts.FestackContractTests -q` → OK.

- [ ] **Step 3: Commit**

```bash
git add tests/test_contracts.py && git commit -m "test: ledger v2 contract tests (failing)"
```

---

### Task 2: The authoritative reference — `ledger-lifecycle.md`

**Files:**
- Create: `skills/festack/references/ledger-lifecycle.md`

- [ ] **Step 1: Create the file with exactly this content**

````markdown
# engagement ledger lifecycle

The single authoritative reference for festack engagement state. Skills that read or
write ledgers follow this file; do not restate its rules elsewhere.

## Layout

```
$FESTACK_HOME/engagements/
  ENGAGEMENTS.md          # index, one line per engagement
  <slug>/
    brief.md              # tier 1: curated facts
    log.md                # tier 2: append-only receipts
  archive/<slug>/         # closed engagements, moved whole
```

`$FESTACK_HOME`: environment value when set; otherwise Cursor `~/.cursor/festack`,
Claude Code `~/.claude/festack`. Pointing both hosts at one shared directory is
recommended; it solves cross-host continuity, not cross-person sharing.

## Index line format (ENGAGEMENTS.md)

One Markdown table row per engagement:

```
| slug | account | status | last-touched | next step | aliases |
| dbs-sg-eval | DBS Bank Singapore | active | 2026-06-10 | review questionnaire v2 | dbs, dbs sg |
```

Statuses: `active`, `dormant`, `closed-won`, `closed-lost`, `closed-dropped`. Archived
engagements are removed from this index entirely.

## brief.md: Head and annex

- **Head** (top of file to the `<!-- annex -->` marker): capped at roughly one page.
  The only ledger content resume loads. Sections: Status and next step; Brief (goal,
  audience, timeline, playbook); Live decisions and gate answers; Stakeholder personas;
  Accepted residual risks.
- **Annex** (below the marker): read on demand, never auto-loaded. Holds superseded
  decisions with dates, full gate history, extended persona notes.
- Facts are **superseded in place**: when a fact changes, write the new value in the
  head and move the old line to the annex with a `superseded YYYY-MM-DD` marker. Facts
  are never deleted and never compacted. The head cap is enforced by moving aged facts
  to the annex.

## log.md: Receipt format

Append-only. One receipt per skill completion, one line, pipe-separated:

```
YYYY-MM-DD | <skill> | artifact: <name> v<N> | <outcome>
2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted
2026-06-10 | /review-work | artifact: dbs-onepager v2 | reviewed: 0 blockers 0 majors | panel: 3 workers, lenses correctness/client-readiness/persona
2026-06-10 | /client-debug | RLS question answered, cited, high confidence
2026-06-10 | outbound | artifact: dbs-onepager v2 | sent via gmail | review state at send: reviewed
```

Omit the `artifact:` field when no artifact is involved. Prose dumps and transcript
excerpts are forbidden input formats. Compaction summaries sit at the top of the file;
raw receipts below.

## Auto-create

The first time any festack skill runs **with a named account as the subject of the
work** and no matching engagement exists: propose a slug inline ("creating
`dbs-sg-eval` — ok?"), accept an override in the same breath, create the folder, the
index row, and a brief.md head seeded from the current context, then continue the
actual work. One inline confirm, zero ceremony. A passing mention of another account
("like we did for DBS" while working a different deal) never creates a ledger; it
resolves against existing engagements or nothing. No setup flow. Generic or unnamed
work runs stateless; never force a ledger.

## Resume

- Match the user's words against **account names and aliases** from the index, never
  slugs alone.
- **Always announce the pick first**: "**<slug> (<account>)** — resuming. Last
  activity: <...>. Next step: <...>". A wrong pick must be catchable at a glance.
- **Name-stem collisions hard-ask.** If more than one engagement matches, ask; never
  silently default. There is no single-active silent default.
- Load the brief.md head only. Resuming a `dormant` engagement flips it back to
  `active`.

## Statuses and transitions

- `active` → `dormant`: automatic when last-touched is 30+ days ago, applied at the
  next index read. Dormant engagements drop to a separate section of the index view
  and stay fully resumable. Quiet is neutral; never ask whether to close.
- any → `closed-*`: only when the user declares an outcome. Run `/retro` over the full
  ledger first (the one time log.md is read whole), distill lessons to the host's
  lesson store, stamp the outcome in brief.md, then move the folder to `archive/` and
  remove the index row. Retro-before-archive is mandatory ordering.
- On Cursor, continual-learning mines transcripts passively; `/retro` remains the
  authoritative engagement-close harvester. Do not write duplicate lessons.

## Compaction

Trigger (observable only): at resume, when log.md exceeds 40 raw receipts or the brief
head exceeds its cap. Action: collapse the oldest receipts into one dated summary block
at the top of log.md and delete the raw lines beneath. Pinned exception: receipts for
artifact versions not yet sent stay until sent or superseded (the last-look hook reads
them). brief.md is never compacted (supersede instead).

## Privacy

Outbound receipts are a plaintext local record of what was sent to which customer.
Keep `FESTACK_HOME` on storage you control; do not place it on a synced or shared
drive without considering who can read it.

## Maintenance contract

All maintenance happens at touchpoints the agent already occupies (resume, close):
no daemon, no scheduler, no background process, no decision ever required from the FE.
Everything is plain Markdown: user-editable, deletable, git-able.
````

- [ ] **Step 2: Run the reference test**

Run: `python3 -m unittest tests.test_contracts.LedgerV2ContractTests.test_ledger_lifecycle_reference_exists_with_required_sections -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add skills/festack/references/ledger-lifecycle.md && git commit -m "feat: ledger lifecycle reference"
```

---

### Task 3: Router — resume, inference, auto-create, announce, collisions

**Files:**
- Modify: `skills/festack/SKILL.md` (Step 0 list ~line 13, new Step after setup gaps, receipt section)
- Modify: `skills/festack/references/routing-table.md` (map + receipt preamble)

- [ ] **Step 1: Add ledger orientation to `skills/festack/SKILL.md` Step 0**

After the line `- Resolve `$FESTACK_HOME` first. ...` insert:

```
- Read `$FESTACK_HOME/engagements/ENGAGEMENTS.md` if it exists. Engagement state and all ledger rules live in `references/ledger-lifecycle.md`; read it before any ledger read or write. Apply auto-dormant transitions to the index now (last-touched 30+ days → `dormant`).
```

- [ ] **Step 2: Insert a new "Step 2.5: engagement context" section in `skills/festack/SKILL.md`**

After the `## Step 2: handle setup gaps` section, insert:

```markdown
## Step 2.5: engagement context

Before routing, resolve which engagement this work belongs to, per
`references/ledger-lifecycle.md`:

- Match the ask against account names and aliases in the index. On a match, **announce
  the pick before anything else**: "**<slug> (<account>)** — resuming. Last activity:
  <...>. Next step: <...>", then load the brief.md head only.
- On a name-stem collision (more than one match), hard-ask with one `AskQuestion`;
  never silently default. There is no single-active silent default: with one engagement
  the inference still matches and still announces.
- Bare `/festack` with no ask shows the index view: active engagements first, one line
  each with next steps, always ending with a dormant-count line ("dormant: 4 — oldest
  quiet 47d: `lotte-eval`") so the Monday screen never shows a clean board when it
  isn't one.
- A named account **that is the subject of the work** with no matching engagement
  triggers auto-create: propose a slug inline, accept an override in the same breath,
  seed brief.md from current context, continue. A passing mention of another account
  never creates a ledger. Generic or unnamed work runs stateless; never force a ledger.
- `/festack resume <slug>` is the explicit fallback and follows the same announce rule.
```

- [ ] **Step 3: Add routing rows to `skills/festack/references/routing-table.md`**

After the `| Carry a broad FE task through multiple skills | ... |` row, add:

```
| Resume an engagement / "where were we on X" | `/festack` | Inference per ledger-lifecycle.md; announce the pick; collisions hard-ask. |
| Package an engagement for a colleague | `/handoff` | Self-contained snapshot from the ledger; paste it yourself. |
```

- [ ] **Step 4: Run the router test**

Run: `python3 -m unittest tests.test_contracts.LedgerV2ContractTests.test_router_announces_pick_and_hard_asks_collisions -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add skills/festack && git commit -m "feat: router engagement context — resume, announce, collisions, auto-create"
```

---

### Task 4: Closeout convention sweep — every skill appends to the ledger

**Files:**
- Modify: every `skills/*/SKILL.md` containing a `## Closeout receipt` section (grep first; ~15 files)

- [ ] **Step 1: Find the targets**

Run: `grep -l '## Closeout receipt' skills/*/SKILL.md`
Expected: list of skill files (festack-debate has no closeout; that is fine).

- [ ] **Step 2: Add the ledger bullet to each closeout section**

In each file, after the `- `visual_artifact_receipt`: ...` bullet, add exactly:

```
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
```

- [ ] **Step 3: Run the sweep test**

Run: `python3 -m unittest tests.test_contracts.LedgerV2ContractTests.test_closeout_convention_appends_to_ledger -v`
Expected: PASS. Also run the full pre-existing suite: `python3 -m unittest tests.test_contracts -q` → only remaining LedgerV2 failures are handoff/hook/persona (Tasks 5-7).

- [ ] **Step 4: Commit**

```bash
git add skills && git commit -m "feat: closeout receipts append to the active engagement ledger"
```

---

### Task 5: `/handoff` skill

**Files:**
- Create: `skills/handoff/SKILL.md`

- [ ] **Step 1: Create the skill with exactly this content**

````markdown
---
name: handoff
description: Package an engagement's ledger into one self-contained snapshot a colleague can pick up; use before travel, coverage swaps, or account transitions.
disable-model-invocation: true
---

# /handoff

Turn the live state of one engagement into a single artifact another human can pick up
cold. The reader is a colleague who knows nothing about the account and has thirty
minutes before their first call.

## Workflow

1. **Resolve the engagement** with the same inference rules as resume
   (`festack/references/ledger-lifecycle.md`): match account names and aliases,
   announce the pick, hard-ask on collisions. No ledger for this account means there is
   nothing to hand off; say so and offer to summarize from conversation instead.
2. **Read** the brief.md head, the open gates from its decisions section, and the most
   recent receipts in log.md (compacted view; do not dump the raw log).
3. **Compose the snapshot** as one self-contained Markdown block:
   - A **coverage line first**: "last receipt: <age>; <N> receipts this phase — ledger
     may not reflect untracked work (calls, hallway Slack, customer files)." Frame
     "what I'd do next Monday" as derived from the ledger, not asserted. A confident
     hollow snapshot is worse than a writeup that knows what it doesn't know.
   - Account, status, and one-sentence engagement goal.
   - The brief: audience, timeline, playbook position.
   - Decisions made and **open gates** (what is undecided and who owns it).
   - Accepted residual risks.
   - Stakeholder personas (who is in the room, what they care about).
   - Recent activity: the last few receipts, summarized.
   - **What I'd do next Monday**: the concrete next step from the playbook position,
     in one short paragraph.
4. **Audience argument.** Default is FE-to-FE full fidelity. "for my AE" (or any named
   non-technical audience) trims internals: drop receipts and panel details, keep
   status, decisions, risks, and next step.
5. **Deliver in chat for the FE to paste** into Slack, Notion, or a doc. festack does
   not send it anywhere itself. Offer `/doc` packaging only if asked.

## Prose

All output follows the `fe-deslop` skill. The snapshot must stand alone: no references
to "above", "this chat", or files the reader cannot open.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: prose snapshot, owner: the FE who pastes it.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
````

- [ ] **Step 2: Run the handoff test**

Run: `python3 -m unittest tests.test_contracts.LedgerV2ContractTests.test_handoff_skill_exists -v`
Expected: PASS (routing-table row landed in Task 3).
Also: `python3 -m unittest tests.test_contracts.FestackContractTests -q` → OK (frontmatter contract test must accept the new skill; its `name:` matches the directory).

- [ ] **Step 3: Commit**

```bash
git add skills/handoff && git commit -m "feat: /handoff engagement snapshot skill"
```

---

### Task 6: Last-look hook — core script + unit tests

**Files:**
- Create: `hooks/check_ledger.py`
- Create: `tests/test_hook.py`

- [ ] **Step 1: Write the failing unit tests (`tests/test_hook.py`)**

```python
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "check_ledger.py"


def run_hook(home: Path, payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(HOOK)],
        input=json.dumps(payload),
        env={"FESTACK_HOME": str(home), "PATH": "/usr/bin:/bin"},
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

    def test_fail_open_on_corrupt_home(self) -> None:
        with tempfile.TemporaryDirectory() as home_str:
            home = Path(home_str)
            (home / "engagements").mkdir()
            (home / "engagements" / "ENGAGEMENTS.md").write_text("not | a | table", encoding="utf-8")
            result = run_hook(home, {"text": "anything"})
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
```

- [ ] **Step 2: Run to verify failure**

Run: `python3 -m unittest tests.test_hook -v`
Expected: errors (hooks/check_ledger.py does not exist).

- [ ] **Step 3: Write `hooks/check_ledger.py`**

```python
#!/usr/bin/env python3
"""festack last-look hook core.

Reads a JSON payload on stdin describing an outward-facing send, checks active
engagement ledgers for the review state of any referenced artifact, prints at most one
awareness line to stdout (never blocks), and appends an outbound receipt to the
matching log.md.

Contract: ALWAYS exits 0 (fail-open). This script must never be able to stop a send.
Host adapters translate each host's hook payload into {"text": ..., "channel": ...}.
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path


def festack_home() -> Path | None:
    env = os.environ.get("FESTACK_HOME")
    if env:
        return Path(env)
    for candidate in (Path.home() / ".claude/festack", Path.home() / ".cursor/festack"):
        if candidate.exists():
            return candidate
    return None


def active_slugs(engagements: Path) -> list[str]:
    index = engagements / "ENGAGEMENTS.md"
    if not index.exists():
        return []
    slugs = []
    for line in index.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[2] in ("active", "dormant") and cells[0] != "slug":
            slugs.append(cells[0])
    return slugs


ARTIFACT = re.compile(r"artifact:\s*([^|]+?)\s+v(\d+)")


def artifact_states(log_text: str) -> dict[str, dict]:
    """name -> {latest: int, reviewed: set[int]} from receipt lines."""
    states: dict[str, dict] = {}
    for line in log_text.splitlines():
        match = ARTIFACT.search(line)
        if not match:
            continue
        name, version = match.group(1).strip(), int(match.group(2))
        state = states.setdefault(name, {"latest": 0, "reviewed": set()})
        state["latest"] = max(state["latest"], version)
        if "reviewed" in line.split("|", 3)[-1]:
            state["reviewed"].add(version)
    return states


def main() -> None:
    payload = json.load(sys.stdin)
    text = str(payload.get("text", ""))
    channel = str(payload.get("channel", "unknown"))
    # Outward-detection rule: adapters set external=True only on positive evidence
    # (recipient outside the org domain, shared/external Slack channel, Drive share
    # outside the org). Can't tell -> stay silent, write no receipt.
    if payload.get("external") is not True:
        return
    home = festack_home()
    if not home or not text:
        return
    engagements = home / "engagements"
    today = datetime.date.today().isoformat()
    for slug in active_slugs(engagements):
        log_path = engagements / slug / "log.md"
        if not log_path.exists():
            continue
        log_text = log_path.read_text(encoding="utf-8")
        for name, state in artifact_states(log_text).items():
            if name.lower() not in text.lower():
                continue
            latest, reviewed = state["latest"], state["reviewed"]
            review_state = "reviewed" if latest in reviewed else "unreviewed"
            if review_state == "unreviewed":
                if reviewed:
                    print(f"last-look: {name} v{latest} edited since its last review (v{max(reviewed)}) — send is proceeding.")
                else:
                    print(f"last-look: no review on record for {name} — send is proceeding.")
            with log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(
                    f"{today} | outbound | artifact: {name} v{latest} | sent via {channel} | review state at send: {review_state}\n"
                )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # fail-open: a broken hook must never affect a send
    sys.exit(0)
```

- [ ] **Step 4: Run the hook tests**

Run: `python3 -m unittest tests.test_hook -v`
Expected: 6 PASS.
Run: `python3 -m unittest tests.test_contracts.LedgerV2ContractTests.test_hook_never_blocks -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add hooks/check_ledger.py tests/test_hook.py && git commit -m "feat: last-look hook core (never blocks, outbound audit trail)"
```

---

### Task 7: Hook adapters + manifest wiring + test runner

**Files:**
- Create: `hooks/hooks.json` (Claude Code wiring)
- Create: `hooks/cursor-hooks.json` (Cursor wiring template)
- Modify: `scripts/test.sh` (add the hook tests)
- Modify: `README.md` (document the hook + ledger in a short v2 section)

- [ ] **Step 1: Claude Code wiring — `hooks/hooks.json`**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__google__gmail_message_send|mcp__google__drive_file_create|mcp__slack__slack_write_api_call",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/check_ledger.py\""
          }
        ]
      }
    ]
  }
}
```

Note for the implementer: Claude Code passes the tool call JSON on stdin; `check_ledger.py` tolerates any JSON shape (it reads `text`/`channel` keys and fails open otherwise). A richer adapter that maps `tool_input` into `text` is acceptable if `claude plugin validate .` accepts it; keep exit 0 semantics regardless.

- [ ] **Step 2: Cursor wiring template — `hooks/cursor-hooks.json`**

```json
{
  "version": 1,
  "hooks": {
    "beforeMCPExecution": [
      { "command": "python3 ~/.cursor/festack/hooks/check_ledger.py" }
    ]
  }
}
```

With a header comment in README (Step 4) that Cursor users merge this into `~/.cursor/hooks.json` (Cursor has no per-plugin hook auto-loading; the installer prints the instruction, it does not edit user hook config).

- [ ] **Step 3: Add hook tests to `scripts/test.sh`**

Append after the existing unittest line:

```bash
python3 -m unittest tests.test_hook -v
```

- [ ] **Step 4: README v2 section**

In `README.md`, after the `## Configuration model` section, insert:

```markdown
## Engagement ledger (v2)

festack keeps per-engagement state under `$FESTACK_HOME/engagements/`: a one-page
`brief.md` of curated facts and an append-only `log.md` of receipts. Engagements
auto-create on first touch of a named account, go dormant automatically after 30 quiet
days, and archive through `/retro` when you declare an outcome. Resume always announces
which engagement it picked. `/handoff <engagement>` packages the ledger into one
snapshot you can paste to a colleague. Rules live in
`skills/festack/references/ledger-lifecycle.md`.

A last-look hook watches outward-facing sends (mail, Drive, Slack) made through agent
tools: it never blocks, prints one awareness line when an artifact ships unreviewed,
and appends an outbound receipt to the ledger. It acts only on positive evidence that
a send is external (outside-org recipient, shared/external channel); when it cannot
tell, it stays silent and writes nothing — internal traffic never generates noise.
Sends made outside agent tools are invisible to it by design; it is an
audit-and-awareness layer, not a guarantee. Claude Code wires it via the plugin's
`hooks/hooks.json`; Cursor users merge `hooks/cursor-hooks.json` into
`~/.cursor/hooks.json`.
```

- [ ] **Step 5: Validate + run everything**

```bash
claude plugin validate .
scripts/test.sh
```

Expected: validation passes; all tests green except remaining persona test (Task 8).

- [ ] **Step 6: Commit**

```bash
git add hooks scripts/test.sh README.md && git commit -m "feat: hook adapters, manifest wiring, README v2 section"
```

---

### Task 8: Lifecycle integration (/retro, setup-festack) + persona seat (/review-work)

**Files:**
- Modify: `skills/retro/SKILL.md`
- Modify: `skills/setup-festack/SKILL.md`
- Modify: `skills/review-work/SKILL.md`

- [ ] **Step 1: `/retro` close flow**

In `skills/retro/SKILL.md`, after its main workflow section, add:

```markdown
## Engagement close

When the FE declares an engagement outcome (won, lost, dropped), `/retro` is the
mandatory close step, per `festack/references/ledger-lifecycle.md`: read the full
ledger (brief.md head and annex, plus the whole log.md — the one time it is read
whole), distill lessons to the host's lesson store, stamp the outcome and date in
brief.md, move the folder to `engagements/archive/`, and remove the index row. On
Cursor, continual-learning mines transcripts passively; this close pass is the
authoritative harvester — do not duplicate lessons it already captured.
```

- [ ] **Step 2: `setup-festack` engagements dir**

In `skills/setup-festack/SKILL.md`, in its setup workflow, add one bullet where directories are prepared:

```
- Ensure `$FESTACK_HOME/engagements/` exists with an empty `ENGAGEMENTS.md` index (header row only). Mention once: pointing both hosts' `FESTACK_HOME` at one shared directory keeps engagements continuous across Cursor and Claude Code.
```

- [ ] **Step 3: `/review-work` persona seat**

In `skills/review-work/SKILL.md`, after the step that assembles the rubric (step 1 area), add:

```markdown
### Client-persona seat

When the active engagement's brief.md names a stakeholder persona and the draft
targets that stakeholder, replace the generic client-readiness lens on one panel seat
with the persona: the reviewer role-plays that named stakeholder. **Grounding
requirement:** first extract the draft's claim inventory (every factual claim a
skeptical reader could check) and pass it to the persona seat, which must flag the
claims that stakeholder would demand evidence for. Cultural and role framing is the
top layer only. No claim inventory, no persona seat: fall back to the generic
client-readiness lens — an ungrounded persona is cosplay and worse than absence.
```

- [ ] **Step 4: Run the remaining tests**

Run: `python3 -m unittest tests.test_contracts -q`
Expected: OK (all LedgerV2ContractTests pass now).

- [ ] **Step 5: Commit**

```bash
git add skills/retro skills/setup-festack skills/review-work && git commit -m "feat: retro close flow, engagements setup, claim-grounded persona seat"
```

---

### Task 9: End-to-end smoke test (fixture engagement, fresh-window simulation)

**Files:** none (verification only; uses a temp FESTACK_HOME)

- [ ] **Step 1: Build a fixture engagement and exercise the hook end to end**

```bash
export SMOKE=$(mktemp -d)
mkdir -p "$SMOKE/engagements/petco-poc"
cat > "$SMOKE/engagements/ENGAGEMENTS.md" <<'EOF'
| slug | account | status | last-touched | next step | aliases |
| petco-poc | Petronas Trading | active | 2026-06-10 | review AE doc | petco, petronas |
EOF
printf '# brief\nStatus: active. Next: review AE doc.\n' > "$SMOKE/engagements/petco-poc/brief.md"
printf '2026-06-10 | /doc | artifact: ae-doc v3 | drafted\n' > "$SMOKE/engagements/petco-poc/log.md"
echo '{"text": "sending ae-doc to the AE", "channel": "gmail", "external": true}' | FESTACK_HOME="$SMOKE" python3 hooks/check_ledger.py
cat "$SMOKE/engagements/petco-poc/log.md"
```

Expected: stdout contains `last-look: no review on record for ae-doc — send is proceeding.`; log.md gained an `outbound ... review state at send: unreviewed` line; exit code 0.

- [ ] **Step 2: Dry-run the prose flows with subagents**

Dispatch one verification subagent that, against the same fixture `FESTACK_HOME`, simulates: (a) `/festack where were we on petco` → must announce "petco-poc (Petronas Trading)" before anything else; (b) `/handoff petco` → must produce a self-contained snapshot with a "what I'd do next Monday" section; (c) an ask matching two fixture engagements (add a second `petro-mlops` row first) → must hard-ask, not default. Report pass/fail per check.

- [ ] **Step 3: Final suite + validate + record**

```bash
scripts/test.sh && claude plugin validate . && git log --oneline claude-code-port..HEAD
```

Expected: all green; ~8 commits on `ledger-v2`. Report results to Casper; merge decision is his.
```

---

## Self-review (done at write time)

- Spec coverage: ledger layout/auto-create/resume/announce/collisions (Tasks 2-3), closeout writes + fast lane (Task 4), /handoff (Task 5), last-look hook + audit + fail-open + adapters (Tasks 6-7), lifecycle auto-dormant/retro/compaction rules (Tasks 2, 8), claim-grounded persona (Task 8), fresh-window smoke (Task 9). Non-goals respected: no blocking exits anywhere, no schedulers, no sync.
- No placeholders: every step carries full content or exact commands.
- Consistency: receipt grammar (`artifact: <name> v<N>`, `reviewed:`, `outbound`) is identical in ledger-lifecycle.md (Task 2), the hook parser (Task 6), and the smoke fixture (Task 9).
