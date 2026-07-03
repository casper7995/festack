# decision-gate convention

festack work is decision-heavy. Business calls, stakeholder calls, and product calls run through it. AskQuestion is first-class. Throughout festack, `AskQuestion` means the host's structured question gate: the `AskQuestion` tool in Cursor, the `AskUserQuestion` tool in Claude Code, and the host prompt in Codex. Resolve it to your host's tool wherever a festack skill says `AskQuestion`. But asking the human about things you could check yourself is a tax. Classify every fork before you ask.

## Classify before you ask

For each fork, decide which kind it is.

- **Observable.** You can resolve it by reading, running, or checking something. The profile, a doc, the data, a config, a platform behavior, the engagement history. Resolve it. Do not ask.
- **Reversible and low-stakes.** Cheap to undo and not client-visible. Pick a sensible default, state the choice, and move on. Do not ask.
- **Genuine decision.** A business, stakeholder, scope, audience, tone, or preference call that you cannot derive and that changes the deliverable. Ask.

Only the third kind goes to `AskQuestion`.

Classify inline; it is part of the reasoning you are already doing and costs nothing. If a fork is genuinely ambiguous and you cannot tell reversible from genuine, spend one cheap call on the `classifier` role (the cheapest model in the host's model config) rather than a frontier model, or rather than reflexively interrupting the human. If it is still unclear after that, treat it as genuine and ask.

## How to ask well

When a fork is a genuine decision:

- Ask at the real fork, not before you have framed it. The human should see the trade-off, not a blank prompt.
- Offer concrete options with the trade-off attached. Recommend one and say why.
- Batch related decisions into one `AskQuestion` call rather than drip-feeding. Respect the host tool's limits when batching: Claude Code's `AskUserQuestion` caps at four questions per call with four options each, so when a batch exceeds the cap, split it into sequential calls rather than truncating options.
- Use `allow_multiple: true` when the valid answer is additive: stakeholders, audiences, priorities, objections, success criteria, risks, requirements, scope items, sources, output surfaces, assets, or things to cut. Use single-select when the options are mutually exclusive: one route, one primary recommendation, one default, approve/revise/stop, live vs recorded, current vs future state, or a primary document target.
- Never ask a question whose answer is already in the profile or the prior conversation.

## Gate receipt

Every `AskQuestion` gate returns a short receipt so the FE can see why they were interrupted:

- `fork`: the decision being made.
- `classification`: genuine decision.
- `options`: the exact structured options shown.
- `recommendation`: the default the agent recommends and why.
- `answer`: the selected option or options.
- `recommended_next_step`: what should happen immediately after the answer.

## Refuse to proceed on missing pieces

A Socratic festack skill does not paper over a gap. If a required input is missing (the goal, the audience, a success criterion, a hard constraint), name it and resolve it. Resolve observable gaps yourself. Gate on genuine ones. Do not silently assume and build on the assumption.

## Where multi-model fits

Run the panel (`festack-debate`) where the output iterates heavily under human review. Design debate, demo design, diagrams, research, contested alignment. A gate is not automatically a panel. Most gates are a single classify-and-ask. Reserve the panel for the forks where exploring alternatives changes the answer.
