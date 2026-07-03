# diagram tool matrix

Pick the tool by diagram type first, then by what is available, then by the profile preference, then by how the diagram will be used downstream. All of these are vendor-neutral. Use whichever the host actually has.

## By diagram type

| Type | First choice | Why | Alternatives |
| --- | --- | --- | --- |
| ERD / data model | Mermaid `erDiagram` | Text-based, fast, version-controllable, imports to draw.io | draw.io, a diagrams-as-code ER tool |
| Flow / process | Mermaid `flowchart` | Quick, readable, easy to revise | draw.io, tldraw |
| Sequence | Mermaid `sequenceDiagram` | Purpose-built, clean | draw.io |
| State machine | Mermaid `stateDiagram` | Purpose-built | draw.io |
| Architecture (structured / system) | Diagrams-as-code (Graphviz-based) | Deterministic layout, grouping, repeatable source; can use profile-provided icon packs when explicitly requested | Mermaid for simple structures; Figma or tldraw for a polished one-off |
| Client-polished / brand | Figma | Design-system styling, presentation grade | tldraw |
| Freeform / whiteboard | tldraw | Collaborative, fast, loose | FigJam |
| Editable handoff | draw.io | Widely shareable, client can edit, imports Mermaid | Figma |

## Selection tiebreakers

| Need | Prefer | Avoid |
| --- | --- | --- |
| Regenerable architecture | Text or code-backed source | Manual-only layouts for systems that will change |
| Current/future comparison | A deterministic layout engine or duplicated frame | One mixed diagram where live and proposed paths look identical |
| Client-owned editing | An editable or import-friendly format | A flat image as the only deliverable |
| Precise visual polish | A design canvas or presentation tool | Fighting low-level syntax for brand or layout details |
| Dense sequence or protocol | A purpose-built sequence engine | Freeform boxes and arrows that hide ordering |
| Unknown downstream target | PNG plus SVG plus source | A single proprietary output |
| Import into another editor | Simple shapes, explicit edge colors, plain labels | Exotic shapes, HTML labels, or styling that may not survive import |

## Detect what is available, then pick

Before choosing, enumerate the diagramming tools this host actually has, then pick the richest one that fits the type and the client-readiness bar. Do not reach for Mermaid because it is familiar. Reach for it because nothing richer is present or the job is a fast internal sketch.

Discovery ladder (check each, use the best fit that is present):

1. **Design / canvas MCP (highest polish).** A Figma or FigJam connector for brand-grade, deck-ready, design-system work; a tldraw connector for collaborative or polished freeform. When one of these is present and the output is client-facing, prefer it. Load the tool's companion skill first if the host requires one (for example the Figma diagram, use, or FigJam skills).
2. **Editable-handoff MCP.** A draw.io or diagrams connector when the client must own and edit the file.
3. **Diagram MCP / renderer.** A Mermaid-chart MCP or any diagram MCP the host exposes; a local Mermaid renderer (mmdc, a render skill); a Graphviz / diagrams-as-code toolchain for deterministic structured architecture.
4. **Always-available fallback.** Mermaid source rendered by `mmdc`, or Graphviz `dot`. These need no MCP and are the zero-dependency baseline. A diagram you can render now beats a richer tool you do not have.

The rule: **MCP-rich tool (Figma, tldraw, draw.io) when the bar is client polish and the tool is present; Mermaid or Graphviz when the job is speed, version control, or nothing richer is available.** Whatever the tool, the visual feedback loop and the truthfulness bar are identical. The tool sets the polish ceiling, not the method. If the user has a tool you are not using, say why you skipped it.

## Output formats

- **PNG.** Docs and slides.
- **SVG.** Web, scalable, still editable in design tools.
- **Source** (Mermaid text, diagrams code). Regenerate and version-control.
- **draw.io / editable.** Hand to the client to own.

Ask the genuine preference (tool, editable vs final) only when type and profile do not already settle it.

## Adapter contract

Use any diagram adapter that satisfies the job; do not hardcode vendor-specific assets in core festack.

Every adapter must make these steps possible:

1. **Setup check.** Confirm the renderer, MCP, auth, companion skill, or local command is available before committing to it.
2. **Renderable source.** Keep a source representation where the tool supports it: diagram syntax, code, editable canvas, or tool-native file.
3. **Visual inspection.** Open or capture the rendered output so the visual loop reviews the actual artifact, not just source text.
4. **Export.** Produce the downstream format the user needs: slide-ready image, scalable web asset, editable file, and/or source.
5. **Troubleshooting path.** If rendering fails, diagnose setup, syntax, missing assets, unreadable labels, oversized layouts, and export incompatibility before switching tools.

Generic adapter patterns:

| Adapter | Setup check | Best for | Common failure | Fallback |
| --- | --- | --- | --- | --- |
| Design canvas MCP | Tool is connected, target file is writable, companion skill is loaded | Deck-ready polish, design-system styling | Auth or file permission failure | tldraw, draw.io, SVG/PNG export |
| Whiteboard MCP | Tool is connected and writable | Collaborative architecture or rough but polished flows | Loose layout gets too dense | Figma/design tool or Graphviz |
| Editable diagram tool | Tool or import path exists | Client-owned editable handoff | Styling lost on import | Simple Mermaid or SVG |
| Mermaid renderer | `mmdc` or equivalent renderer works | Flow, sequence, ERD, state, quick source-controlled diagrams | Syntax or layout crowding | Graphviz or editable tool |
| Graphviz / diagrams-as-code | Renderer works and any requested icon assets exist | Structured architecture and current/future comparisons | Missing renderer/icon or cramped layout | Mermaid for simple diagrams, design tool for polish |

Icon packs and templates come from the profile or chosen adapter. If none are declared, use neutral shapes and labels.
