---
name: scope-and-align
description: Align an engagement around goals, success criteria, audience, risks, requirements, and the winning deliverable.
disable-model-invocation: true
---

# /scope-and-align

The alignment step before any deliverable. It is Socratic on purpose. It asks until the engagement is clear, then writes the brief and renders the canvas. It does not let the work start on a fuzzy scope.

This is the heavyweight front door for an engagement. For a narrow ask, the human can skip it and call a primitive or a builder directly. When it runs, it runs to alignment.

## Workflow

Open with this todolist and work it in order.

```
- [ ] 1. Read references/alignment-checklist.md, the decision-gate convention, the profile, and the models
- [ ] 2. Inventory what is known vs missing across the alignment checklist
- [ ] 3. Run the Socratic loop until every required piece is present and sharp
- [ ] 4. Debate the winning deliverable with /solution-critic where alternatives are real
- [ ] 5. Draft the brief, then stress it with /review-work using the alignment-brief rubric
- [ ] 6. Write the brief and render the alignment canvas
- [ ] 7. Confirm the exit contract
```

### 1. Read the ground

Read [references/alignment-checklist.md](references/alignment-checklist.md) for the required pieces and the bar for each. Read the decision-gate convention in the `festack-debate` skill (`references/decision-gates.md`). Read `$FESTACK_HOME/profile.md` if present for client, stack, resources, tone, and output preferences. Read the host's model-role config for panel models.

### 2. Inventory

Fill the alignment checklist from the request, the profile, and the prior conversation. Mark each piece present, vague, or missing. Resolve observable gaps yourself before asking the human anything.

### 3. Socratic loop

Drive the gaps to closure. For each missing or vague piece, classify the fork per the decision-gate convention. Resolve observable ones. Pick defaults for reversible ones and say so. Use `AskQuestion` for genuine business, stakeholder, scope, audience, or preference calls, batching related decisions and attaching the trade-off. Do not move on while a required piece is still vague. State plainly what is still blocking alignment.

Use multiple selection when the answer is naturally a set: stakeholders in the room, audiences to win, requirements, constraints, risks, success criteria, or possible deliverables to compare. Use single selection for the primary goal, the winning deliverable, and any one-default decision.

### 4. Debate the deliverable

The winning deliverable is the highest-value fork. Where there are real alternatives (a demo vs a doc vs a diagram vs a POC, or competing approaches), invoke `/solution-critic` to run the multi-model debate and converge. Where the deliverable is obvious, name it and move on without a panel.

### 5. Draft and stress

Draft the brief using [references/brief-template.md](references/brief-template.md). Then invoke `/review-work` with the alignment-brief rubric to stress it. Loop fixes until there are no blockers and no majors. The brief is a client-credible artifact, not internal notes.

### 6. Write the brief and render the canvas

Write the brief in two forms.

- **Written brief.** If the profile declares a document target and the matching document skill is available, create the brief there and return the link. The target and the writer are whatever the profile declares; this skill names none. If no document target is available, ask before creating local markdown; otherwise return the brief in chat and the canvas as the durable artifact.
- **Canvas.** Render a structured alignment canvas following the `canvas` skill. One section per checklist piece, plus Decided and Open decisions. This is the shared picture the team aligns on.

### 7. Exit contract

Exit only when all of these hold. State the check explicitly before you finish.

- Every required checklist piece is present and sharp.
- Success criteria are measurable, not sentiment.
- The winning deliverable is chosen, with one line on why.
- No open blockers remain. Remaining open items are genuine decisions with a named owner.

If any fails, you are not done. Say what is missing and keep going.

## Notes

- Alignment is the product here. A fast, fuzzy brief is worse than a slower sharp one.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
