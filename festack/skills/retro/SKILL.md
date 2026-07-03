---
name: retro
description: Run a retrospective on an engagement, deliverable, or session and extract durable lessons for /learn.
disable-model-invocation: true
---

# /retro

Turn an engagement, a deliverable, or a chunk of work into lessons you will actually reuse. The enemy of a useful retro is the tidy story that makes everyone feel fine and teaches nothing. Aim for the honest version.

## Step 0: read config and profile

- Read `$FESTACK_HOME/profile.md` for context and existing `$FESTACK_HOME/lessons.md` if present, so you do not re-derive lessons you already hold.
- Read the host's model-role config for model roles.

## Step 1: set the frame

Establish what you are reflecting on and what outcome it produced:

- **The thing.** A demo, a POC, a doc, a full engagement, a single hard session.
- **The outcome.** Won, lost, shipped, stalled, mixed. Be specific. "It went fine" is not an outcome.
- **The bar.** What were you trying to achieve, and did you hit it? Pull from the `/scope-and-align` brief or POC criteria if they exist.

## Step 2: walk the reflection

Lay down the timeline first, the sequence of events and the turning points, so the reflection sits on facts before it reaches conclusions. Then go through each, with specifics, not generalities:

- **What worked.** What would you deliberately do again? Name the move, not the vibe.
- **What did not.** Where did time leak, where did you guess wrong, what frustrated the client or you? This is the part people skip. Do not skip it.
- **Surprises.** What did you assume that turned out false? Assumptions that broke are the richest source of lessons.
- **Decisions to revisit.** Calls you made under uncertainty that you would reconsider with what you know now.
- **What the client taught you.** Signals, objections, or reactions worth remembering for next time.

For an engagement you lost or that stalled, be especially honest about the cause. A postmortem that blames the client or "timing" teaches nothing. Find the part you controlled.

## Step 3: extract candidate lessons

A lesson is durable, reusable guidance, not a one-off note. Test each candidate:

- **Durable:** would this apply to a future engagement, or is it specific to this one client and gone?
- **Actionable:** does it tell future-you what to do differently, not just what happened?
- **Honest:** does it survive the "would I actually follow this" test?

Phrase each as guidance: "When X, do Y, because Z." Drop anything that is just a feeling or a restatement of events.

It helps to sort candidates by surface area so you do not over-index on one: technical approach, process and communication, stakeholder alignment, expectation setting, decision quality, tooling or workflow, and preparation or readiness. For the lessons worth acting on, shape them as recommendations: the recommendation, who it is for, when to apply it, the evidence from this engagement, and the expected impact.

Optionally, for a high-stakes retro, run a `festack-debate` critique pass with `review-reviewers` over your draft lessons: which are real, which are rationalization, which are too narrow to keep?

## Step 4: render and hand off

- For a substantial retro (a full engagement, a lost deal, a team or client readout), render a canvas: outcome, what worked, what did not, surprises, and the candidate lessons. For a quick single-session reflection, a concise written summary is enough; do not force a canvas onto a five-minute retro.
- Run all prose through `fe-deslop`. Retros rot into corporate slop fast; keep it plain and specific.
- Hand the candidate lessons to `/learn`, which sorts them into your profile and lessons file and dedups against what is already there. Do not append to the lessons file directly from here; `/learn` owns that write so the dedup and promote rules always run.

## Engagement close

When the FE declares an engagement outcome (won, lost, dropped), `/retro` is the
mandatory close step, per `festack/references/ledger-lifecycle.md`: read the full
ledger (brief.md head and annex, plus the whole log.md, the one time it is read
whole), distill lessons to the host's lesson store, stamp the outcome and date in
brief.md, move the folder to `engagements/archive/`, and remove the index row. On
Cursor, continual-learning mines transcripts passively; this close pass is the
authoritative harvester. Do not duplicate lessons it already captured.

## Principles

- **The honest version teaches; the tidy version comforts.** Choose teaching.
- **A lesson is reusable guidance, not a diary entry.** If it will not change a future call, it is not a lesson.
- **Own the controllable.** Blaming externals ends the learning.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
