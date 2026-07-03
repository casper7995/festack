# festack engagement ledger v2 — design (final)

Date: 2026-06-10
Status: approved scope (Casper), incorporating APJ Cursor FE persona review (no-go on v1
spec; this revision adopts the re-scope). Supersedes the draft of the same date.

## Problem

festack is stateless prose. Every quality guarantee (panels, gates, receipts) is an
instruction emitted into a conversation and gone when the session ends. Real FE work is
a multi-week engagement run from fresh context windows, often across two hosts and,
during travel, across two people. Three evaluations (two dry-run panels, one cold
reviewer at 7/10) plus an APJ field persona review converged: ceremony repeated per
task, receipts that evaporate, no engagement memory, no handoff, and enforcement bets
that real FEs would disable.

## Design principles

1. **Fresh context is the core assumption.** Every session starts cold. All durable
   knowledge lives in files; the conversation is a scratchpad. Rehydration is one file
   read (~1 page).
2. **Code only where prose provably fails: state and awareness.** Never script the
   judgment. No blocking enforcement — the persona review showed a blocking gate guards
   the wrong door (FEs ship risky content outside agent tools) and dies at the first
   false block.
3. **Zero decisions, zero ceremony, zero memorization for the FE.** Auto-create,
   auto-dormant, alias matching. Anything that requires the FE to remember, name, file,
   or decide housekeeping will be deferred forever and must not exist.
4. **Adoption is measured on `/handoff`, not on ledgers existing.** The first time an FE
   sends a handoff snapshot to a colleague unprompted is the success signal.

## 1. Engagement ledger

Layout under `$FESTACK_HOME/engagements/` (host-neutral: Cursor `~/.cursor/festack`,
Claude Code `~/.claude/festack`; pointing both hosts' `FESTACK_HOME` at one directory is
recommended and documented — it solves cross-host, not cross-person):

```
engagements/
  ENGAGEMENTS.md          # index: slug | account | status | last-touched | next step | aliases
  <slug>/
    brief.md              # TIER 1: curated facts (head + annex, see caps below)
    log.md                # TIER 2: append-only receipts; never bulk-loaded
  archive/<slug>/         # closed engagements, moved whole; never indexed for resume
```

### brief.md structure (resolves the v1 cap contradiction)

- **Head (capped ~1 page): the only part resume loads.** Current status, next step,
  engagement brief (goal, audience, timeline, playbook), live decisions, active
  stakeholder personas, accepted residual risks.
- **Annex (same file, below a marker): read on demand, never auto-loaded.** Superseded
  decisions with dates, full gate-answer history, extended persona notes.
- Facts are superseded in place (dated marker, old value moves to annex), never
  duplicated and never compacted away. The head cap is enforced by moving aged facts to
  the annex, not by deleting them.

### log.md

One receipt per skill completion: 3-5 schema-shaped lines (date, skill, artifact +
version when relevant, outcome, attestation summary when a panel ran, outbound sends).
Prose dumps and transcript excerpts are forbidden input formats. Compaction summaries at
top, raw receipts below.

### Auto-create (no ceremony)

The first time any festack skill runs **with a named account as the subject of the
work** and no matching engagement exists, the model proposes a slug inline ("creating
`dbs-sg-eval` — ok?"), the FE can override in the same breath, work continues. One
inline confirm, zero ceremony — never fully silent creation, and never from a passing
mention ("like we did for DBS" while working another account resolves against existing
engagements or nothing). No setup flow, no separate command. Generic/unnamed work runs
stateless exactly as today; no ledger is forced.

### Writes

The shared closeout-receipt convention gains one line: append the receipt to the active
engagement's `log.md`. A normal file-append by the agent (not a hook), once per skill
completion. Fast-lane narrow asks append one line and pay no other ceremony.

## 2. Resume and routing (fresh-window UX)

Three doors, no flags to memorize:

1. **Inference (normal path).** `/festack <anything mentioning the account>` matches
   account names and aliases from the index — never slugs-only, FEs think in account
   names. **Resume always announces its pick first**: "**dbs-sg-eval (DBS Bank
   Singapore)** — resuming. Last activity: … Next step: …" so a wrong pick is caught at
   a glance. **Name-stem collisions hard-ask** (DBS / DBS HK / DBS Securities): never
   silently default when more than one engagement matches.
2. **Bare `/festack`** → index view of active engagements, one line each with next
   steps, **always ending with a dormant-count line** ("dormant: 4 — oldest quiet 47d:
   `lotte-eval`") so the Monday-morning screen never shows a clean board when it isn't
   one. Quiet engagements are dimmed, never invisible.
3. **Explicit `/festack resume <slug>`** → fallback for certainty and scripts.

Resume loads the `brief.md` head only. The v1 Step 0 multi-file ceremony runs once per
engagement at creation; its outputs live in the brief thereafter. A "single active
engagement defaults silently" rule is explicitly NOT adopted (dead code for multi-eval
FEs, dangerous for everyone else); with one engagement, inference trivially matches it
and still announces.

## 3. Lifecycle (fully automatic, no nags)

- **Statuses: active → dormant → closed(won/lost/dropped) → archived.**
- **Auto-dormant:** untouched 30 days → status flips to `dormant` automatically. Drops
  out of the default index view (visible under "dormant" section), stays fully
  resumable; resuming flips it back to active. Quiet is neutral, not a death signal —
  no close/keep question is ever asked.
- **Close** happens only when the FE declares an outcome. Then `/retro` reads the full
  ledger (the one time `log.md` is read whole), distills lessons to the host's lesson
  store, stamps the outcome, moves the folder to `archive/`. Retro-before-archive is
  mandatory ordering. On Cursor, continual-learning keeps mining transcripts passively;
  `/retro` is the authoritative engagement-close harvester (stated in prose to avoid
  duplicate lessons).
- **Compaction** (observable triggers only: `log.md` exceeds 40 raw receipts, or the
  brief head exceeds its cap; executed at the next resume): collapse the oldest
  receipts into a dated summary block, delete the raw lines. Pinned exception: receipts
  for artifact versions not yet sent stay until sent or superseded (the last-look hook
  reads them).
- Maintenance happens only at touchpoints the agent already occupies (resume, close).
  No daemon, no scheduler, no background process. Escape hatch: plain Markdown,
  user-editable, deletable, git-able.
- **Privacy note (documented in ledger-lifecycle.md):** outbound receipts are a
  plaintext local record of what was sent to which customer. A shared `FESTACK_HOME`
  must live on storage the FE controls; do not place it on a synced/shared drive
  without considering who can read it — the likeliest adopters are exactly the people
  handling bank InfoSec reviews.

## 4. /handoff (the adoption engine)

`/handoff <engagement>` (inference rules as resume) emits one self-contained snapshot
formatted for a human colleague: account + status, the brief, decisions and open gates,
accepted risks, last-N receipts (compacted view), stakeholder personas, and a "what I'd
do next Monday" section derived from the playbook position. Output is a single Markdown
block ready to paste into Slack/Notion/a doc — festack does not send it anywhere itself.
Optional argument for audience ("for my AE" trims internals; default is FE-to-FE full
fidelity). This is a read-and-format skill over existing ledger data; no new state.

**Coverage honesty (required):** the snapshot always carries a freshness/coverage line
("last receipt: 9 days ago; 6 receipts this phase — ledger may not reflect untracked
work") and frames "what I'd do next Monday" as derived from the ledger, not asserted.
Ledgers are systematically incomplete (calls, hallway Slack, customer spreadsheets
never pass through skills); a confident hollow snapshot is worse than a manual writeup
that knows what it doesn't know.

## 5. Last-look hook (awareness, never enforcement)

One shared core script + two thin host adapters, shipped in the plugin:

- Fires only on outward-facing agent tool calls (mail send, Drive upload, Slack post).
- **Never blocks.** Emits at most one line of awareness when the ledger shows risk:
  "this references doc-v2 — last reviewed 6 days and 2 edits ago" or "no review on
  record for this artifact." The FE proceeds by doing nothing differently.
- **Always appends an outbound receipt** to `log.md` (what was sent, where, review state
  at send time). This audit trail is the hook's primary value: it feeds `/retro`,
  `/handoff`, and any later quality review.
- Claude Code adapter: `PreToolUse` (non-blocking — observe, print, allow). Cursor
  adapter: `beforeMCPExecution`/`beforeShellExecution` equivalents.
- **Outward-detection rule:** the adapters mark a send external only on positive
  evidence — an email recipient outside the org domain, a Slack channel flagged
  shared/external, a Drive share outside the org. **When the adapter cannot tell, the
  hook stays silent and writes no receipt.** Internal traffic must never generate
  awareness lines or log noise; an awareness layer that cries on internal posts trains
  the FE to ignore it.
- Rules: outward actions only; fast (<100ms, pure file reads); fail-open and silent on
  any script error; identical behavior on both hosts. Known and accepted limitation
  (from the persona review): sends made outside agent tools (typing into a customer's
  sheet, pasting in the Slack app) are invisible to it; the hook is an audit-and-
  awareness layer, not a guarantee, and is documented as such.

## 6. Client-persona reviewer (claim-grounded)

- `brief.md` stakeholder section: who is in the room, what they care about, skepticism
  level. Populated by inference from conversation; gaps that matter are filled by one
  `AskQuestion`.
- `/review-work` gains an optional persona seat used when a persona exists and the
  deliverable targets that stakeholder. **Grounding requirement:** the persona seat is
  fed the deliverable's claim inventory (the factual claims extracted from the draft)
  and must flag which claims that stakeholder would demand evidence for, with the
  cultural/role framing as the top layer only. A persona seat without a claim inventory
  is not run (generic client-readiness lens applies instead) — cosplay is worse than
  absence.

## 7. Build order

1. Ledger + auto-create + announce-on-resume + collision hard-ask (foundation).
2. `/handoff` (adoption engine; cheap read-and-format).
3. Last-look hook (core + 2 adapters + outbound receipts).
4. Auto-dormant lifecycle + compaction.
5. Claim-grounded persona seat (depends on stakeholder section existing).

## 8. Changes inventory

Code (new): `hooks/check-ledger` core + Claude Code adapter + Cursor adapter, wired in
both plugin manifests. Tests: hook unit tests with fixture ledgers (warn, silent-pass,
outbound receipt written, fail-open), contract tests for ledger format references and
the no-blocking rule.

Prose (new): `skills/festack/references/ledger-lifecycle.md` (single authoritative
reference: format, tiers, head/annex, caps, supersede, compaction, statuses, close
flow); `skills/handoff/SKILL.md`; router resume/inference/index routing.

Prose (changed): closeout-receipt convention (append line + auto-create rule),
`/review-work` (persona seat + claim inventory), `/retro` (ledger close flow),
`/client-debug` + fast `/compete` (fast-lane line), `setup-festack` (engagements dir,
shared FESTACK_HOME note).

## Late additions (from the persona reviewer's 8-9 roadmap, approved by Casper)

- **Quick log**: `/festack log "<one sentence>"` captures out-of-band reality (calls,
  hallway Slack, customer files) as a `quick-log` receipt, supersedes contradicted
  brief facts, updates the next step when named. Fixes the sparse-ledger failure mode.
- **Round-trippable handoff format**: snapshot section headings mirror brief.md
  section names exactly so a colleague's festack can rebuild a ledger from a pasted
  snapshot. The import verb itself ships when a second user exists.
- **Index staleness marker**: next steps older than the latest receipt are flagged
  "(next step set Nd ago, M receipts since)".
- Deferred to v3 (deliberately, after v2 proves the ledger habit on a real
  engagement): security-questionnaire claim provenance (`claims.md` register with
  verified/asserted/superseded statuses), questionnaire-aware `/client-debug`, and the
  handoff import verb.

## Non-goals

No blocking enforcement anywhere. No team server, sync, or analytics; `/handoff` output
is pasted by the human. No transcript mining (continual-learning owns that on Cursor).
No deterministic panel scripts (cut in review). No modeling of security-questionnaire
claim provenance in v2 (named as the strongest v3 candidate from the persona review).
