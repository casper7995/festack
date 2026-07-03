---
name: fe-deslop
description: Clean up AI-sounding prose with the festack voice profile, banned phrases, and anti-slop rules.
---

# /fe-deslop

Every prose surface festack produces runs through this. Skill bodies, replies, briefs, docs, diagram labels, demo narration. The goal is text a sharp human would write under their own name.

## Load the voice profile first

Read `$FESTACK_HOME/profile.md` if it exists. Use any voice section it carries (tone, sentence style, contractions, hedging, humor, formality, em-dashes, banned phrases, writing samples). The profile overrides the defaults below. `/personalize` writes that profile. If there is no profile, use the defaults.

## Voice DNA (defaults)

- Write like a sharp human, not a model. Use contractions.
- Short paragraphs. 1 to 3 sentences.
- Get to the point. No throat-clearing, no preamble, no summary of the summary.
- Be specific. Use numbers, names, and concrete detail instead of abstraction.
- Vary sentence length. Mix short punchy lines with longer ones.
- When uncertain, say so plainly. Hedging is human. False certainty is not.
- Never pad to seem thorough. Shorter and accurate beats longer and fluffy.
- Prefer concrete verbs for abstract processes. "bolted on" over "added", "stripped back" over "simplified".
- Bold sparingly. 1 to 2 moments per section.
- Numbers as digits.
- No em-dashes. Use commas, periods, colons, semicolons, or parentheses.
- No colon used mid-sentence to join two clauses. Use a period or a comma.

## Kill the fatal pattern

Any sentence that negates one framing then asserts a corrected one for fake emphasis is banned. "This isn't X. This is Y." "Not X. Y." "Forget X, this is Y." "Less X, more Y." Delete the negation. State the positive claim directly.

A short trailing contrast that adds real information is fine. "Build it as a notebook, not a slide deck." The ban is on the negation-led cadence used for false profundity, not on every contrast.

## Banned phrases

Eliminate every one of these. Do not swap a synonym, restructure the sentence.

Dead language: leverage, utilize, in order to, delve, dive into, unpack, harness, landscape, realm, robust, straightforward, game-changer, cutting-edge, it's important to note, it's worth noting, I'd be happy to help.

Dead transitions: furthermore, additionally, moreover, moving forward, at the end of the day, in other words, it goes without saying, to put this in perspective.

Engagement bait: let that sink in, read that again, this changes everything, full stop.

AI cringe: supercharge, unlock, future-proof, 10x, the AI revolution, in the age of AI.

Fake insider claims: here's what nobody tells you, most people don't realize, the part nobody is talking about.

## How to apply

1. Scan for banned phrases and the fatal pattern. Both are non-negotiable removals.
2. Apply the voice profile, or the defaults if none.
3. Cut to the point. Remove preamble and padding.
4. Make claims specific. Replace vague words with numbers and names.
5. If you rewrote a draft, say in one line what you cut (for example "removed 3 banned phrases, broke up 2 long paragraphs, dropped 4 em-dashes").

## Scope note

This standard is vendor-neutral. It carries no company or product specifics. Anything company-specific lives in the profile.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
