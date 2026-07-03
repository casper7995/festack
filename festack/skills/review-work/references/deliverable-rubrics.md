# per-deliverable rubrics

Each rubric extends the base rubric in the festack-debate skill (`references/critique-rubric-base.md`). The base covers correctness, fit, missing pieces, client-readiness, and risk. These add what each deliverable type demands. Pick the one matching the draft. Extend, do not replace.

## demo

- **Time box.** Does it fit the stated slot end to end, with a buffer? Is there a minute-by-minute run of show?
- **Live surface and failure path.** What runs live, and what is the rehearsed fallback if it fails in the room?
- **Determinism.** Are non-deterministic steps frozen for the live run (pinned versions, cached acceptable output)?
- **Audience split.** Does it land for both business and technical attendees? Who sees what?
- **Impact number.** Is the headline metric defended with a stated baseline, assumption, and source?
- **Path to production.** Is there a credible step from demo to production, not just a clever one-off?
- **Data and privacy.** Synthetic or de-identified? What sensitive fields are masked on screen?

## alignment brief

- **Completeness.** Are vision, goal, requirements, success criteria, audience, and risks all present and specific?
- **Measurability.** Is success stated as something checkable, not a sentiment?
- **Decisions vs open forks.** Are settled decisions separated from genuine open questions? No internal SA notes leaking into a client surface.
- **Single owner per open item.** Does each unresolved item name who decides and by when?

## diagram

- **Truthfulness.** Does the diagram match the actual or proposed architecture? No boxes that do not exist.
- **Reading order.** Does it read in the direction the story flows? Left to right or top to bottom, one primary path.
- **Density.** Not a wiring schematic, not a cartoon. Right altitude for the audience.
- **Labels and legend.** Are components, flows, and trust boundaries labeled? Is anything color-coded explained?
- **Client styling.** Styling is consistent and intentional, with no default-tool clutter and no unrequested vendor marks. Apply client or profile styling only when it was asked for.

## doc

- **Audience and purpose.** Clear who reads it and what they should do after. One job per doc.
- **Structure.** Skimmable. Headings, short paragraphs, a lead that states the point.
- **Anti-slop.** Passes the `fe-deslop` skill. No filler, no banned phrases, no generated cadence.
- **Accuracy.** Every claim is checkable or attributed. No invented specifics.
- **Formatting.** Real headings, real bullets, embedded links. No bare URLs in body text. Inline citations for key facts.
- **Next step.** Ends with a concrete ask or action, not a summary of itself.

## design package

For the output of /solution-critic (a recommended approach with the debate captured).

- **Decision quality.** Is the recommendation justified against the stated criteria, or asserted? The reasoning is visible.
- **Rejected alternatives.** Are the paths not taken named, with why each lost? A design with no rejected options did not debate.
- **Dissent preserved.** Is the strongest counter-argument still visible, not averaged away?
- **Feasibility.** Is the approach buildable with the stated constraints and resources? No hand-waving over the hard part.
- **Open forks.** Are the genuine remaining decisions surfaced with owners, separated from what is decided?
- **Path to production.** Does it lead somewhere real, not just a clever one-off?

## research answer

For a researched answer to a client or product question (the output of `/discovery`, `/client-debug`, or any research deliverable).

- **Answers the exact question.** Addresses the specific scenario asked, including every "or" branch. Explains why, not just yes or no.
- **Cited.** Every key claim has an inline source. High-authority sources named.
- **Uncertainty is explicit.** Separates what is confident, what is less confident and why, and what could not be determined and who to ask.
- **Confidence rating.** Carries a confidence level with a one-line justification. A low-confidence answer is not dressed up as settled.
- **Source quality.** Weighted by authority and recency. No stale or informal source presented as authoritative.

## competitive

For competitive comparisons, battlecards, proof assets, and competitive demo claims.

- **Scoped claim.** Every "better than" claim is scoped to a use case, workload, constraint, or buyer priority. No absolute superiority claims.
- **Competitor fairness.** Real competitor strengths are stated clearly enough that a skeptical evaluator would recognize them.
- **Citation shareability.** Client-facing claims cite client-citable sources. Internal evidence can influence confidence but is not quoted or exposed.
- **Freshness.** Competitive facts are current enough for the decision, or staleness is called out.
- **Proof falsifiability.** Demonstrable proof points state what would count as success or failure.
- **No strawmen.** The comparison attacks the actual competing product, pattern, or incumbent architecture, not a simplified version.
