---
name: autopilot
description: Execute an approved scope autonomously with a canvas, todolist, phase checks, retry budget, and only genuine decision pauses.
disable-model-invocation: true
---

# /autopilot

Keep grinding. Once a scope is designed and approved, autopilot executes it end to end, pausing only for decisions a human must own. It is the build engine that sits downstream of the design skills, the answer to "the plan is good, now just make it real without checking in every five minutes".

## The one precondition: an approved design

Autopilot does not design. It executes a design that already exists. Before it starts, there must be an approved scope, ideally from `/demo`, `/poc`, `/solution-critic`, or `/scope-and-align`. If there is no design yet:

- If the work is small and the path is obvious, draft a quick scope and get one approval before building.
- If the work is non-trivial, stop and route to the right design skill first. Do not let autopilot invent the architecture as it goes.

If the user says the design is approved, verify the approval payload before building. Required payload: approved artifact or pasted scope, asset list or phase list, acceptance checks, target environment, build adapter, deploy/export target, review status, and rollback or failure evidence for deployed work. If any required part is missing, ask for the artifact or reconstruct a compact build scope and get explicit approval once before proceeding.

## Step 0: read config and profile

- Read `$FESTACK_HOME/profile.md` for delivery defaults and the build environment.
- Read the host's model-role config for model roles: `evaluator` for the per-phase correctness check, and `classifier` (the cheapest configured model) for triaging ambiguous forks. `/setup-models` owns the per-host defaults.
- Read `skills/autopilot/references/autopilot-loop.md` and `skills/festack-debate/references/decision-gates.md`. Follow both.

Detect the build adapter before decomposing work. A build adapter is any profile-declared or host-available skill/toolchain that can validate setup, create the artifact, run checks, export or deploy, and return evidence. It can be a notebook builder, app builder, slide/doc writer, diagram adapter, local code stack, test runner, or another FE workflow. Do not hardcode vendor-specific builders in core festack. If no adapter can build the approved scope, stop with a build-ready spec and the missing adapter requirements.

## Step 1: show the scope (canvas)

Render the approved scope in a canvas before building: what is being built, the success criteria, what is in and out of scope. This is the shared picture the human glances at while you grind. Confirm it matches their intent once. This is the build gate.

## Step 2: build the todolist

Decompose the scope into an exhaustive, ordered todolist of phases. Each phase needs:

- A concrete deliverable.
- An **acceptance check**: how you will know the phase is done and correct.
- Its dependencies (what must finish first).
- The adapter or tool that will execute it, when execution requires one.

Be thorough here. A vague todolist produces a vague grind. Use the `TodoWrite` tool so progress is visible.

## Step 3: grind, phase by phase

For each phase, follow the loop in the reference:

1. Validate the adapter for the phase: auth, workspace or file access, required commands, companion skill, and output path.
2. Build the phase.
3. Verify with the adapter's real evidence: tests, render, preview, export, deployment status, screenshot, or generated artifact.
4. Run the `evaluator` over just that phase's output: did it meet its acceptance check, did it create a problem for later, is there a genuine decision the human must make?
5. If it failed the check, retry within the budget (default 2). If still failing, stop and report what you tried and what you need.
6. If a genuine decision surfaced, stop and ask with `AskQuestion`. Otherwise, continue to the next phase.

Keep the canvas and todolist current the whole time. The human should be able to look in at any moment and understand exactly where things stand.

## Step 4: do not stop for things you can settle

This is what makes autopilot autopilot. Classify every fork before pausing:

- **Observable** (a fact you can check): resolve it yourself, run it or read it.
- **Reversible** (cheap to undo, low-stakes, and not client-visible): pick the sensible default, note it, keep moving.
- **Genuine** (irreversible, expensive, or real judgment): stop and ask.

**How the classification runs, cheaply.** Most forks are obvious; the orchestrator classifies them inline at no extra cost and keeps moving. That is the fast path. Only when a fork is genuinely ambiguous (you cannot tell whether it is reversible or genuine) do you spend a model call, and that call goes to the `classifier` role (the cheapest model in the host's model config), not a frontier model: pass it the fork, the three definitions, and the context, and have it return one of observable / reversible / genuine with a one-line reason. This keeps the frequent, latency-sensitive triage cheap and reserves the strong models for synthesize and critique. When still in doubt after the cheap pass, treat it as genuine and ask.

A fork is only reversible if it is all three: cheap to undo, low-stakes, and invisible to the client. Anything touching business intent, scope, stakeholders, audience, tone, or a client-visible preference is a genuine decision even when it is technically easy to change later. Route those to `AskQuestion`. Interrupting for truly observable or reversible forks defeats the purpose; settle those and grind on.

A genuine decision does not wait for the next phase boundary. If a destructive action, a scope change, or a real judgment call surfaces mid-phase, stop and ask at that moment.

When asking, use `allow_multiple: true` for additive build decisions such as files or phases to include, tests to run, acceptance checks to add, scope items to cut, or risks to accept. Use single-select for destructive approvals, one default path, or continue/stop/revise decisions.

## Step 5: budget and stop conditions

- **Per-phase retry budget:** default 2 retries. Past that, stop and report what you tried and what you need.
- **Global budget:** default cap of 12 phases or 20 total retries across the run, whichever comes first; for time-boxed runs, an elapsed-time cap the user sets. When the budget is exhausted, stop and summarize progress against the todolist instead of pushing past it. (The defaults are overridable in the profile.)
- Stop early and report if you are genuinely stuck, with the specific decision or input you need.

## Step 6: close out

When the todolist is complete:

- Run the final output through `/review-work` against the relevant rubric (demo, doc, design package).
- Run all prose through `fe-deslop`.
- Update the canvas to the finished state and summarize what was built against the original scope, including every default you picked along the way so the human can adjust.
- Offer a `/retro` to capture lessons from the run.

## Principles

- **Execute a design, do not invent one.** The build gate is non-negotiable.
- **Classify before you ask.** Settle observable and reversible forks; pause only for genuine ones.
- **Autonomous, not opaque.** Keep the canvas and todolist live so the grind is always legible.
- **Budgets beat loops.** Cap retries and the run; stop and report rather than thrash.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
