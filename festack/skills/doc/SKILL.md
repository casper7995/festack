---
name: doc
description: Write a client-ready doc, one-pager, FAQ, design note, how-to, or decision brief with structure and clean prose.
disable-model-invocation: true
---

# /doc

Client documents are deliverables, and they fail in two ways: wrong structure for the job, and prose that reads like a machine wrote it. This skill fixes both. It picks the doc type, structures the content, and writes it in a human voice through the `fe-deslop` standard.

## Workflow

```
- [ ] 1. Read the ground: doc rubric, doc types, profile, fe-deslop
- [ ] 2. Pin the doc's one job and audience
- [ ] 3. Gather and structure the content
- [ ] 4. Draft against the skeleton
- [ ] 5. Stress it with /review-work
- [ ] 6. Write to the document target
- [ ] 7. Verify the written artifact
- [ ] 8. Hand off
```

### 1. Read the ground

Read the doc rubric in the `review-work` skill (`references/deliverable-rubrics.md`, doc section), [references/doc-types.md](references/doc-types.md), and `$FESTACK_HOME/profile.md` for the document target, audience defaults, and voice profile. The `fe-deslop` skill governs all prose.

### 2. Pin the one job and audience

State who reads this and the single action they should take after. A doc with two jobs needs to be two docs. Use `AskQuestion` only if the job or audience is genuinely unclear and not in the profile or context.

Capture the constraints that change the doc when they matter: reader, decision or action, distribution level, sensitivity, required format, deadline, source-authority requirement, and required reviewer. If the doc touches legal, security, privacy, pricing, roadmap, or contractual claims, mark it review-required and keep uncertain claims out of the client-ready draft.

Use `allow_multiple: true` when asking for readers, secondary audiences, required reviewers, source families, sections to include, or distribution surfaces. Use single-select for the document's one job, the primary audience, sensitivity level, and primary output target.

### 3. Gather and structure

Collect the content. If lookups are needed, apply the research discipline: cite every claim, weight sources by authority and recency, separate confident from uncertain, and rate confidence. Map the content onto the matching skeleton from the doc types reference.

If the source artifact is a diagram, require the diagram handoff package before drafting: exported file or reachable image, source/editable file, caption, alt text, intended placement, resolution/export format, and open assumptions. If any required piece is missing, ask for the minimum missing field or route back to `/diagram` for handoff completion. Do not embed a diagram with unclear source, stale assumptions, or missing alt text in a client-ready doc.

For a batch of questions (an RFP, an FAQ, a questionnaire), normalize before answering: preserve each original question, deduplicate near-matches, group by topic, classify each, and track status as answered, partial, blocked, or needs-review. Lead the output with a short completion summary before the detailed answers.

### 4. Draft against the skeleton

Write the draft. Lead with the point. Real headings, real bullets, embedded links, inline citations for anything challengeable. No bare URLs. Run the prose through `fe-deslop`.

### 5. Stress it with /review-work

Invoke `/review-work` with the doc rubric. Loop fixes until there are no blockers and no majors. Pay attention to anti-slop, accuracy, formatting, and whether it ends with a concrete action.

For anything client-facing, run a final sanitization pass: no other client names, no copied template residue, no internal-only terms, no unsupported metrics, no confidential source details, no raw research notes, and no claim whose source cannot be shared or cited.

### 6. Write to the document target

If the profile declares a document target and the matching document skill is available, create the doc there and return the link. Before writing, load the companion writer skill or adapter, validate auth and write access, and preserve formatting: headings, lists, tables, links, citations, and image placement. The target and writer are whatever the profile declares; this skill names none.

If no document target is available, do not silently create a local markdown file. Ask first. Offer: return the draft in chat, create local markdown in the engagement workspace, or pause until the user configures a document target. Only create a local `.md` file when the user explicitly chooses that path or the profile declares local markdown as the document target.

For a long or navigation-heavy doc (a how-to, runbook, design doc, account or partnership review, workflow showcase, or a large FAQ or questionnaire), also render it as a navigable canvas (the `docs-canvas` skill) so the reader can scan sections instead of scrolling a wall of text. Keep one-pagers and short briefs as plain prose; do not canvas what fits on a screen.

### 7. Verify the written artifact

After writing to a document target, verify the produced artifact rather than trusting the write call. At minimum, reopen or read back the document metadata/content the adapter exposes and check: title, headings, links, citations, embedded diagrams/images, table/list formatting, sensitivity/sanitization, and shareability. For visual-heavy docs, inspect a screenshot or exported preview when the adapter supports it. If verification is impossible, say so and mark the residual risk.

### 8. Hand off

State what the doc is for and the action it asks of the reader. Note anything that still needs confirmation.

## Notes

- The two failure modes are wrong structure and slop. The skeleton fixes the first, `fe-deslop` fixes the second.
- For a heavy research doc, delegate the gathering to `/discovery` (a broad client picture) or `/client-debug` (one specific question). For light lookups, do the targeted research here against the profile sources.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
