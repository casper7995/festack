---
name: diagram
description: Create or polish a client-ready architecture, ERD, flow, sequence, or state diagram with visual review and refinement.
disable-model-invocation: true
---

# /diagram

A diagram is a client deliverable, and it usually eats more time than it should because polishing it by hand never ends. This skill compresses that. It frames the diagram, picks the tool, proposes the structure across models when the structure is non-obvious, and then iterates on the rendered image against a rubric until it is client-ready.

Truthfulness first. A beautiful diagram of an architecture that does not exist is worse than an ugly honest one.

## Workflow

Open with this todolist and work it in order.

```
- [ ] 1. Read the ground: diagram rubric, tool matrix, visual loop, decision-gates, models, profile
- [ ] 2. Frame the diagram
- [ ] 3. Choose the tool
- [ ] 4. Propose the structure (multi-model when non-obvious)
- [ ] 5. Render v1
- [ ] 6. Run the visual feedback loop
- [ ] 7. Render in canvas and export
- [ ] 8. Hand off
```

### 1. Read the ground

Read the diagram rubric in the `review-work` skill (`references/deliverable-rubrics.md`, diagram section), [references/tool-matrix.md](references/tool-matrix.md), and [references/visual-loop.md](references/visual-loop.md). Read the decision-gate convention in the `festack-debate` skill (`references/decision-gates.md`), the host's model-role config for panel models, and `$FESTACK_HOME/profile.md` for the preferred diagram tool and brand styling. Establish the source of truth for what you are drawing (an architecture, a data model, a flow). You draw only what is real or explicitly proposed.

If the request does not provide an actual architecture, label the work as a proposed reference architecture, not the client's current state. Gate this distinction before drawing when the diagram is client-facing: actual current state, proposed target state, or generic reference pattern.

### 2. Frame the diagram

State the type (architecture, ERD, flow, sequence, state), the audience and altitude, current vs future vs both, and the one thing the diagram must communicate. A diagram that tries to say five things says nothing. If the source of truth is missing or contradictory, resolve it before drawing. Resolve observable gaps yourself; when the audience, altitude, current-vs-future framing, or actual-vs-reference framing is a genuine call you cannot derive from the request or profile, gate it with one `AskQuestion` rather than guessing, because it reshapes the whole diagram.

If the request spans current and future state, choose the comparison pattern up front:

| Pattern | Use when | Rule |
| --- | --- | --- |
| Side-by-side panels | The audience compares architectures directly | Keep ordering, grouping, and scale consistent across panels |
| Delta overlay | Future state is a small change to current | Show only changed or added paths as proposed; keep existing paths quiet |
| Two-step sequence | The migration path matters more than the end states | Show current, transition, future as ordered steps |
| Separate diagrams | Both states are dense enough to compete | Split them, reuse the same legend and visual grammar |

### 3. Choose the tool

First detect what the host actually has: check for diagram-capable MCP connectors (Figma or FigJam, tldraw, draw.io, a Mermaid-chart or other diagram MCP) and local renderers (a Mermaid renderer, Graphviz). Then use the tool matrix to pick by diagram type, by the richest available tool for the client-readiness bar, and by the profile preference. For client-ready architecture diagrams, prefer an adapter that can produce both a polished export and editable/source handoff. Use Mermaid or Graphviz as the zero-dependency fallback or for fast, version-controlled work; use design or canvas MCPs when polish, editable collaboration, or visual QA matters more than source simplicity. If you choose an MCP-backed tool, load its companion skill first when the host requires one. Use `AskQuestion` only for a genuine fork the matrix and profile do not settle (editable file vs final image, polished-brand vs quick-and-clear). Tool and style choices are usually single-select. Export formats and downstream surfaces are additive, so use `allow_multiple: true` when asking for them. If the user has a richer tool you are not using, say why.

Use adapter quality without locking to a vendor. A diagram adapter is any available path that can do these jobs: validate setup, render, let you inspect the output, export at least one shareable format, and preserve editable source when possible. Examples are design MCPs, whiteboard MCPs, editable diagram tools, Mermaid renderers, Graphviz-based renderers, or profile-provided icon packs. Do not hardcode product icons, cloud brands, or company-specific templates into core festack; those belong in the profile or an adapter skill.

### 4. Propose the structure

For a non-obvious diagram (many components, unclear grouping, contested layout), invoke `festack-debate` in synthesize mode on the structure question: what to show, how to group, the reading order, the altitude. Converge on one structure with the dissent visible. For a simple diagram with one obvious shape, name the structure and skip the panel.

### 5. Render v1

Before rendering, run the adapter's setup check: confirm the tool exists, required auth is valid, required renderer commands or MCP methods are available, and requested icon or template assets exist. If the best adapter is unavailable, fall back one level in the tool matrix and say why. Produce the first version in the chosen tool. Keep the source (Mermaid text, diagrams code, or the tool's file) so iteration is cheap and the diagram is regenerable.

### 6. Run the visual feedback loop

Follow [references/visual-loop.md](references/visual-loop.md). Render, capture the actual rendered image (screenshot via a browser tool when available, else export and open), then critique the image against the diagram rubric. Run the critique multi-model via `/review-work` with the diagram rubric, passing the image to the reviewers when the host supports it. Apply the highest-signal fixes, re-render, and repeat. Bound it to 2 or 3 rounds. Stop when it passes the rubric or the fixes go marginal. This loop is the whole point, so do not skip the capture and review on the image itself.

Panel-spend rule: use a full panel on round 1 to catch structural misses and on the final round when the diagram is client-facing or high-stakes. For intermediate rounds, use a lighter delta critique focused only on what changed unless blockers remain or the audience is executive/client-critical.

### 7. Render in canvas and export

Render a canvas following the `canvas` skill: the diagram, the key structural decisions, the rejected layouts, any client or profile styling the user explicitly requested, and any open items. Export the diagram in the formats the downstream use needs (PNG for slides and docs, SVG for web, source for regeneration, an editable file when the client owns it).

If export fails, fix the adapter issue before handoff or explicitly downgrade the output format. Do not hand off only a screenshot when the user needed an editable file, and do not hand off only source when the user needed a slide-ready image.

### 8. Hand off

State what the diagram shows, what was decided, and anything still open. Return the source and the exported files. If this was called by `/scope-and-align`, `/demo`, or another builder, return the diagram package to it.

When the diagram is bound for a doc, slide, wiki, or deck, include an embedding handoff: recommended file (PNG for docs and slides, SVG for web or scalable review, source for regeneration, editable file when the recipient will own it), resolution (150 DPI screen, 300 DPI print or exec), placement (full-width when it is the main artifact, half-width only if labels stay readable), a short caption and alt text, and any open assumptions listed beside the diagram rather than hidden in the source.

## Notes

- The value is in the visual loop and the truthfulness bar, not in any one tool. Stay tool-agnostic and use what the host has.
- Use the structure panel only when the layout genuinely has alternatives. Do not tax a three-box flowchart with a debate.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
