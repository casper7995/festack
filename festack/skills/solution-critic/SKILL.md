---
name: solution-critic
description: Run a multi-model design debate to compare approaches and converge on one recommended architecture or plan.
disable-model-invocation: true
---

# /solution-critic

Design the approach, not the picture. This is the reasoning step that decides how to solve a client problem before anyone builds anything. It runs a multi-model debate, converges on one recommendation, and surfaces the real decisions for the human.

Visual artifacts are `/diagram`. The build is `/demo`, or `/autopilot` for an approved scope. This skill produces the design.

## Workflow

Open with this todolist and work it in order.

```
- [ ] 1. Read references/decision-gates from the festack-debate skill, and read the host's model-role config plus `$FESTACK_HOME/profile.md` if present
- [ ] 2. Frame the design question
- [ ] 3. Run festack-debate synthesize
- [ ] 4. Gate the open forks
- [ ] 5. Render the design in a canvas
- [ ] 6. Hand off
```

### 1. Read the ground

Read the decision-gate convention in the `festack-debate` skill (`references/decision-gates.md`). Read the host's model-role config for the panel models. Read `$FESTACK_HOME/profile.md` if it exists for the client and stack context. Resolve observable context from these. Do not ask the human what the profile already answers.

### 2. Frame the design question

State the one question the panel will answer, the inputs they get, and the decision criteria (feasibility, fit to the client goal, path to production, or whatever the engagement demands). If a required input is missing and is not observable, gate on it now before spending the panel. A vague frame produces vague candidates.

For product or architecture option decisions, gather the minimum frame before the panel: workload shape, source and target systems, latency or freshness requirement, transformation complexity, data quality or governance requirements, operational owner, integration constraints, success criteria, and any hard "must use" or "must avoid" tools. Ask only for the missing inputs that materially change the recommendation.

### 3. Run festack-debate synthesize

Invoke the `festack-debate` skill in synthesize mode with the framed question and context. It fans out the runner panel with a distinct adversarial lens per runner, across diverse model families where the host offers more than one, and merges the candidates into one package with a recorded decision and the strongest dissent kept visible. Do not average. Do not skip the dissent.

If the current execution context cannot launch Task/subagent workers, do not silently degrade or run a fake single-model panel. Return a parent-action gate with the framed question, context, decision criteria, expected synthesize mode, model role, and required `festack-debate` mode so the parent can run the panel from a context that supports fan-out. If the question is trivial enough to skip the panel, say why and answer directly.

### 4. Gate the open forks

Take the open forks from the synthesis. Classify each (observable, reversible, or genuine) per the decision-gate convention. Resolve observable forks yourself. Pick sensible defaults for reversible ones and say so. Use `AskQuestion` only for genuine product, stakeholder, scope, or preference calls, with the trade-off attached and one option recommended.

Use `allow_multiple: true` for additive gates such as stakeholders to optimize for, constraints to honor, risks to accept, requirements to prioritize, or components to include. Use single-select for the primary recommendation or any fork where exactly one approach must win.

### 5. Render the design in a canvas

Render the converged design as a structured canvas following the `canvas` skill. Show the recommendation, the key choices, the rejected paths with reasons, the open decisions, and the risks to watch. Canvas is the default surface. A design the team cannot see together is half a design.

When composed by `/scope-and-align`, `/demo`, `/diagram`, or `festack-delivery-agent`, return the structured design package and skip the canvas unless the caller asks for it. The deliverable owner renders the final visual surface.

For a trivial design call with one obvious approach and no meaningful rejected paths, answer in prose and offer the canvas instead of forcing one.

### 6. Hand off

State what is decided and what is still open. If the caller was `/scope-and-align`, `/demo`, or `/diagram`, return the design package to it. If the human invoked this directly, offer the next step (review the design with `/review-work`, build it with `/demo`, or draw it with `/diagram` when that ships).

## Notes

- Use the panel where alternatives genuinely change the answer. For a near-trivial design call, resolve it single-model and say why a panel was not warranted.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
