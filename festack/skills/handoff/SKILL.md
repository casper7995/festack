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
   recent receipts in log.md (compacted view; do not dump the raw log). Derive open
   gates from recent receipts too, not only the decisions section; a question raised on
   a logged call is an open gate. Mark receipt-derived gates as derived.
3. **Compose the snapshot** as one self-contained Markdown block:
   - A **coverage line first**: "last receipt: <age>; <N> receipts since the last
     compaction summary (or all receipts when none exists). The ledger may not reflect
     untracked work (calls, hallway Slack, customer files)."
     Frame "what I'd do next Monday" as derived from the ledger, not asserted. A
     confident hollow snapshot is worse than a writeup that knows what it doesn't know.
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

## Round-trip format

Keep the snapshot's section headings stable and machine-recognizable: use the exact
brief.md section names (Status and next step; Brief; Live decisions and gate answers;
Stakeholder personas; Accepted residual risks) plus "Recent activity" and "What I'd do
next Monday". A colleague's festack must be able to rebuild a ledger from this snapshot
without guessing; the snapshot is designed for round-trip even though the import verb
ships later. Never rename or merge these sections for style.

## Prose

All output follows the `fe-deslop` skill. The snapshot must stand alone: no references
to "above", "this chat", or files the reader cannot open.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: prose snapshot, owner: the FE who pastes it.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
