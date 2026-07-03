---
name: learn
description: Capture feedback, observations, and retros as durable profile updates or reusable lessons.
disable-model-invocation: true
---

# /learn

Make festack better at your job over time. Every engagement teaches something; this skill is where that something stops being a passing thought and becomes guidance future skills will actually read.

## Step 0: read what exists

- Read `$FESTACK_HOME/profile.md` (stable preferences and context).
- Read `$FESTACK_HOME/lessons.md` if it exists (accumulated lessons). If it does not exist, create it on first write.
- Read `skills/learn/references/lessons-format.md` for the file shapes and the dedup rules. Follow them.

## Step 1: gather what there is to learn

The input can come from several places:

- **A `/retro`** handed off candidate lessons.
- **Direct feedback** the user gives you ("stop doing X", "I always want Y").
- **An observation** from the current session worth keeping.

Collect the raw material. If the user just said "remember this", capture the specific thing they mean, not a paraphrase that loses the point. When the lesson comes from a work session, read the record (the deliverables, decisions, errors, retries, and outcome) rather than relying on recall alone, and ask only for the judgment that the record does not show.

## Step 2: sort each item, profile or lesson

For every candidate, decide where it belongs, using the split in the format reference:

- **Stable fact or preference** about who you are, what you represent, how you like to work, your voice → **profile**. Example: "I always present to technical and economic buyers together."
- **Reusable lesson** learned from doing the work → **lessons file**. Example: "When a client says 'just show me', open the live demo before any slides."

If something is genuinely both, store the preference in the profile and the situational guidance in lessons, cross-referenced. Do not duplicate the same content in both.

## Step 3: dedup before writing

This is the step that keeps the files useful. For each item:

- Search the destination file for a near-match.
- If one exists, **merge** rather than append. Sharpen the existing entry with new evidence; keep one copy.
- If the same lesson has now arrived from three different engagements, **promote** it from a lesson to a profile default.
- If a new lesson contradicts an old one, **update or retire** the old one.

## Step 4: write it down

- Profile updates: edit `$FESTACK_HOME/profile.md` in place, preserving its schema. For voice or preference changes, keep them where `/personalize` put them so the structure stays coherent.
- Lessons: write to `$FESTACK_HOME/lessons.md` in the entry shape from the format reference, with a date.
- Run any prose you write through `fe-deslop`. Even private notes get the no-slop treatment so they stay readable.

## Step 5: confirm

Show the user, briefly, what changed: which items went to the profile, which to lessons, what was merged or promoted, what you chose not to keep and why. Learning the user disagrees with should be easy to reverse.

## Principles

- **Separate who-you-are from what-you-learned.** Profile for the first, lessons for the second.
- **Dedup or drown.** A file no one re-reads teaches nothing. Merge, promote, prune.
- **A lesson is reusable guidance.** If it will not change a future call, do not store it.
- **The user owns their memory.** Always show what changed; make it reversible.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
