---
name: problem-frame
description: Structure a fuzzy client problem into pain, sub-problems, constraints, stakeholders, unknowns, and a canvas.
disable-model-invocation: true
---

# /problem-frame

Understand the problem before solving it. This is the structure-first primitive. It turns a fuzzy client ask into a clear problem statement, a decomposition, and the named unknowns. It does not design the approach. That is `/solution-critic`.

## What this is not

- Not the design debate. Hand the structured problem to `/solution-critic` for the approach.
- Not deep research. For heavy research, use the profile-declared knowledge sources and whatever connector skills are available. If the profile names no source, ask which source families to use with `allow_multiple: true`. Delegate to `/discovery` for broad research and `/client-debug` for a specific question. Do light, targeted lookups only.

## Workflow

Open with this todolist.

```
- [ ] 1. Read the decision-gate convention and the profile
- [ ] 2. Clarify the real problem
- [ ] 3. Structure it
- [ ] 4. Light research only
- [ ] 5. Render the structure in a canvas
- [ ] 6. Hand off
```

### 1. Read the ground

Read the decision-gate convention and shared research discipline in the `festack-debate` skill (`references/decision-gates.md` and `references/research-method.md`). Read `$FESTACK_HOME/profile.md` if it exists. Resolve observable context from it.

### 2. Clarify the real problem

Separate the stated ask from the underlying problem. Clients often ask for a solution, not the problem. Use `AskQuestion` for genuine unknowns (the actual pain, the audience, the constraint that matters). Resolve observable facts yourself. Refuse to proceed while the core problem is still unclear.

Use `allow_multiple: true` for additive problem-framing answers such as audiences, stakeholders, constraints, sub-problems, unknowns, or priorities. Use single-select only when one primary pain, one primary audience, or one governing constraint must be chosen.

### 3. Structure it

Decompose into:

- The core problem in one sentence.
- Sub-problems, in priority order.
- Hard constraints (platform, data, regulatory, time, budget).
- Stakeholders and what each needs to see.
- Unknowns, marked as unknown, with what would resolve each.

### 4. Light research only

Do targeted lookups to fill small gaps. If the gap is large, name it and recommend dedicated research (`/discovery` for a broad picture, `/client-debug` for a specific question) rather than doing deep research here. Stay structure-first.

Apply the research discipline whenever you do look something up:

- Cite every claim. A claim with no source is a guess, mark it as one.
- Weight sources by authority and recency. A current authoritative source beats an old informal one.
- Separate what you are confident about from what you are not, and from what you could not determine.
- Rate confidence plainly (high, medium, low) with the reason. Do not present a low-confidence answer as settled.

### 5. Render the structure in a canvas

Render the structured understanding as a canvas following the `canvas` skill. Problem, sub-problems, constraints, stakeholders, unknowns. This is the shared artifact the engagement reasons from.

When composed by `/scope-and-align`, `/solution-critic`, `/diagram`, `/demo`, or `festack-delivery-agent`, return a structured problem package and skip the canvas unless the caller asks for it. The deliverable owner renders the final visual surface.

For a trivial one-line framing where there are no meaningful sub-problems, stakeholders, or unknowns to inspect, keep the answer in prose and offer the canvas rather than forcing one.

### 6. Hand off

State what is understood and what is still unknown. Offer the next step: design the approach with `/solution-critic`, align the full engagement with `/scope-and-align`, or research the gaps with `/discovery` or `/client-debug`.

## Notes

- Resist jumping to a solution. The value here is a clean problem.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
