---
name: setup-festack
description: Use when setting up festack for the first time, repairing setup, or refreshing profile, model-role, and capability wiring configuration together.
disable-model-invocation: true
---

# /setup-festack

One guided setup flow for festack. Users should not have to know whether they need `/personalize`, `/setup-models`, or `/setup-capabilities` before they understand the stack.

## What it owns

`/setup-festack` coordinates setup. It does not duplicate every subflow.

- `/personalize` owns `$FESTACK_HOME/profile.md`.
- `/setup-models` owns the host's model-role config.
- `/setup-capabilities` owns `$FESTACK_HOME/capabilities.md` or the advanced strict `$FESTACK_HOME/capabilities.yaml`.

## Workflow

Open with this todolist.

```
- [ ] 1. Read current setup state
- [ ] 2. Recommend a setup path
- [ ] 3. Run or route to needed subflows
- [ ] 4. Verify the resulting setup
- [ ] 5. Confirm how `/festack` will use it
```

### 1. Read current setup state

Check whether these files exist and summarize them without exposing secrets:

- `$FESTACK_HOME/profile.md`
- the host's model-role config
- `$FESTACK_HOME/capabilities.md`
- `$FESTACK_HOME/capabilities.yaml`

Also inspect installed skill names when available so capability setup can propose real providers.

### 2. Recommend a setup path

Use `AskQuestion` with concise options:

- Accept recommended setup for missing sections.
- Refresh profile only.
- Refresh model roles only.
- Refresh capability wiring only.
- Customize all setup sections.
- Skip setup for now.

If this is a fresh setup, recommend profile and model roles first. Recommend capability wiring in the same flow only when non-core provider candidates are detected, profile adapter hints exist, or the user explicitly wants company/MCP provider wiring. If only one section is missing, recommend only that section.

### 3. Run or route to needed subflows

For each selected section:

- Profile: invoke `/personalize` and let it own the profile workflow.
- Model roles: invoke `/setup-models` and let it own model choices.
- Capabilities: invoke `/setup-capabilities` only when non-core provider candidates are detected, the user accepted adapter hints in the profile, or the user explicitly wants workflow wiring. Otherwise, use core default capabilities and mention `/setup-capabilities` as a later option.

Do not write a subflow's file directly from `/setup-festack` unless the user explicitly asks for a non-interactive repair and the needed values are already available.

### 3b. Prepare engagement storage

Before the verify step, ensure the engagement directory exists:

- Ensure `$FESTACK_HOME/engagements/` exists with an empty `ENGAGEMENTS.md` index (header row only). Mention once: pointing both hosts' `FESTACK_HOME` at one shared directory keeps engagements continuous across Cursor and Claude Code.

### 4. Verify the resulting setup

After the selected subflows finish, re-read setup state and check:

- Profile exists, or the user intentionally skipped profile setup.
- Model role config exists, or the user intentionally accepted built-in defaults.
- Capability registry exists, or the user intentionally accepted the default core registry.

If capability wiring is missing, say that core defaults will still work but company-specific providers will not be used automatically.

### 5. Confirm how `/festack` will use it

Explain the runtime split:

- `/festack` reads profile, model roles, playbooks, and capability registry during orientation.
- `festack-delivery-agent` chooses a playbook, resolves capabilities, then invokes the mapped providers.
- Company-specific skills stay outside core festack and plug in through capability mappings.

Keep the closeout short and practical: what exists, what was skipped, and what command to run later for a focused refresh.

## Notes

- This is the only recommended first-run setup command.
- Advanced users can still call `/personalize`, `/setup-models`, or `/setup-capabilities` directly.
- All prose follows `fe-deslop`.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
