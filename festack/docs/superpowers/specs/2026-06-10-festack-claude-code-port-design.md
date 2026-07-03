# festack Claude Code port — design

Date: 2026-06-10
Status: approved (Casper, in-session)

## Context

festack is a vendor-neutral SA/FE workflow plugin built for Cursor. Its core engine
(`festack-debate`) fans work out across multiple model *families* (GPT, Claude, Composer)
because cross-family disagreement is the quality signal. Claude Code is a single-provider
host: every subagent runs a Claude model, and the session model (Fable) is inherited by
default. This port makes the same plugin first-class on Claude Code without forking it.

The repo already ships `.claude-plugin/plugin.json`, `marketplace.json`, and
`install.sh claude`. Skills use the standard `<name>/SKILL.md` format both hosts read.
What remains is the model layer and a thin host-adaptation pass.

## Decisions (settled with Casper)

1. **Panel diversity**: persona/lens diversity replaces model-family diversity.
   Runners and reviewers each get a distinct named lens.
2. **Repo shape**: one source tree, host-adaptive skills. No `claude/` overlay, no fork.
3. **Install path**: proper Claude Code plugin via `/plugin marketplace add` +
   `/plugin install`. `install.sh claude` stays as the fallback for locked-down setups.
4. **Model placement principle**: *anything that exercises judgment or produces what the
   client sees runs Fable; parallel exploration runs opus; high-frequency checks run haiku.*

## Model roles on Claude Code

Written by `/setup-models` to `~/.claude/festack/models.md` (never `CLAUDE.md`):

| Role | Model | Rationale |
| --- | --- | --- |
| `debate-runners` | `opus` ×3, one lens each | Disposable exploration; candidates are merged then discarded |
| `review-reviewers` | `opus` ×3, one lens each | Adversarial critique feeding the judge |
| `synthesizer` | `fable` (explicit pin) | Judgment + final prose — what actually ships |
| `evaluator` | `haiku` | Done/not-done checks at phase boundaries, high frequency |
| `classifier` | `haiku` | Cheapest triage |

Orchestration (`/festack`, `festack-delivery-agent`, `/autopilot` main loop) runs in the
main session and therefore inherits Fable naturally.

Notes:

- Model aliases (`opus`, `fable`, `haiku`), not dated slugs. Claude Code resolves aliases
  to current models, so configs do not go stale the way Cursor slugs do.
- The model pin travels in the per-`Task` call, driven by the role line in `models.md`.
  `festack-agent.md` frontmatter stays model-agnostic because the same worker serves
  opus runner jobs and haiku evaluator jobs.
- Cursor behavior is unchanged: `festack-models.mdc`, Cursor slugs, family diversity.

## Lenses

New file `skills/festack-debate/references/lenses.md`:

- Runner lenses: **risk-first skeptic**, **pragmatist / MVP-first**, **customer-advocate**.
- Reviewer lenses: **correctness**, **client-readiness**, **feasibility**.

Engine fan-out rule changes from "different model per runner" to "**different lens per
runner; different model family too when the host offers one**" — one instruction valid on
both hosts. Panel size guidance (default 3, 2 narrow, 4 high-stakes) is unchanged.

The **Panel attestation** block gains a `lens` field (`lenses:` line listing the lens per
worker) so callers can verify diversity actually happened on single-provider hosts.

## Host adaptations

- **AskQuestion alias (25 files reference it)**: define once in
  `skills/festack-debate/references/decision-gates.md` — "AskQuestion means the host's
  gate tool: `AskQuestion` in Cursor, `AskUserQuestion` in Claude Code." No per-file
  rewrite; skills are prompts, and one authoritative definition resolves the term.
- **`festack-models.mdc` references (7 files)**: replace the hardcoded path with "the
  host's model config" plus the per-host table (Cursor `~/.cursor/rules/festack-models.mdc`,
  Claude Code `~/.claude/festack/models.md`, Codex `AGENTS.md`/`config.toml`). Pattern
  already exists in `festack-delivery-agent` Step 0; this makes it consistent everywhere,
  including updating Step 0 itself from "CLAUDE.md or host-supported project guidance"
  to the concrete `~/.claude/festack/models.md` path.
- **`subagent_type: "festack:festack-agent"`**: already correct — that is exactly how
  Claude Code namespaces plugin agents. No change.
- **Canvas (26 files)**: the markdown/HTML fallback is already the documented behavior.
  Spot-check each skill states the fallback; fix stragglers only.
- **`setup-models` SKILL.md**: becomes host-aware. Detect host, present the right role
  table (Cursor slugs vs Claude aliases), write the right file, and state the placement
  principle (judgment→fable, exploration→opus, frequent checks→haiku) so future roles
  follow it without per-role debate.
- **`autopilot` (SKILL.md + references/autopilot-loop.md)** and
  **`decision-gates.md`**: replace inline Cursor slug mentions with role names resolved
  from the host model config.

## Packaging

- Validate `.claude-plugin/plugin.json` against the current plugin schema
  (plugin-builder guide). Keep `skills/` and `agents/` pointers.
- README: add a "Claude Code (recommended)" install section —
  `/plugin marketplace add ~/Projects/festack` then `/plugin install festack` — and keep
  `scripts/install.sh claude --copy` as the documented fallback. Update the Portability
  table: model config cell for Claude Code becomes `~/.claude/festack/models.md`.

## Verification

- Extend `tests/test_contracts.py`:
  - no Cursor model slugs outside `setup-models` and the `festack-debate` fallback table;
  - the AskUserQuestion alias exists in `decision-gates.md`;
  - `lenses.md` exists and is referenced by the engine;
  - Claude role defaults (`opus`/`fable`/`haiku`) appear in `setup-models`.
- `scripts/test.sh`, `bash -n` on install scripts, `scripts/verify-install.sh`.
- Live smoke test in Claude Code: install the plugin, run `/festack` routing, run one
  `festack-debate` critique pass and confirm the Panel attestation reports 3 opus
  workers with distinct lenses and a fable synthesizer.

## Out of scope

- Codex changes beyond what falls out of host-neutral wording.
- New playbooks or capabilities; canvas tooling for Claude Code.
- Any change to the Cursor install path or Cursor model defaults.
