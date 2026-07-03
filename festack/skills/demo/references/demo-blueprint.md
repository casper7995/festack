# demo blueprint

The artifact `/demo` produces and renders. Fill every section. This is the pre-build design. No asset is built until this blueprint is reviewed and approved.

## Spine (fits one screen)

- **Audience.** Who is in the room, and the business / technical split.
- **The one belief.** "After this demo, they believe ___." One sentence. If you cannot write it, you are not ready to design.
- **The aha moment.** The single moment that earns the belief.
- **Constraints.** Time slot, live or recorded, their data or synthetic, the environment it runs in.

## Story arc

The demo as a narrative in 3 to 5 beats. Each beat states what they see, what it proves, and why they care. It builds tension and resolves it. A feature tour is not a story.

## Run of show

A minute-by-minute table for the live slot.

| Time | Beat | What runs | What you say | Fallback if it breaks |
|------|------|-----------|--------------|-----------------------|

Includes a buffer. The total fits the slot with room to spare.

## Asset map

Each asset to build, with its job and its outline.

- **Asset.** Notebook, app, script, slide, or sandbox.
- **Job.** Which beat it serves.
- **Outline.** The ordered sections. For a notebook, the markdown narration plan and each cell's purpose. The demo should read as a story with clear narration between steps, not a wall of code.

## Data and environment

- **Data.** Synthetic, de-identified, or client-provided. Which sensitive fields are masked on screen.
- **Environment.** What must exist before the demo: accounts, resources, access.
- **Setup.** Ordered, repeatable steps to stand it up.

## Determinism

Non-deterministic steps frozen for the live run. Pinned versions, cached acceptable outputs. Nothing that can surprise you in the room.

## Impact number

The headline metric, with a stated baseline, the assumption behind it, and the source. No undefended multiplier.

## Path to production

The credible step from this demo to the client running it for real. Not a one-off trick.

## Open decisions

Genuine forks still open, each with a named owner and a default. Decided items live in the spine, not here.
