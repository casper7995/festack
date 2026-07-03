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

`$FESTACK_HOME` resolution (do this with a real shell check, not from memory):

1. Run `echo "$FESTACK_HOME"` in the host's shell. Non-empty value wins.
2. If unset, probe BOTH host defaults for an existing index:
   `~/.claude/festack/engagements/ENGAGEMENTS.md` and
   `~/.cursor/festack/engagements/ENGAGEMENTS.md`. Exactly one exists: use that root.
   Both exist: ask which is authoritative and recommend setting `FESTACK_HOME`.
3. Only when neither exists, use the current host's default.

Never create a new engagements root while the other host's default already holds one;
that splits the ledger across hosts, and auto-create against the empty root will
shadow real engagements with duplicate slugs. Pointing both hosts at one shared
directory via `FESTACK_HOME` is recommended; it solves cross-host continuity, not
cross-person sharing.

## Index line format (ENGAGEMENTS.md)

One Markdown table row per engagement:

```
| slug | account | status | last-touched | next step | aliases | step-set |
| dbs-sg-eval | DBS Bank Singapore | active | 2026-06-10 | review questionnaire v2 | dbs, dbs sg | 2026-06-08 |
```

Statuses: `active`, `dormant`, `closed-won`, `closed-lost`, `closed-dropped`. Archived
engagements are removed from this index entirely. `step-set` is the date the current
next step was written; whoever updates the next step updates it. It exists so the index
view can mark stale next steps without opening any log.md. When it is absent, skip the
staleness marker; never guess.

## Head and annex

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

## Receipt format

Append-only. One receipt per skill completion, one line, pipe-separated:

```
YYYY-MM-DD | <skill> | artifact: <name> v<N> | <outcome>
2026-06-10 | /doc | artifact: dbs-onepager v2 | drafted
2026-06-10 | /review-work | artifact: dbs-onepager v2 | reviewed: 0 blockers 0 majors | panel: 3 workers, lenses correctness/client-readiness/persona
2026-06-10 | /client-debug | RLS question answered, cited, high confidence
2026-06-10 | quick-log | call with DBS InfoSec, sub-processor answer accepted, SOC2 bridge letter due Fri
2026-06-10 | outbound | artifact: dbs-onepager v2 | sent via gmail | review state at send: reviewed
```

Omit the `artifact:` field when no artifact is involved. Prose dumps and transcript
excerpts are forbidden input formats. Compaction summaries sit at the top of the file;
raw receipts below.

## Quick log

Most engagement-state changes happen outside festack skills: calls, hallway Slack, a
customer's spreadsheet. `/festack log "<one sentence>"` captures them in five seconds:
append the sentence as a `quick-log` receipt to the active engagement (resume inference
rules apply, collisions hard-ask), supersede any brief.md fact the sentence contradicts,
and update the next step when the sentence names one. No other ceremony. A ledger that
only sees skill-driven work reflects festack usage, not the engagement; quick log is
how the ledger stays true.

## Auto-create

The first time any festack skill runs **with a named account as the subject of the
work** and no matching engagement exists: propose a slug inline ("creating
`dbs-sg-eval` -- ok?"), accept an override in the same breath, create the folder, the
index row, and a brief.md head seeded from the current context, then continue the
actual work. One inline confirm, zero ceremony. A passing mention of another account
("like we did for DBS" while working a different deal) never creates a ledger; it
resolves against existing engagements or nothing. No setup flow. Generic or unnamed
work runs stateless; never force a ledger.

## Resume

- Match the user's words against **account names and aliases** from the index, never
  slugs alone.
- **Always announce the pick first**: "**<slug> (<account>)** -- resuming. Last
  activity: <...>. Next step: <...>". A wrong pick must be catchable at a glance.
- **Name-stem collisions hard-ask.** If more than one engagement matches, ask; never
  silently default. There is no single-active silent default. Collision options carry
  each candidate's last activity and next step so a wrong pick is catchable; include a
  "neither, new engagement" option when the auto-create rules could apply.
- Load the brief.md head and the engagement's index line. Read the tail of log.md only
  when the announce line or the ask needs recent activity; never bulk-load the log.
  Resuming a `dormant` engagement flips it back to `active`.

## Statuses and transitions

- `active` -> `dormant`: automatic when last-touched is 30+ days ago, applied at the
  next index read. Dormant engagements drop to a separate section of the index view
  and stay fully resumable. Quiet is neutral; never ask whether to close.
- any -> `closed-*`: only when the user declares an outcome. Run `/retro` over the full
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
