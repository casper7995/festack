---
name: festack
description: Canonical front door for festack. Route narrow FE asks to the right skill, or hand broad customer-delivery work to `festack-delivery-agent`.
disable-model-invocation: true
---

# /festack

The canonical entry point for festack. When you know exactly which skill you want, call it directly. When you just have a situation ("a client asked me to compare us to X", "I need to scope a demo for next week", "draw me their architecture"), start here. `/festack` either routes the narrow request to one skill or hands broad work to `festack-delivery-agent` to carry the task through the right playbook end to end.

## Step 0: orient

- Resolve `$FESTACK_HOME` first, with a real shell check (`echo "$FESTACK_HOME"`), never from memory. If unset, probe both host defaults (`~/.claude/festack`, `~/.cursor/festack`) for an existing `engagements/ENGAGEMENTS.md` and use the root that has one; only fall back to the current host's default (Cursor `~/.cursor/festack`, Claude Code `~/.claude/festack`, Codex `~/.codex/festack`) when neither exists. Never create a fresh engagements root while another host default already holds one.
- Engagement state and all ledger rules live in `references/ledger-lifecycle.md`; read it first, then read `$FESTACK_HOME/engagements/ENGAGEMENTS.md` if it exists and apply auto-dormant transitions to the index (last-touched 30+ days -> `dormant`).
- Read `$FESTACK_HOME/profile.md` for who the user is and what they represent. If it does not exist, this is a first run: offer `/setup-festack` before doing delivery work, since every skill leans on setup to stay vendor-neutral.
- Check the host's model-role config exists: Cursor `~/.cursor/rules/festack-models.mdc`, Claude Code `~/.claude/festack/models.md`, Codex `AGENTS.md` / `config.toml`. If missing, suggest `/setup-festack` so profile, models, and capability wiring can be handled in one flow.
- Resolve the installed `/festack` skill directory before reading references. Keep this portable for plugin installs: do not hardcode user-machine-specific absolute paths or assume a particular host's skill directory layout.
- Read the routing table from `references/routing-table.md` relative to the resolved `/festack` skill directory. If running from a package or source checkout instead of an installed skill, locate the package root that contains `skills/festack`, then read `skills/festack/references/routing-table.md`.
- Defer `references/capability-taxonomy.md`, `references/default-capability-registry.md`, `references/playbooks.md`, and `$FESTACK_HOME/capabilities.*` until broad orchestration is selected. Use those reference paths relative to the resolved `/festack` skill directory, or `skills/festack/references/...` from the package/source root. Narrow routes do not need the workflow engine.
- Know the two agents:
  - `festack-delivery-agent` is the end-to-end orchestrator for broad FE work.
  - `festack-agent` is the stateless worker for debate, review, research, and evaluator jobs. Do not use it as the main orchestration agent.

## Step 1: classify the intent

When the ask names an account, resolve engagement context first (Step 2.5); a live engagement's status and next step often change the route, so classify with that context loaded, not before it. Read what the user actually wants to accomplish, the deliverable or the decision, not the keywords. Map it to one skill using the routing table, and apply its disambiguation tie-breakers for the confusable clusters (`/scope-and-align` vs `/problem-frame` vs `/solution-critic`; `/discovery` vs `/client-debug`; `/doc` vs the research skills). Match on intent: "I need to show them it's faster" is a `/demo`; "is feature X supported?" is `/client-debug`; "which approach should we take?" is `/solution-critic`.

## Step 2: handle setup gaps

If the chosen skill needs setup and either profile or model config is missing, recommend `/setup-festack` as the single setup path, then return to the intended skill. Missing user capability wiring is not a setup blocker by itself; use default-only capability mode unless the user wants company providers or a required capability has no default provider. When the capability registry is absent but the profile declares external sources, note in `setup_state` that `/setup-capabilities` would wire them; one mention, never a block.

Do not let setup preflight block explicit setup or cleanup requests. `/setup-festack`, `/personalize`, `/setup-models`, `/setup-capabilities`, and `/fe-deslop` can run as narrow routes even if another setup file is missing; the owning skill handles its own prerequisites.

Before asking the user to restate "this", "that", "attached", or "the current ask", inspect available chat context, selected text, attached files, open files, and profile context. If the referenced artifact is not accessible, treat it as missing and ask for the minimum pointer or pasted content needed.

## Step 2.5: engagement context

Before routing, resolve which engagement this work belongs to, per
`references/ledger-lifecycle.md`:

- Match the ask against account names and aliases in the index. On a match, **announce
  the pick before anything else**: "**<slug> (<account>)** -- resuming. Last activity:
  <...>. Next step: <...>", then load the brief.md head only.
- On a name-stem collision (more than one match), hard-ask with one `AskQuestion`;
  never silently default. There is no single-active silent default: with one engagement
  the inference still matches and still announces.
- Bare `/festack` with no ask shows the index view: active engagements first, one line
  each with next steps, always ending with a dormant-count line ("dormant: 4, oldest
  quiet 47d: `lotte-eval`") so the Monday screen never shows a clean board when it
  isn't one.
- A named account **that is the subject of the work** with no matching engagement
  triggers auto-create: propose a slug inline, accept an override in the same breath,
  seed brief.md from current context, continue. A passing mention of another account
  never creates a ledger. Generic or unnamed work runs stateless; never force a ledger.
- `/festack log "<one sentence>"` captures out-of-band reality (calls, hallway Slack,
  customer files) per the Quick log rules in `references/ledger-lifecycle.md`: append a
  `quick-log` receipt to the active engagement, supersede contradicted brief facts,
  update the next step when named. Announce the engagement pick like any resume.
- In the index view, mark stale next steps from the index alone: when a row's
  `step-set` date predates its `last-touched`, append "(next step set <N>d ago)" so a
  stale plan reads as stale, not current. Skip the marker when `step-set` is absent;
  do not open log files just to compute staleness.
- `/festack resume <slug>` is the explicit fallback and follows the same announce rule.

## Step 3: route, orchestrate, or ask

- **One clear narrow match:** name the skill, say in one line why, and hand off to it. The chosen skill runs its own flow. Route directly only when exactly one skill fits after the tie-breakers.
- **Broad or lazy FE work:** run the `festack-delivery-agent` playbook. Use this when the user asks for an outcome rather than a single artifact, when the task spans multiple skills, or when they explicitly want `/festack` to take them through the work like a playbook. Examples: "prep me for this call", "scope and build a demo", "research the client, make the talk track, and review it", "help with this POC end to end".
- **Broad and ambiguous:** prefer `festack-delivery-agent` when the user wants an outcome that spans phases. Ask first only when the ambiguity changes the deliverable family itself, such as competitive demo vs battlecard vs POC.
- **Two or three plausible narrow routes:** ask once with `AskQuestion`, listing the candidate routes with a one-line description each. Emit a Gate receipt for the route decision, then hand off. Never route to a heavy workflow (`/demo`, `/poc`, `/autopilot`, `/scope-and-align`) on a weak guess; a wrong route there burns real time.
- **Competitive proof request:** if the ask is "prove we are better than X" or "make something competitive," reframe it as scoped, falsifiable differentiators. Route broad competitive proof assets to `festack-delivery-agent`; route a pure comparison to `/compete`.
- **Product question plus client-ready packaging:** if the ask names a packaged deliverable for a product question (an email, doc, slide, one-pager, or something to send the client), route to `festack-delivery-agent`. It should resolve `research.product_question` first, then package only after citations, confidence, and caveats are settled. Without a named deliverable it is a fact lookup; route directly to `/client-debug`, which can offer packaging afterward. Urgency or the answer being relayed onward does not upgrade a lookup.
- **Design plus render/package request:** if the ask combines design and a downstream artifact, such as "design the target architecture and draw it" or "create a diagram and put it into a client doc," route to `festack-delivery-agent`. It should sequence the design or producing skill first, then the rendering or packaging skill.
- **Build request with no design:** route to the right design skill first (`/demo`, `/poc`, `/solution-critic`), and tell the user `/autopilot` comes after the design is approved.
- **Approved build request:** route directly to `/autopilot` only when the approved design artifact or full approved-build payload is available. If approval is only asserted, the attachment is inaccessible, or the design payload is missing, pause for the artifact or route back to the design skill.

## Step 4: hand off cleanly

Pass the chosen skill or `festack-delivery-agent` the context you have gathered: the profile is read, model config is present, routing table and playbooks are read, capability registry state is known, setup gaps are handled, and intent is classified. Do not make the next layer re-interrogate the user for facts already in the profile.

Emit a Routing receipt before handoff so the FE can verify the router did not guess:

- `intent`: the user outcome in one sentence.
- `route`: chosen skill or `festack-delivery-agent`.
- `why`: one routing-table row or tie-breaker.
- `setup_state`: profile, model config, capability registry.
- `recommended_next_step`: the immediate next action after this receipt, usually the handoff itself; `none` only when the route fully answers the ask.
- `visual_artifact_receipt`: the surface the routed skill is expected to own (`canvas`, `docs-canvas`, structured handoff, or prose) and the owner. The router states the expectation; the owning skill confirms it at closeout.

Keep the receipt compact, and never let it delay the handoff. When the route is `festack-delivery-agent` running inline, skip this receipt and let the agent emit one combined receipt carrying these fields; two near-duplicate receipts are pure overhead.

For a narrow skill handoff, read and follow that skill's `SKILL.md`. "Hand off" means the next layer owns its workflow, not that `/festack` summarizes the answer itself.

If the narrow skill owns a panel (`/solution-critic`, `/review-work`, or `festack-debate`) and the current execution context cannot launch nested Task/subagent workers, keep the handoff inline at the top-level conversation. If you are already nested, return a parent-action gate with the exact panel or skill, framed question or draft, rubric or prompt inputs, expected mode and model role, and next step. Do not silently degrade the panel to one model.

When handing off to the delivery agent, use this shape:

```
You are `festack-delivery-agent`. Resolve the installed `/festack` skill directory, read its `SKILL.md`, then carry this FE task through the right festack playbook end to end.

User request: <request>
Profile loaded: <yes/no and any relevant summary>
Model config loaded: <yes/no>
Capability registry loaded: <markdown user registry / yaml user registry / default-only>
Initial classification: <likely playbook or ambiguity>
Known context: <facts already gathered>
Open gates: <decisions the human still owns, if any>
```

Choose the execution path by host capability:

- **Inline path for panel-heavy work:** if the selected playbook will need `/solution-critic`, `/review-work`, or `festack-debate` and the host cannot guarantee nested subagent fan-out, follow the delivery-agent instructions inline from the top-level conversation.
- **Primary-agent path:** address it as `festack:festack-delivery-agent` when the plugin namespace resolves and the host lets that agent continue using skills and panel fan-out.
- **Installed-agent fallback:** use the installed `festack-delivery-agent` from the host agents directory when namespace addressing does not resolve.
- **Inline fallback:** if the only available mechanism is a nested subagent that cannot launch nested Task/subagent panels, do not delegate. Read the installed `festack-delivery-agent` from the host agents directory or the repo `agents/festack-delivery-agent.md`, then follow it inline in the current conversation so `/solution-critic`, `/review-work`, and `festack-debate` can still fan out from the top level.
- **General fallback:** if none of the above resolves, use a general-purpose subagent and paste the delivery-agent role plus this handoff prompt unchanged, but require it to return panel requests to the parent rather than silently skipping them.

## Principles

- **Route or orchestrate, do not absorb.** Narrow requests go to one skill. Broad FE work goes to `festack-delivery-agent`. `/festack` itself does not become a giant workflow.
- **Playbooks before providers.** Broad work selects a playbook, then resolves capabilities to core or company providers.
- **Suggest the next useful step.** When a skill naturally produces a follow-on move, offer it explicitly. Do not force a workflow when the user only asked for a narrow answer.
- **Spend panels where judgment compounds.** Multi-agent review, critique, and synthesis are differentiators for client-facing, contested, or high-value work. Do not forget them, but do not tax every low-stakes step.
- **Use canvas when structure matters.** FE users need shared visual understanding. Prefer canvas for multi-part findings, diagrams, decision maps, and deliverables that are hard to scan in prose. On hosts without a canvas tool, render the same content as a written Markdown or HTML artifact; the structure is the point, not the tool.
- **Own one visual surface.** The deliverable owner renders the canvas; composed skills return structured results to the caller instead of stacking redundant canvases.
- **Keep the human in the loop.** Use `AskQuestion` for genuine scope, success, audience, risk, and approval decisions so the FE stays involved in the outcome.
- **Match on intent, not keywords.** What deliverable or decision are they after?
- **Specific over broad.** Hand off to the smallest skill that fits.
- **Fix setup gaps first.** A configured profile is what keeps every downstream skill vendor-neutral.
- **One good question beats a wrong guess.** Ask once when genuinely torn.
