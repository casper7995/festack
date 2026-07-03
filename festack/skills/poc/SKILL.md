---
name: poc
description: Scope a POC as a living contract with measurable success criteria, baselines, owners, risks, and a clear scope boundary.
disable-model-invocation: true
---

# /poc

Scope a proof of concept so it cannot quietly fail. Most POCs die one of two ways: scope creeps until it never ends, or the definition of "success" drifts until no one can say whether it worked. This skill kills both by writing a measurable contract up front and keeping it alive.

## Step 0: read config and profile

- Read `$FESTACK_HOME/profile.md` for what you represent, delivery defaults, and the profile-declared document target.
- Read the host's model-role config for model roles.
- If a `/scope-and-align` brief exists for this engagement, read it. The POC inherits the business context and success definition from it.
- Apply upstream brief inheritance: when a brief or prior context already settled the Goal, Audience, Success criteria, Belief to change, Judges, Decision unblocked, or Hard constraints, treat those fields as observable and do not re-ask.

## Step 1: establish what the POC must prove

Before any structure, get crisp on the spine:

- **The belief to change.** What does the client currently doubt that a successful POC would settle? "Can it handle our scale", "can it integrate with our stack", "is it actually faster".
- **Who judges.** Who decides this POC passed? That person's criteria are the only ones that count.
- **The decision it unblocks.** A purchase, an expansion, a migration. If a passing POC changes nothing, rescope it.

Use `AskQuestion` for these if they are genuinely open. They are usually the highest-value questions in the whole engagement. Do not re-ask goal, audience, success criteria, belief, judges, decision unblocked, or hard constraints that an upstream brief already answered; cite the inherited value and move on.

Use single-select for the belief to change and the decision the POC unblocks. Use `allow_multiple: true` when asking for judges, success criteria, in-scope items, out-of-scope items, risks, owners, or milestones, because those are sets.

## Step 2: force measurable exit criteria

Read `skills/poc/references/poc-doc.md`. The success-criteria table is the heart of the work.

For every criterion the client cares about, get four things: the metric, the current baseline, the target, and how it will be measured. **If there is no baseline, it is not a criterion yet.** Push back until each one is measurable. "Demonstrate good performance" becomes "process the sample in under N minutes against today's M-minute baseline".

This is where multi-model helps. If the success definition is fuzzy or contested, run a `festack-debate` synthesize pass with `debate-runners` to surface criteria the client and you might both be missing, then bring the genuine gaps to the human via `AskQuestion`.

## Step 3: draw the scope boundary

Fill the in-scope list and, just as deliberately, the out-of-scope list. The out-of-scope list is the document's main defense against creep. An empty out-of-scope section means the boundary was never drawn.

## Step 4: plan, risks, owners

Complete the rest of the document: approach (link a `/diagram` if one helps), phased plan with dates, named owners on both sides, and a risks-and-assumptions list where every risk has an owner and a mitigation.

## Step 5: review

- Run the document through `/review-work` with the doc rubric and the POC quality bar in the reference. The reviewer's first job is to attack every success criterion: is it truly measurable? does it have a baseline?
- Run all prose through `fe-deslop`.

## Step 6: render and set up the living loop

- Write the document to the profile-declared document target via the matching document skill. If no document target is configured, ask before creating local markdown; a POC contract usually wants to live somewhere both sides can see it.
- Render a canvas of the success-criteria table and scope boundary for fast shared understanding.
- Tell the human how to keep it alive: scope changes go in the doc with both sides aware, the decisions log accumulates, and at the end the criteria table is the verdict, met or not, per row.

## Step 7: gate the build

If the user wants to build POC assets after scope is approved, stop for one explicit `AskQuestion`: build now, revise the POC scope first, or stop at the contract.

Only after build approval, hand `/autopilot` the full approved-build payload:

- Approved artifact or pasted POC scope.
- Asset list or phase list.
- Acceptance checks derived from the POC success criteria.
- Target environment.
- Build adapter.
- Deploy/export target.
- Review status or explicit acceptance of review risk.
- Rollback or failure evidence expectations for deployed work.

Do not let a scoped POC turn into a build without those details.

## When the POC is running or ending

`/poc` also maintains. If invoked on an existing POC doc, update status against the criteria table, append to the decisions log, and never silently rewrite the original goal. If the POC is wrapping up, the criteria table becomes the result, and `/retro` turns the experience into lessons.

## Principles

- **No criterion without a baseline.** This single rule prevents most POC failures.
- **The out-of-scope list is the real work.** Saying no in writing is how you finish.
- **It is a contract, not a wishlist.** Both sides should recognize the definition of done.
- **Update, never reinterpret.** The goal set at the start is the goal you measure against.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
