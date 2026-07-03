---
name: compete
description: Position your platform against a competitor with fair, cited proof; use for /compete, "why us over X", or competitive research.
disable-model-invocation: true
---

# /compete

Position what you represent against a competitor, for a specific client, in a way a skeptical technical buyer will believe. Fair, specific, cited.

festack ships no competitive opinions. Who your competitors are, where you win, and your proof points all come from the profile. If the profile has none, this skill researches from declared sources and asks you for the differentiators it cannot find.

## Step 0: read config and profile

- Read `$FESTACK_HOME/profile.md` for: what you represent, named competitors, known differentiators, proof points, and declared research sources. If there is no profile, run `/personalize` first or ask for the essentials inline.
- Read the host's model-role config for model roles. If a debate or research step wants a panel, use `debate-runners`.

## Step 1: pick the mode

Read the ask.

- **Fast** (default): a quick "why us over X" for a conversation. Answer from the profile's differentiator notes. 2 to 3 differentiators tied to this client's use case, the honest "where they're strong", done in chat. Stop here unless asked for more.
- **Comprehensive**: the ask says detailed analysis or the competitive research will be shared. Go to Step 2. If the user asks to create a battlecard, leave-behind, client doc, or competitive proof demo, route through `festack-delivery-agent` so `/compete` supplies the research and the parent workflow owns packaging, review, and build gates.

Fast is the reversible default; take it unless the output is client-visible, shareable, or the ask materially changes the deliverable. Do not interrupt to ask which mode for a quick in-conversation question.

## Step 2: frame (comprehensive)

Pin down before researching:

- **Competitor.** Which one, which product line.
- **Client context.** What does this client actually care about? A generic comparison is weak. Scope the comparison to their use case, their stack, their constraints.
- **Audience.** A technical evaluator and an economic buyer need different cuts.
- **The decision.** What is this analysis meant to move? A bake-off, a renewal, a greenfield choice.
- **The buyer's evidence.** When the buyer already leans toward the competitor, find out what evidence or criteria produced that view before drafting anything. You cannot rebut a view you have not seen, and the buyer will test you on it.

Resolve what the profile and context already answer. For any of these five that is genuinely missing and changes the battlecard (the competitor or product line is unclear; the client context, audience, or decision is unknown; or the buyer leans toward the competitor and their evidence is unknown), gate it with one batched `AskQuestion` before researching. Do not guess the competitor or the audience; a battlecard aimed at the wrong cut is wasted.

Use `allow_multiple: true` for additive framing choices: client priorities, constraints, incumbent tools, evaluator personas, buyer personas, and proof points to emphasize. Use single-select for the primary competitor, product line, and the decision this analysis is meant to move.

## Step 3: research

Read `skills/festack-debate/references/research-method.md` and follow it. For competitive work specifically:

- Pull what the profile already knows first. Then fill gaps from declared sources.
- When every declared source is first-party (your own docs, your own wiki), add at least one source the buyer would accept as neutral: the competitor's public docs, a third-party benchmark, or something the buyer can run themselves. A comparison sourced only from your own material cannot fairly establish the competitor's strengths.
- Competitive facts decay. Weight recent sources hard and flag anything you could not freshly confirm.
- Confirm the competitor's strengths as carefully as your own. You will state them.
- If research shows the competitor genuinely wins the axis the buyer cares about, say so. Then reframe: concede that axis, shift the evaluation to axes where you win, or propose a bake-off with criteria both sides accept. A credible concession beats a losing argument, and it is often the actual winning play.
- Cite every claim that will appear in the comparison.

## Step 4: draft against the structure

Read `skills/compete/references/compete-structure.md` and draft the comprehensive analysis against it. Lead with the quick answer. Build the comparison scoped to this client. State where you win with proof, and where the competitor is genuinely strong.

## Step 5: the fairness gate

Before review, check the draft against the credibility rules in the structure reference. Falsifiable means stated so the buyer could check it and prove it wrong: run it, measure it, or trace the citation. A claim that cannot fail is marketing; cut it.

- Are the competitor's real strengths stated, not buried?
- Is every differentiator a concrete, falsifiable capability with proof, not an adjective?
- Is every comparison claim cited, and could the buyer verify it themselves from what you cite?
- Did you avoid asserting any competitor gap you cannot prove?

If any answer is no, fix it before going further. A competitive doc that fails the fairness gate will lose the technical buyer the moment they catch one overclaim. Under deadline pressure, cut scope, not this gate or the review pass: a smaller honest comparison beats a complete puff piece.

## Step 6: review and humanize

- For a comprehensive analysis, use a single-panel default: run the draft through `/review-work` with the research-answer and doc rubrics. A competitive doc is adversarial by nature, so the multi-model critique is required here, not optional.
- Add an extra adversarial critique pass with `festack-debate` only when the work is contested or high-stakes: an executive-ready battlecard, a competitive POC, a bake-off proof asset, or a claim set likely to be challenged by the competitor's technical counterpart. If you spend that extra panel, record why it was worth the cost and pass the synthesis into `/review-work` rather than rerunning the same critique blindly.
- Run all prose through `fe-deslop`. Competitive docs attract superlatives worse than any other deliverable; the `fe-deslop` banned list is the filter, applied hard.

## Step 7: render

- **Fast:** the answer is the chat reply. Offer to expand into a comprehensive analysis.
- **Comprehensive:** render a canvas with the comparison and differentiators. If a packaged battlecard or leave-behind is needed, hand the researched comparison to `create.client_doc` through the parent workflow or `/doc`; do not silently own packaging from `/compete`.

## Principles

- **Fairness is the credibility engine.** The honest "where they're strong" is what makes the rest believable.
- **Specific beats loud.** One concrete, proven differentiator outweighs five adjectives.
- **The profile owns the opinions.** festack supplies the discipline; your profile supplies the stance.
- **Stale competitive claims are worse than none.** Flag what you could not confirm.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
