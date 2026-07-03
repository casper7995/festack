---
name: setup-capabilities
description: Use when configuring which installed skills or tools provide festack workflow capabilities such as account research, usage lookup, document creation, diagrams, review, or approved builds.
disable-model-invocation: true
---

# /setup-capabilities

Capability setup maps neutral festack workflow needs to providers in the current environment. This is where company-specific plugin packs plug into core festack without changing the core skills.

## Inputs

Read, when available:

- `$FESTACK_HOME/profile.md` for adapter hints and source preferences.
- `$FESTACK_HOME/capabilities.md` or the advanced strict `$FESTACK_HOME/capabilities.yaml` for existing mappings.
- `references/capability-taxonomy.md` from the resolved `/festack` skill directory for canonical capability names. If running from a package or source checkout, use `skills/festack/references/capability-taxonomy.md` from the same package root.
- `references/default-capability-registry.md` from the resolved `/festack` skill directory for core defaults. If running from a package or source checkout, use `skills/festack/references/default-capability-registry.md` from the same package root.
- Installed skill names and available MCP servers/tools from the current host, if exposed.

Never copy credentials, tokens, account-specific confidential facts, or secrets into the registry.

Prefer `capabilities.md` for normal setup. Use `capabilities.yaml` only when the user wants stricter parsing. If both exist and conflict, ask whether to reconcile into Markdown, reconcile into YAML, or keep one and archive the other.

## Workflow

Open with this todolist.

```
- [ ] 1. Read taxonomy, defaults, profile, and existing registry
- [ ] 2. Detect provider candidates
- [ ] 3. Ask the user to accept or customize mappings
- [ ] 4. Write the capability registry
- [ ] 5. Confirm resolution behavior
```

### 1. Read the ground

Load the canonical capability list and default registry first. Then read the profile for adapter hints such as document writer adapters, diagram adapters, build adapters, and research sources.

If a registry already exists, treat this as an update. Do not erase mappings unless the user chooses to replace them.

### 2. Detect provider candidates

Inspect installed skill names where the host exposes them. Match candidates conservatively by capability:

| Capability | Candidate patterns |
| --- | --- |
| `research.account` | `discovery`, CRM, account research, enterprise search, internal search, customer notes |
| `research.product_question` | `client-debug`, product research, public docs, internal docs, support search, knowledge base, chat search |
| `research.competitor` | `compete`, competitive analysis, battlecard, market intelligence |
| `fetch.customer_usage` | usage, consumption, metrics, telemetry, analytics, billing |
| `fetch.open_risks` | issue tracker, blockers, support escalation, incidents, cases, delivery risks |
| `create.client_doc` | `doc`, document writer, docs-canvas, slides, collaborative doc |
| `create.diagram` | `diagram`, Figma, FigJam, tldraw, Mermaid, Lucid, Draw.io |
| `build.approved_scope` | `autopilot`, app builder, demo builder, notebook, bundle, sandbox, deployment |

Candidate matching proposes options only. It does not prove a provider is usable. MCP providers should use `mcp:<server>` for a tool family or `mcp:<server>/<tool>` for a specific tool.

Mark each provider as:

- `verified`: visible in installed skills/tools or otherwise reachable in the current host.
- `declared`: named by the profile or user, but not visible to the current host.

If no non-core provider candidates are detected, do not force capability setup. Tell the user core defaults are enough to start, and offer `/setup-capabilities` later when a company pack is installed.

### 3. Ask the user to accept or customize mappings

Use `AskQuestion`.

Use `allow_multiple: true` for additive provider capabilities where several providers can be useful:

- `research.account`
- `research.product_question`
- `research.competitor`
- `fetch.customer_usage`
- `fetch.open_risks`
- `create.client_doc`
- `create.diagram`

Use single-select for default owner capabilities where one provider should normally own the step:

- `frame.problem`
- `decide.approach`
- `design.demo`
- `scope.poc`
- `review.deliverable`
- `build.approved_scope`

Always include a skip/default option. A skipped capability falls back to the core default when one exists.

For capabilities with multiple selected providers, preserve order. The first provider is the owner unless the user marks providers as additive enhancers. Additive providers should all run when available and their outputs should be aggregated by the delivery agent.

### 4. Write the capability registry

Prefer `$FESTACK_HOME/capabilities.md` for readability. Use this shape:

```markdown
# festack capabilities

This file maps neutral festack workflow capabilities to installed providers in this environment.

## Capability providers

| Capability | Providers | Fallback | Notes |
| --- | --- | --- | --- |
| `research.account` | `/discovery`, `salesforce-actions`, `enterprise-search` | `/discovery` | CRM and internal docs are optional enhancers. |
| `research.product_question` | `/client-debug`, `mcp:user-docs/search`, `mcp:user-chat/search` | `/client-debug` | Product docs and internal chat can inform confidence; client citations must be shareable. |
| `fetch.customer_usage` | `mcp:user-usage/query` | ask | Usage data needs a company adapter. |
| `create.client_doc` | `/doc`, `mcp:user-docs/create`, `docs-canvas` | `/doc` | Pick target based on audience and requested format. |
```

Keep provider names as skill names or tool family names. Do not include secrets or environment-specific tokens.

When provider reachability is known, annotate it in notes: `verified` or `declared`.

If the user explicitly wants strict parsing, write `$FESTACK_HOME/capabilities.yaml` instead using:

```yaml
capabilities:
  research.account:
    preferred:
      - provider: /discovery
        type: core-skill
        when: default account research
    fallback: /discovery
```

### 5. Confirm resolution behavior

Summarize:

- Which capabilities use only core defaults.
- Which capabilities have company-specific providers.
- Which important capabilities are still missing providers.
- How `/festack` and `festack-delivery-agent` will use the registry.

## Notes

- This skill configures wiring, not profile facts. Use `/personalize` for profile facts.
- Run `/setup-festack` for the guided full setup experience.
- All prose follows `fe-deslop`.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
