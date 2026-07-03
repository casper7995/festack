# base critique rubric

Every critique pass starts here. The calling skill extends this with a per-deliverable rubric (demo, diagram, doc, alignment brief). Reviewers are adversarial and specific. The goal is client-ready, not polite.

## Dimensions every reviewer checks

1. **Correctness and feasibility.** Is anything wrong, infeasible, or based on a false assumption about the platform, the data, or the client? Trace it. Do not flag what you have not checked.
2. **Fit to the goal.** Does this actually serve the stated client goal and audience? Or does it answer a different question well?
3. **Missing pieces.** What required element is absent? A success criterion, a constraint, a stakeholder, a failure path, a cost.
4. **Client-readiness.** Would this land in front of the client as-is? Tone, clarity, structure, and credibility. Flag anything that reads as internal, sloppy, or generated.
5. **Risk and blast radius.** What is the worst plausible outcome if this ships unchanged? Who is affected.

## How to report each finding

- **Severity**: blocker, major, or minor. Blocker means do not ship. Major means fix before the client sees it. Minor means improve if time allows.
- **Evidence**: the specific place and the specific reason. No vague "could be clearer."
- **Fix**: one concrete change that resolves it.

## Calibration

Do not inflate severity. If everything is a blocker, nothing is. State what is already strong so the human knows what not to touch. Over-reporting burns trust and gets reviewers ignored.

## Prose

Short declarative sentences. No em-dashes. No mid-sentence colon connectors.
