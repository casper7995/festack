# routing table

How `/festack` maps what the user wants to the right festack skill or the end-to-end delivery agent. Match on intent, not keywords. When the user asks for a narrow deliverable, prefer the smaller, more specific skill. When the user asks for an outcome that spans phases, hand off to `festack-delivery-agent`.

Every route emits a Routing receipt: intent, route, why, setup_state, recommended_next_step, and visual_artifact_receipt. Field semantics: `recommended_next_step` is the immediate next action after this receipt (usually the handoff itself; `none` only when the route fully answers the ask). `visual_artifact_receipt` is the surface the routed skill is expected to own (`canvas`, `docs-canvas`, structured handoff, prose, or `none`) plus the owner; the router states the expectation, the owning skill confirms it at closeout. If routing used `AskQuestion`, include the Gate receipt from `festack-debate/references/decision-gates.md`; read that file before emitting any Gate receipt.

Receipts never delay value. Keep them compact, and when the route hands off to `festack-delivery-agent` running inline, emit one combined receipt (the agent's, carrying the router's fields) rather than two near-duplicates.

## The map

| The user wants to... | Route to | Notes |
|---|---|---|
| Align on goals, vision, success criteria before work starts | `/scope-and-align` | The Socratic front of an engagement. |
| Prep me for this account / help me with this account | `festack-delivery-agent` | Broad account help. Sequence discovery, alignment if needed, packaging, and review. |
| Prep me for an industry/persona call without a named account | `festack-delivery-agent` | Ask whether to do account-specific research or generic prep with assumptions. |
| Research a client or account before engaging | `/discovery` | Structured client picture with citations. |
| Answer a product question for a client-ready deliverable | `festack-delivery-agent` | Use the product-question playbook: research first, package only after facts are settled. |
| Answer a product question plus an architecture option | `festack-delivery-agent` | Settle product facts first, then decide the approach. |
| Answer a specific ad-hoc client or product question | `/client-debug` | Fast or deep; cited; confidence stated. |
| Decide between approaches / get a recommendation | `/solution-critic` | Multi-model debate, decision captured. |
| Understand and frame a fuzzy client problem | `/problem-frame` | Problem, sub-problems, constraints, stakeholders, unknowns, and canvas. |
| Draw an already-decided architecture | `/diagram` | Visualize what is real or explicitly proposed. |
| Scope and design a customer demo | `/demo` | Flagship. Design before build. |
| Make a client-ready diagram (architecture, ERD, flow) | `/diagram` | Multi-model iteration + visual loop. |
| Write a client-facing document | `/doc` | Right structure + anti-slop prose. |
| Put an existing or final diagram into a client doc | `festack-delivery-agent` | Use the doc-from-existing-artifact playbook and require diagram handoff metadata. |
| Design something and render it as a diagram/doc | `festack-delivery-agent` | Sequence design first, then `/diagram` or `/doc`. |
| Create multiple client artifacts or embed one in another | `festack-delivery-agent` | Produce the source artifact first, then package it with handoff metadata. |
| Scope a proof of concept with success criteria | `/poc` | Living contract, measurable exit criteria. |
| Quick compare / why us over a competitor | `/compete` | Fair, cited, profile-supplied differentiators. |
| Create a battlecard, leave-behind, or competitive proof asset | `festack-delivery-agent` | Research via `/compete`, then package and review. |
| Make a competitive proof asset or demo | `festack-delivery-agent` | Sequence alignment, `/compete`, `/demo` or `/doc`, review, and build gate. |
| Prep a competitive POC or bake-off end to end | `festack-delivery-agent` | Use the competitive-poc playbook: pain research, competitor research, POC contract, demo design, doc, review. |
| Stress-test a deliverable before it ships | `/review-work` | Adversarial critique against a rubric. |
| Just build an already-approved scope to completion | `/autopilot` | Executes a design; never invents one. |
| Reflect on what worked and what did not | `/retro` | Honest reflection into candidate lessons. |
| Capture a lesson or preference for next time | `/learn` | Sorts into profile vs lessons; dedups. |
| Clean up prose so it does not read like AI | `/fe-deslop` | Usable directly or composed by any skill. |
| Set up or repair festack | `/setup-festack` | One guided setup for profile, model roles, and capability wiring. |
| Configure which models festack uses | `/setup-models` | Writes the host's model config (`festack-models.mdc` on Cursor, `~/.claude/festack/models.md` on Claude Code). |
| Set up or update their profile and voice | `/personalize` | Writes profile.md. |
| Configure which installed providers satisfy workflow capabilities | `/setup-capabilities` | Writes capabilities.md or capabilities.yaml. |
| Pick the right festack workflow (ambiguous ask) | `/festack` | Canonical front door. Self-entry when the user is unsure. |
| Carry a broad FE task through multiple skills | `festack-delivery-agent` | Orchestrator. Use for lazy end-to-end asks, not for one narrow artifact. |
| Resume an engagement / "where were we on X" | `/festack` | Inference per ledger-lifecycle.md; announce the pick; collisions hard-ask. |
| Package an engagement for a colleague | `/handoff` | Self-contained snapshot from the ledger; paste it yourself. |
| Capture a call note / out-of-band update for an engagement | `/festack log "<sentence>"` | Five-second quick-log receipt; supersedes contradicted facts. |
| (internal) Run a multi-model debate or critique | `festack-debate` | Engine only. Never a route; skills compose it, the user does not call it. |

## Disambiguation: the confusable clusters

The sub-skills overlap at the edges. These are the tie-breakers the router applies before routing.

**Pre-engagement vs problem vs decision (`/scope-and-align` | `/problem-frame` | `/solution-critic`):**

- `/scope-and-align` when nothing is agreed yet and the fork is "what are we trying to achieve and how will we know we won." Aligns goal, audience, success criteria, scope. *"We're kicking off with this client, help me frame the engagement."*
- `/problem-frame` when the problem is fuzzy and you need to understand it before designing. It names pain, sub-problems, constraints, stakeholders, and unknowns. *"Help me frame their batch-latency problem."*
- `/solution-critic` when there are competing approaches and you must pick one with rationale. Multi-model debate. *"Should we use approach A or B for their pipeline?"*

**Whole account vs one question (`/discovery` | `/client-debug`):**

- `/discovery` builds a broad picture of an account before or around engaging. *"Research this client before our first call."*
- `/client-debug` answers one specific question with citations. *"They asked if feature X supports Y, find out."*

**Write-up vs research (`/doc` | research skills):**

- `/doc` when the deliverable is a written document and structure plus prose are the job. *"Turn this into a client-ready summary."*
- The research skills (`/discovery`, `/client-debug`) find and structure facts; `/doc` packages them. If both are needed, research first, then `/doc`.
- A single product/support question routes through `festack-delivery-agent` only when the user names a packaged deliverable: an email, doc, slide, one-pager, or something to send the client. Urgency, stakes, or the answer being relayed onward do not upgrade a fact lookup; without a named deliverable it routes directly to `/client-debug`, which can always offer packaging afterward.

**Standalone diagram vs inside a workflow (`/diagram`):**

- `/diagram` when the diagram is the deliverable and the architecture is already decided or explicitly proposed.
- "Design the target architecture and draw it" is not standalone. Route through `festack-delivery-agent`: use `/problem-frame` only if the problem is still fuzzy, `/solution-critic` for the design decision, then `/diagram`.
- "Put this final diagram into a doc" is packaging, not diagram creation. Route through `festack-delivery-agent` to run `doc-from-existing-artifact` unless diagram handoff metadata is missing.

**Competitive comparison vs packaged competitive asset (`/compete` | `festack-delivery-agent`):**

- `/compete` owns competitive research and quick comparison: "why us over X", "compare us to X", "where do we win".
- `festack-delivery-agent` owns packaged assets: battlecards, leave-behinds, cited claim docs, and competitive proof demos. It sequences alignment, `/compete`, packaging, review, and build gates if needed.

## Glossary

- `/problem-frame`: understand the problem.
- `/solution-critic`: decide the approach.
- `/diagram`: visualize an already-decided or explicitly proposed architecture.
- `festack-delivery-agent`: sequence multiple phases.

## Routing rules

- **Route directly only on a single clear narrow match.** If exactly one skill fits after the tie-breakers above, name it and hand off. If two or more narrow skills still fit, ask once with `AskQuestion` listing the candidates. Never route to a heavy workflow (`/demo`, `/poc`, `/autopilot`, `/scope-and-align`) on a weak guess; a wrong route there burns real time.
- **Use `festack-delivery-agent` for lazy end-to-end asks.** If the user invokes `/festack` with an outcome rather than a specific artifact, or asks to be taken through a task like a playbook, hand off to the delivery agent. It sequences the skills, keeps state, asks gates, and routes to `/autopilot` only after design approval.
- **Broad beats route-choice ambiguity.** If the ambiguity is "which phases are needed to get this outcome," use the delivery agent. If the ambiguity is "what deliverable do you want," ask one structured question with a recommended path.
- **Resolve "this" before asking.** Inspect available context, selected text, attachments, open files, and profile facts before asking the user to restate an account, artifact, or customer ask. If a referenced attachment is inaccessible, treat it as missing evidence.
- **Do not break panel fan-out.** If `festack-delivery-agent` would run as a nested subagent that cannot launch the panel workers used by `/solution-critic`, `/review-work`, or `festack-debate`, follow the delivery-agent instructions inline from the top-level conversation instead.
- **Specific over broad.** "Draw the architecture" is `/diagram`, not `/demo`, even though a demo may contain a diagram.
- **Design before build.** Any "build it" request with no approved design routes through a design skill first (`/demo`, `/poc`, `/solution-critic`), then `/autopilot`.
- **Approved build evidence.** A claimed approval or inaccessible attachment is not enough for `/autopilot` unless the approved artifact or equivalent payload is present: approved artifact or pasted scope, asset list or phase list, acceptance checks, target environment, build adapter, deploy/export target, review status, and rollback or failure evidence for deployed work.
- **Setup gaps.** If profile or model config is missing, route through `/setup-festack` first, then continue. Missing user capability registry is not a setup blocker; use default-only capability mode unless the user wants company providers or a required capability has no default provider.
- **Compose, do not absorb.** The router hands off to one skill or the delivery agent. The chosen layer composes the others it needs. The router does not try to do the work itself.
