---
name: demo
description: Design a customer demo before build: spine, story, aha moment, run of show, risks, and reviewed blueprint.
disable-model-invocation: true
---

# /demo

The flagship. A good demo is designed before it is built. This skill produces the design: the spine, the story, the run of show, the asset blueprint, the failure plan. It debates the approach across models, gates the real decisions with you, and renders the result so the team shares one picture before a single asset is built.

Hard rule: design before build. Do not write asset code until the blueprint is reviewed and you approve the build.

End-to-end build is allowed only through adapters the profile or current host actually provides. Keep the core skill vendor-neutral: detect the builder, validate setup and auth, build, verify, export, and hand off. If no builder adapter exists, stop at a build-ready blueprint instead of pretending the assets can be produced.

## Workflow

Open with this todolist and work it in order.

```
- [ ] 1. Read the ground: demo rubric, decision-gates, models, profile, and any alignment brief
- [ ] 2. Establish the demo spine
- [ ] 3. Debate the approach with /solution-critic
- [ ] 4. Gate the genuine decisions
- [ ] 5. Build the demo blueprint and run of show
- [ ] 6. Stress it with /review-work against the demo rubric
- [ ] 7. Render in canvas and docs-canvas
- [ ] 8. Gate the build
```

### 1. Read the ground

Read the demo rubric in the `review-work` skill (`references/deliverable-rubrics.md`, demo section) so you design against the bar you will be reviewed against. Read the decision-gate convention in the `festack-debate` skill (`references/decision-gates.md`). Read the host's model-role config for panel models and `$FESTACK_HOME/profile.md` for client, stack, and output preferences. If an alignment brief exists from `/scope-and-align`, read it and inherit the Goal, Audience, Success criteria, Belief to change, Judges, Decision unblocked, and Hard constraints. Apply upstream brief inheritance: when the brief or prior context already settled the goal, audience, success criteria, primary belief, judges, decision unblocked, or hard constraints, treat them as observable and do not re-ask. If there is no upstream brief and the demo-critical pieces are missing, run a compressed alignment on just those (audience, the one belief, the success signal) before designing. When you can draft the spine with a stated candidate belief, hold these alignment questions and batch them with the step 4 gate in one call instead of interrupting twice.

A demo is competitive when it makes claims about a named competitor or will be scored against one. Positioning context alone (a competitor demoed first, the client mentioned another vendor) does not make it competitive. If the demo is competitive, read or run `/compete` before locking the demo spine. Competitive demo claims must be fair, scoped to the customer's use case, and cited. Do not build a demo around an absolute "we are better" claim; turn it into specific proof points and state the competitor's real strengths.

### 2. Establish the demo spine

Fill the spine from [references/demo-blueprint.md](references/demo-blueprint.md): audience and split, the one belief, the aha moment, and the constraints (time slot, live or recorded, their data or synthetic, environment). Resolve what the profile and brief already answer. If you cannot state the one belief in a sentence, the demo is not ready to design. Surface that, do not paper over it.

### 3. Debate the approach with /solution-critic

The demo approach is a real fork: which scenario, depth vs breadth, the asset structure, what to show live vs narrate. Invoke `/solution-critic` to run the multi-model debate on the spine and converge on one recommended approach with the dissent kept visible. For a trivial demo with one obvious shape, name it and skip the panel.

### 4. Gate the genuine decisions

Take the open forks from the design. Classify each per the decision-gate convention. Resolve observable ones, including anything the profile, the alignment brief, the stated constraints, or the calendar invite already answer; the time slot is observable when an invite exists, so check before asking. Pick defaults for reversible ones and say so. Use `AskQuestion` only for genuine calls a human owns that are still unanswered: audience level, which scenario, live vs recorded, the data source when it is not already set. Attach the trade-off and recommend one. FE demos live or die on these calls, so make the real ones explicit and do not re-ask the settled ones. Defer "what to cut to fit the slot" until after step 5; you cannot choose cuts before the run of show exists.

Use `allow_multiple: true` for additive demo choices: audience segments, assets to include, story beats to cut, risks to plan around, fallback paths, or success signals. Use single-select for mutually exclusive calls: scenario, live vs recorded, primary data source, or build/revise/stop.

### 5. Build the demo blueprint and run of show

Fill the rest of the blueprint: story arc in 3 to 5 beats, the minute-by-minute run of show with a fallback per beat, the asset map with per-asset section outlines (for a notebook, the markdown narration plan and each cell's purpose), data and environment and setup, determinism freezes, the impact number with baseline and source, and the path to production. The demo must read as a story, not a feature tour. If the run of show overflows the slot, gate "what to cut" now, with the over-stuffed version visible so the human chooses among real beats.

### 6. Stress it with /review-work

Invoke `/review-work` with the demo rubric to red-team the blueprint. Pay attention to the time box, the live-failure fallback, determinism, the audience split, and the defended impact number. Loop fixes until there are no blockers and no majors, capped at two fix rounds; after two rounds, stop and either ship with the remaining majors named as accepted residual risk or escalate the stubborn findings to the human.

### 7. Render in canvas and docs-canvas

Render two surfaces using the host's canvas tooling when present (the `canvas` and `docs-canvas` skills in Cursor); on hosts without it, render the same two surfaces as Markdown, in chat or as files, and ask before creating local files.

- **Canvas.** The demo at a glance: spine, story arc, the aha moment, key decisions, risks. The shared picture the team aligns on.
- **Docs-canvas.** The full blueprint and run of show as a navigable runbook the presenter and builders work from.

The shared-understanding artifact is not optional here. The whole point is shared understanding before build. On hosts without a canvas tool, render the same two surfaces as written Markdown or HTML artifacts.

### 8. Gate the build

State what is decided and what is still open. Confirm the blueprint passed review. Then gate the build with one explicit `AskQuestion`: build now, revise the blueprint first, or stop. This is an irreversible, expensive fork, so make it a structured decision, not a passing "ok to build?".

Only after build approval, choose the build path:

- **Adapter present:** hand the approved artifact or blueprint, asset list or phase list, acceptance checks, target environment, build adapter, deploy/export target, review status, and rollback or failure evidence expectations to `/autopilot`. It can build end to end only after validating the adapter.
- **No adapter present:** return a build-ready spec and name the missing adapter or tool. Ask before creating local files.

Do not start building before this gate.

## Notes

- Design before build is the whole value. A reviewed blueprint prevents the most expensive demo failures, which happen in the room.
- Use the panel where the approach genuinely has alternatives. Do not spend it on a demo with one obvious shape.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
