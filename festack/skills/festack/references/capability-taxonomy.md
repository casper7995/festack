# capability taxonomy

Capabilities are the neutral contract between festack playbooks and installed skills or tools. A playbook asks for a capability; the registry resolves which provider should handle it in the current environment.

Do not put company-specific products, internal systems, account names, credentials, or customer facts in this file.

## Resolution rules

1. Match the playbook step to one capability.
2. Resolve the capability from `$FESTACK_HOME/capabilities.md` when present, or `$FESTACK_HOME/capabilities.yaml` when it is selected for strict parsing or Markdown is absent.
3. If both user registries exist and disagree, pause for `/setup-capabilities` to reconcile them.
4. If no user registry exists, use `default-capability-registry.md`.
5. If the user registry names a provider that is not installed or reachable, fall back to the next available provider or the default provider.
6. If no provider exists, ask one focused question or continue with a clearly stated missing-capability caveat. Do not invent a company-specific provider.

MCP providers use `mcp:<server>` or `mcp:<server>/<tool>`. Always verify the MCP descriptor and schema before invocation.

## Handoff contract

Every capability provider should return enough structure for the next step:

- `capability`: the capability fulfilled.
- `provider`: the skill or tool used, or `providers` when multiple additive providers were used.
- `artifact_type`: research, design, diagram, document, review, build, or gate.
- `summary`: what was learned or produced.
- `sources`: citations or source descriptions when claims are made.
- `confidence`: high, medium, low, or not applicable.
- `decisions`: decisions made by the user or by the workflow.
- `open_questions`: unresolved questions and who can resolve them.
- `next_recommended_capability`: the next capability to run, if obvious.

When a capability uses multiple additive providers, aggregate their results:

- Preserve every provider name in `providers`.
- Merge sources and mark source shareability.
- Summarize conflicts instead of smoothing them away.
- Emit one combined confidence level and explain what drove it.
- Produce one handoff payload for the next capability.

## Canonical capabilities

| Capability | Purpose | Typical input | Expected output | Default fallback |
| --- | --- | --- | --- | --- |
| `research.account` | Build account or client context before engagement. | Account name, client context, call goal. | Cited account picture, stakeholder hints, unknowns. | `/discovery` |
| `research.product_question` | Answer a specific product, support, or technical question. | The exact client question and constraints. | Cited answer, confidence, caveats. | `/client-debug` |
| `research.competitor` | Position against a named competitor or alternative. | Competitor, use case, audience. | Fair differentiators, competitor strengths, proof needs. | `/compete` |
| `fetch.customer_usage` | Retrieve customer usage, adoption, or consumption signals. | Account identifier and metric need. | Usage summary with source and caveats. | Ask for provider |
| `fetch.open_risks` | Retrieve open blockers, issues, escalations, or delivery risks. | Account, project, or use-case context. | Risk list with status and owner hints. | Ask for provider |
| `frame.problem` | Structure a fuzzy problem before designing. | Stated ask, pain, constraints. | Problem statement, sub-problems, constraints, unknowns. | `/problem-frame` |
| `decide.approach` | Choose among competing approaches. | Framed problem and candidate approaches. | Recommended approach, rationale, dissent. | `/solution-critic` |
| `align.scope` | Align goals, audience, success criteria, and scope. | Engagement context and desired outcome. | Alignment brief and decision gates. | `/scope-and-align` |
| `design.demo` | Design a customer demo before build. | Goal, audience, proof point, constraints. | Demo brief, scenario, acceptance checks. | `/demo` |
| `scope.poc` | Scope a POC as a measurable contract. | Use case, stakeholders, timeline. | POC scope, success criteria, exit conditions. | `/poc` |
| `create.diagram` | Produce or refine a diagram. | Decided or proposed architecture, flow, or model. | Diagram artifact plus source/handoff metadata. | `/diagram` |
| `create.client_doc` | Package information into a client-facing document. | Source artifact, audience, tone, target surface. | Written deliverable and shareability notes. | `/doc` |
| `review.deliverable` | Red-team a deliverable before shipping. | Draft artifact and rubric type. | Findings, severity, required fixes, residual risk. | `/review-work` |
| `build.approved_scope` | Execute an already-approved scope. | Full approved-build payload: artifact or scope, assets or phases, checks, target environment, adapter, deploy/export target, review status, rollback evidence expectations. | Build status, evidence, remaining gates. | `/autopilot` |
| `learn.feedback` | Capture durable lessons or preferences. | Feedback, outcome, correction. | Profile or lessons update proposal. | `/learn` |
| `clean.prose` | Remove AI-sounding prose. | Draft text and audience. | Cleaned prose or style findings. | `/fe-deslop` |

## Naming rules

- Use verb-noun names: `research.account`, `create.diagram`, `build.approved_scope`.
- Keep names vendor-neutral and reusable across companies.
- Add a capability only when at least two playbooks or company packs could use it.
- Prefer one capability per workflow step. If a step needs two capabilities, split the step.
