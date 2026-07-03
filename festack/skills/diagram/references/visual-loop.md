# the visual feedback loop

The reason `/diagram` exists. Manual diagram polish eats hours because the author cannot see their own diagram with fresh eyes. This loop replaces that with render, look, critique, refine, in a few bounded rounds.

## The loop

1. **Render.** Produce the diagram in the chosen tool.
2. **Capture.** Get an image of the rendered diagram. Use a browser automation tool to screenshot it when one is available, otherwise export to PNG or SVG and open it. You must look at the actual rendered output, not the source.
3. **Critique.** Stress the rendered image against the diagram rubric (in the `review-work` skill, `references/deliverable-rubrics.md`). Run it multi-model via `/review-work` when the host can pass the image to reviewers, otherwise review the image yourself and let the panel review the source and structure. Weight a problem higher when more than one reviewer flags it.
4. **Refine.** Apply the highest-signal fixes. Re-render.
5. **Stop.** End when the diagram passes the rubric or another round returns only diminishing fixes. Bound to 2 or 3 rounds. Endless polishing is the thing this loop exists to prevent.

Spend the full panel on round 1 and on the final client-facing or high-stakes round. Intermediate rounds should use a lighter delta critique focused only on what changed unless blockers remain: one reviewer or the parent checks the changed regions against the same rubric, confirms the prior blockers were fixed, and avoids relitigating settled layout choices.

## What to critique (from the diagram rubric)

- **Truthfulness.** Every box and line is real. No invented components.
- **Reading order.** One primary path, left to right or top to bottom.
- **Density.** Right altitude for the audience. Not a wiring schematic, not a cartoon.
- **Spacing.** No overlaps, minimal crossings, even rhythm.
- **Labels and legend.** Components, flows, and trust boundaries labeled. Any color coding explained.
- **Client styling.** Consistent, intentional, not default-tool clutter.

## Truthfulness gate before final export

Before the final render, validate the technical story separately from visual polish. A polished but wrong diagram is worse than a rough correct one.

- [ ] Every node comes from the stated source of truth or is explicitly marked `proposed`.
- [ ] Every edge is a technically possible relationship. Label what it is: data flow, control flow, request/response, dependency, ownership, or migration.
- [ ] Directionality matches the story: sources precede entry points, processing precedes storage or serving, and consumers do not appear upstream unless the flow is an explicit callback or feedback loop.
- [ ] Components sit in the right boundary or group: actor, client, edge, application, data, control plane, external dependency, or environment.
- [ ] Current-state and future-state items are visually distinct. Proposed or migration paths are not drawn as live production paths.
- [ ] Unknowns are not hidden. Resolve them, remove them, or annotate them as open.

## Layout fixes (tool-agnostic)

| Problem | Fix |
| --- | --- |
| Nodes cramped | Increase node and rank separation |
| Arrows overlap | Orthogonal or polyline edges |
| Arrows cross | Reorder nodes, or switch direction (TB vs LR) |
| Too dense to read | Raise the altitude, or split into two diagrams |
| No focal point | Group related nodes, weight the primary path |
| Looks like a default | If the user requested client or profile styling, apply it; otherwise use a neutral palette, consistent spacing, and clean typography. Align and distribute. |

## Layout control baseline

For engines with explicit layout controls, reach for these knobs before manually dragging shapes.

| Intent | Generic control | Common attribute names | Starting point | Change when |
| --- | --- | --- | --- | --- |
| Reading direction | Layout direction | `rankdir`, `direction` | `LR` for flows, `TB` for stacks | The story reads against the arrows |
| Horizontal spacing | Node separation | `nodesep`, node gap | 1.0 to 1.5 | Nodes cramp or labels collide |
| Vertical spacing | Rank separation | `ranksep`, layer gap | 1.5 to 2.0 | Edge labels overlap or layers blur |
| Edge routing | Connector style | `splines`, route style | `ortho` or `polyline` for technical diagrams | Arrows cross, curve oddly, or obscure labels |
| Outer whitespace | Canvas padding | `pad`, margin | 0.5 to 1.0 | The export feels clipped or crowded |
| Text legibility | Font sizes | `fontsize`, label size | nodes 12, edges 10, title 14+ | Text is unreadable at final display size |
| Export quality | Raster resolution | `dpi`, scale | 150 for screen, 300 for print | The target is slides, print, or high-res docs |

## Capture protocol

The capture step is what makes the critique real. A critique of diagram source is weak; a critique of the rendered image is strong. Capture the diagram in the form the audience will actually see.

- Open the exported image or rendered canvas, not the source.
- Capture the full diagram and a downscaled view at the expected doc or slide size.
- Check that labels, arrowheads, legends, and boundary names stay readable after scaling.
- Prefer a white or transparent background unless the downstream surface needs otherwise.
- If the source exports both SVG and PNG, inspect the PNG too; rasterization can change line weights, font fallback, and label wrapping.
