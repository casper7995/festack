---
name: discovery
description: Research a client or account into a cited, confidence-rated picture with stakeholders, stack, signals, and open unknowns.
disable-model-invocation: true
---

# /discovery

Walking into an engagement blind wastes the first meeting. This skill builds the client picture first: who they are, what they run, who decides, and what is moving. It researches with discipline and renders a structured, cited picture the team can act on.

## Workflow

```
- [ ] 1. Read the ground: discovery checklist, research method, decision-gates, profile
- [ ] 2. Frame the scope of the research
- [ ] 3. Research the checklist from the declared sources
- [ ] 4. Structure and cite the findings
- [ ] 5. Stress it with /review-work
- [ ] 6. Render in canvas, and a doc if asked
- [ ] 7. Hand off
```

### 1. Read the ground

Read [references/discovery-checklist.md](references/discovery-checklist.md), the research method in the `festack-debate` skill (`references/research-method.md`), and the decision-gate convention (`references/decision-gates.md`). Read `$FESTACK_HOME/profile.md` for the declared knowledge sources, the client if known, and output preferences, and the host's model-role config for model roles. If the profile names no sources, ask which source families to use before researching, with `allow_multiple: true` because research sources are additive.

### 2. Frame the scope

State what this discovery is for (a first meeting, an account plan, a specific opportunity) and which checklist pieces matter most. A discovery with no focus collects trivia.

If the purpose is not given and not derivable from the request or profile, gate it with one `AskQuestion` before researching (first-meeting prep, account plan, or specific opportunity, with a recommended default). The purpose reshapes the entire picture, so it is a genuine fork, not a silent assumption.

### 3. Research the checklist

Work the checklist against the declared sources following the research method. Cite as you go. Weight by authority and recency. Mark genuine unknowns as unknown rather than guessing.

For a broad or high-stakes discovery, parallelize: run a `festack-debate` synthesize pass with `debate-runners`, each runner working a different slice of the checklist or a different source family, then merge into one cited picture. A single-threaded crawl is fine for a narrow discovery. When using peer benchmarks, choose peers by industry, size, operating model, and maturity, and treat them as directional pressure tests, not prescriptions.

### 4. Structure and cite

Assemble the findings against the checklist. Each piece is sourced or marked unknown, with a confidence note. Stakeholders are named by role with what they care about. Signals are dated and interpreted.

### 5. Stress it with /review-work

Invoke `/review-work` with the research-answer rubric. Loop fixes until the picture is cited, its uncertainty is explicit, and no major claim is unsupported.

### 6. Render

Before rendering, run a hygiene pass: verify every client-specific fact belongs to the target client, strip any template or example residue, and label any borrowed framework as a framework rather than evidence. Cross-client contamination is the fastest way to lose trust.

Render a structured canvas (the `canvas` skill): one section per checklist piece, a confidence summary, and the open unknowns. Tell a client-centered story, what is working, what is blocked, what is changing, and what should happen next, with claims quantified where possible. If the profile or the user wants a written brief, write it to the document target (the same rule as `/doc`).

### 7. Hand off

State the picture, the confidence, and the open unknowns with who could resolve each. Make the handoff transition-ready: executive summary, current team context, stakeholder map, initiatives by stage, paused or lost items worth revisiting, known blockers, key resources, open unknowns, and first-meeting questions for the next owner. Offer the next step: align the engagement with `/scope-and-align`, or design with `/solution-critic`.

## Notes

- Discovery is broad. For a single ad-hoc question, use `/client-debug` instead.
- The sources are the profile's, never hardcoded. This is how `/discovery` generalizes across companies.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
