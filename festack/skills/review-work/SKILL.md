---
name: review-work
description: Red-team a draft, doc, diagram, demo plan, or design package with adversarial reviewers and ranked fixes.
disable-model-invocation: true
---

# /review-work

Stress a draft toward client-ready. This is the adversarial pass that catches what one author misses. It runs several reviewers against a rubric, merges and ranks the findings, and optionally loops fixes until the draft holds.

Use the panel deliberately, not everywhere. Enterprise token cost is acceptable when the artifact is client-facing, high-stakes, contested, or likely to improve through adversarial critique. Low-stakes internal notes can stay single-model or skip this skill.

## Inputs

- The **draft** to review (a brief, a design package, a doc, a diagram, a demo plan).
- The **deliverable type**, which selects the rubric extension. If the caller does not name one, infer it from the draft and confirm with one quick `AskQuestion` only if genuinely ambiguous.

## Workflow

Open with this todolist.

```
- [ ] 1. Resolve festack-debate, load the base rubric and per-deliverable extension; read the host's model config
- [ ] 2. Run festack-debate critique
- [ ] 3. Report deduped, ranked findings
- [ ] 4. Offer the fix loop
```

### 1. Load the rubric

Resolve the `festack-debate` skill before loading rubrics. Keep this portable for plugin installs: do not hardcode user-machine-specific absolute paths or assume a particular host's skill directory layout. Do not rely on broad whole-home or glob-only searches; host installs may expose festack skills as symlinks, and those searches can miss symlinked skill directories even when direct reads work.

Use this lookup order:

1. Installed sibling skill: a directory named `festack-debate` in the same resolved host skill root as `review-work`; equivalently, `../festack-debate` relative to the resolved `review-work` skill directory.
2. Package/source fallback: if running from a plugin package or source checkout, locate the package root that contains `skills/review-work`, then read `skills/festack-debate` from that same root.
3. Caller-provided fallback: if the caller already resolved the `/festack` skill directory or package root, use that location rather than searching the user's home directory.
4. Only if all direct reads fail, report a parent-action gate with the exact relative roots attempted. Do not invent a rubric, do not continue with a single-model review, and do not describe the rubric as missing until the package/source fallback has been tried.

Load these files explicitly:

- Base rubric: `festack-debate/references/critique-rubric-base.md`
- Reviewer prompt: `festack-debate/references/reviewer-prompt.md`
- Decision gate convention when `AskQuestion` is used: `festack-debate/references/decision-gates.md`
- Per-deliverable rubric extension: `review-work/references/deliverable-rubrics.md`

Add the matching per-deliverable rubric to the base rubric. Read the host's model-role config for the reviewer panel.

### Client-persona seat

When the active engagement's brief.md names a stakeholder persona and the draft
targets that stakeholder, replace the generic client-readiness lens on one panel seat
with the persona: the reviewer role-plays that named stakeholder. **Grounding
requirement:** first extract the draft's claim inventory (every factual claim a
skeptical reader could check) and pass it to the persona seat, which must flag the
claims that stakeholder would demand evidence for. Cultural and role framing is the
top layer only. No claim inventory, no persona seat: fall back to the generic
client-readiness lens. An ungrounded persona is cosplay and worse than absence.

### 2. Run festack-debate critique

Invoke the `festack-debate` skill in critique mode with the draft and the combined rubric. It fans out the reviewer panel across diverse model families, then dedupes and ranks the findings. Findings that more than one reviewer raised are weighted higher.

Under the hood this means several `festack-agent` reviewer workers run in parallel from the `review-reviewers` model role, followed by one synthesis/ranking pass. Do not manually simulate the panel and do not silently degrade it to one model unless the host cannot spawn workers; if fan-out is blocked, return a parent-action gate with the draft, rubric, expected critique mode, model role, and reviewer prompt inputs.

### 3. Report

Lead with the findings, highest signal first. Group by severity (blocker, major, minor). Each finding carries evidence and one concrete fix. State what is already strong so the human knows what not to touch. Do not inflate severity.

When `/review-work` is invoked directly on a non-trivial draft, render the ranked findings as a canvas (the `canvas` skill): severity, finding, evidence, fix, plus what is already strong. A severity-grouped findings set is exactly the categorized result the canvas skill says to render rather than dump as a markdown table. When `/review-work` is composed mid-loop by another skill (`/demo`, `/doc`, `/diagram`, `/poc`, `/discovery`), return the findings to the caller and let it render, so you do not stack a redundant canvas inside someone else's flow.

### 4. Offer the fix loop

Offer to apply the fixes and re-review. Use a single-select `AskQuestion` when the next step is a real human choice, with these options:

- **Apply all blocker and major fixes.** Best default for client-facing work.
- **Fix blockers only and accept stated major risks.** Only valid when the user explicitly accepts the named residual risk.
- **Choose among competing fixes.** Use when two fixes trade off scope, tone, or claims.
- **Stop and keep the residual risk.** record the specific residual finding, why it remains, and who accepted it.

Stop when the draft has no blockers and no majors, or when the human says it is good enough with the residual risk recorded. Each round should visibly reduce the finding count, not churn.

## Notes

- A clean review with zero findings on a nontrivial draft is suspicious. Push the reviewers to be adversarial.
- Canvas is part of the experience when the findings need scanning. Use it for direct, non-trivial `/review-work` results; return structured findings to a composing skill when it owns the final artifact.
- Include panel attestation in the report: mode, worker count, model roles, finding count, and whether fan-out launched or was blocked.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
