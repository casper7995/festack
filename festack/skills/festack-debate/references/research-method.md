# research method

The shared research discipline for festack. Used by `/discovery`, `/client-debug`, `/doc`, `/compete`, and the light research step in `/problem-frame`. Vendor-neutral: the sources are whatever the profile declares, never hardcoded.

## Steps

1. **Map the question.** Name the direct subject, its dependencies, the alternatives, and the related concepts. A precise answer often depends on a nearby fact, so map before you search.
2. **Preflight connectors.** Before researching, validate that the declared source adapters are actually available: auth is valid, the companion skill or MCP exists, and the source can be queried or read. If a source is inaccessible, do not silently skip it. Mark it unavailable, say how confidence changes, and ask only if the missing source is essential.
3. **Cover breadth, then rank by authority.** Search the profile-declared sources in order of authority (authoritative or public documentation first, then the internal knowledge base, then community and chat), but do not stop at the first family that appears to settle the question. When the profile declares both an external and an internal source family, consult at least one of each before answering: external sources tell you what is promised, internal knowledge and chat tell you what is actually true right now, including status, limits, and field gotchas. For feature status, roadmap, limits, or anything in flux or contested, treat internal confirmation as required, not optional. Refer to sources by family, not by tool name, so this holds for whatever the profile declares. If the profile declares no source, ask which source families to use.
4. **Find the right people and channels.** When a question needs a human confirm, identify the owner or channel from the profile. Name them in the output.
5. **Deep-dive the uncertain.** For anything in preview, in flux, or contested, get the specifics: current status, timeline, how to access, and what does not work yet. Do not stop at "it exists".
6. **Validate against the exact question.** Answer the specific scenario asked, including every "or" branch. Explain why, not just yes or no.
7. **Handle uncertainty explicitly.** Split the answer into what you are confident about, what you are less confident about and why, and what you could not determine and who to ask.

## Output discipline

- **Cite everything.** Every claim a reader could challenge carries an inline source. A claim with no source is a guess, label it one.
- **Weight by authority and recency.** A current authoritative source beats an old informal one. Say when a source is stale.
- **Rate confidence.** Carry a confidence level (high, medium, low, or a 1 to 10 scale) with a one-line justification. Never present a low-confidence answer as settled.

## Source weighting (general tiers)

1. The owner or decision-maker confirming directly.
2. Official or authoritative documentation.
3. A recent internal confirmation or FAQ.
4. Field or practitioner experience.
5. Old or informal discussion. Lowest weight, and say so.
