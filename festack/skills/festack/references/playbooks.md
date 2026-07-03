# playbooks

Playbooks describe common end-to-end workflows in neutral capabilities. The delivery agent chooses one playbook, resolves each capability through the registry, and keeps handoff state between steps.

Do not hardcode company-specific systems here. Put company providers in `$FESTACK_HOME/capabilities.md` or the advanced strict `$FESTACK_HOME/capabilities.yaml`.

## Execution rules

1. Pick one primary playbook from the user's desired outcome.
2. Run steps in order unless a gate changes the path.
3. Resolve each capability through the capability registry before invoking a provider.
4. Preserve each provider's handoff payload for the next step.
5. Use `/review-work` through `review.deliverable` before calling a client-facing deliverable ready.
6. Use `build.approved_scope` only after explicit approval and an available build payload.
7. Skip conditional `align.scope` when an inherited brief handoff already settles the Goal, Audience, Success criteria, Belief to change, Judges, Decision unblocked, and Hard constraints required by the downstream step.
8. Every step handoff includes `recommended_next_step`: the next capability, skill, gate, review, build, stop, or `none` when complete.
9. Every playbook gate that uses `AskQuestion` includes a Gate receipt with the fork, classification, options, recommendation, answer, and recommended_next_step.

## account-prep

Use when the user asks to prep for an account, client, call, account transition, or broad account help.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `research.account` | yes | Account context, stakeholders, known initiatives, cited unknowns. |
| 2 | `fetch.customer_usage` | no | Usage or adoption signals when a provider exists. |
| 3 | `fetch.open_risks` | no | Blockers, escalations, support issues, or delivery risks. |
| 4 | `align.scope` | conditional | Alignment brief when goal, audience, or success criteria are unclear. |
| 5 | `create.client_doc` | yes | Call-prep package or account brief. |
| 6 | `review.deliverable` | yes | Readiness findings and residual risks. |

Gate: if the account is missing and context cannot resolve it, ask for the minimum account pointer. If the user wants generic sector or persona prep, proceed with explicit assumptions and treat `research.account` as generic account-context research rather than named-account research.

If `fetch.customer_usage` or `fetch.open_risks` has no configured provider, skip that optional step with a caveat. Missing optional providers are not setup blockers.

## product-question-to-client-answer

Use when the user has a specific customer product, support, roadmap, security, or capability question.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `research.product_question` | yes | Cited answer, confidence, caveats. |
| 2 | `create.client_doc` | conditional | Client-ready wording if requested. |
| 3 | `review.deliverable` | conditional | Review when the answer is client-facing or high-stakes. |

Gate: if the question is too broad, ask for the exact customer question or split it into discrete questions.

## architecture-decision-to-diagram

Use when the user asks to design, recommend, or choose an architecture and then visualize it.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `frame.problem` | conditional | Structured problem when the ask is still fuzzy. |
| 2 | `decide.approach` | yes | Recommended architecture or approach with rationale and dissent. |
| 3 | `create.diagram` | yes | Diagram artifact with source and handoff metadata. |
| 4 | `review.deliverable` | yes | Design package review if `decide.approach` ran; rendered diagram review after `create.diagram`. |

Gate: if the user only asks to draw an already-decided architecture, skip `decide.approach` and run `create.diagram`.

## competitive-proof-asset

Use when the user asks to prove differentiation, compare against a competitor, create a battlecard, or design a competitive proof.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `align.scope` | yes | Audience, success criteria, and proof standard. |
| 2 | `research.competitor` | yes | Fair differentiators, competitor strengths, cited claims. |
| 3 | `design.demo` | conditional | Demo proof when the deliverable is demonstrable. |
| 4 | `create.client_doc` | conditional | Battlecard, talk track, or leave-behind. |
| 5 | `review.deliverable` | yes | Red-team findings, claim risk, proof gaps. |
| 6 | `build.approved_scope` | conditional | Build execution for competitive demos only after explicit approval. |

Gate: never preserve absolute "better than" phrasing. Reframe as scoped, falsifiable differentiators tied to the customer's use case.

## competitive-poc

Use when the user is preparing a competitive POC, bake-off, or head-to-head evaluation against a named competitor end to end. This is the full sequence; for a single competitive asset without a POC, use `competitive-proof-asset` instead.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `research.account` | yes | The customer's pain, stakeholders, and evaluation context, cited. |
| 2 | `align.scope` | yes | Goal, judges, success criteria, audience, hard constraints. |
| 3 | `research.competitor` | yes | Fair differentiators scoped to the use case, competitor strengths, the buyer's evidence for their current view. |
| 4 | `scope.poc` | yes | POC contract with measurable exit criteria both sides accept. |
| 5 | `design.demo` | conditional | Demo design when the proof is demonstrable. |
| 6 | `create.client_doc` | conditional | AE-sendable doc or leave-behind. |
| 7 | `review.deliverable` | yes | Red-team findings on claims, proof gaps, and readiness. |
| 8 | `build.approved_scope` | conditional | Build execution only after explicit approval. |

Gates: confirm the account before step 1 when context cannot resolve it. The `poc-scope` hard gate carries over: do not proceed past step 4 if success criteria cannot be measured. The competitive reframe carries over: no absolute "better than" claims anywhere in the sequence.

## demo-design

Use when the user asks to scope, design, or build a demo and no approved build scope exists yet.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `align.scope` | conditional | Demo audience, belief change, success signal. |
| 2 | `design.demo` | yes | Demo brief, scenario, asset plan, acceptance checks. |
| 3 | `review.deliverable` | yes | Demo design review. |
| 4 | `build.approved_scope` | conditional | Build execution only after explicit approval. |

Gate: if the user asks to build immediately, stop after design and ask for build approval with scope, acceptance checks, adapter, and deploy target.

## poc-scope

Use when the user asks to scope a proof of concept, pilot, or evaluation.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `align.scope` | conditional | Stakeholders, goal, timeline, success criteria. |
| 2 | `scope.poc` | yes | POC contract, measurable exit criteria, responsibilities. |
| 3 | `review.deliverable` | yes | POC scope review. |
| 4 | `build.approved_scope` | conditional | Build execution only after approval. |

Gate: do not proceed if success criteria cannot be measured.

## doc-from-existing-artifact

Use when the user asks to turn an existing answer, diagram, design, or notes into a client-ready written artifact.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `create.client_doc` | yes | Document draft in the requested target surface. |
| 2 | `clean.prose` | conditional | Voice cleanup when prose quality matters. |
| 3 | `review.deliverable` | yes | Client-readiness review. |

Gate: if source material is missing or inaccessible, ask for the minimum artifact pointer or pasted content.

If the source artifact is a diagram, require the diagram handoff package: exported file or reachable image, source/editable file, caption, alt text, intended placement, resolution/export format, and open assumptions. If those are missing, ask for the minimum missing pieces or route back to `create.diagram`.

## approved-build

Use only when the user provides an approved plan or enough equivalent payload to build safely.

| Step | Capability | Required | Output |
| --- | --- | --- | --- |
| 1 | `build.approved_scope` | yes | Build phase status, checks, deployment/export evidence. |
| 2 | `review.deliverable` | conditional | Review if the build creates a client-facing artifact. |

Required payload:

- Approved artifact or pasted scope.
- Asset list or phase list.
- Acceptance checks.
- Target environment.
- Build adapter.
- Deploy or export target.
- Review status or explicit acceptance of review risk.
- Rollback or failure evidence expectations for deployed work.
