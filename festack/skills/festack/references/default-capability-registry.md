# default capability registry

This is the vendor-neutral fallback registry. It maps capabilities to core festack skills only. User or company-specific provider mappings belong in `$FESTACK_HOME/capabilities.md` or the advanced strict `$FESTACK_HOME/capabilities.yaml`.

Resolution priority:

1. User/company registry in `$FESTACK_HOME/capabilities.md`.
2. User/company registry in `$FESTACK_HOME/capabilities.yaml`, when selected for strict parsing or when Markdown is absent.
3. Default provider in this file.
4. Focused user gate if no provider exists.

If both user registries exist and disagree, run `/setup-capabilities` to reconcile them. A missing user registry is not an error; it means default-only mode.

## Defaults

| Capability | Default provider | Provider type | Notes |
| --- | --- | --- | --- |
| `research.account` | `/discovery` | core skill | Uses profile-declared sources. |
| `research.product_question` | `/client-debug` | core skill | Specific question, cited answer, confidence. |
| `research.competitor` | `/compete` | core skill | Fair comparison and proof framing. |
| `fetch.customer_usage` | none | external adapter needed | Ask for the installed provider or continue without usage data. |
| `fetch.open_risks` | none | external adapter needed | Ask for the installed provider or continue without risk data. |
| `frame.problem` | `/problem-frame` | core skill | Understand the problem before design. |
| `decide.approach` | `/solution-critic` | core skill | Debate competing approaches. |
| `align.scope` | `/scope-and-align` | core skill | Align audience, goal, success criteria, and scope. |
| `design.demo` | `/demo` | core skill | Design before build. |
| `scope.poc` | `/poc` | core skill | POC contract and measurable exit criteria. |
| `create.diagram` | `/diagram` | core skill | Diagram is the deliverable or downstream artifact. |
| `create.client_doc` | `/doc` | core skill | Client-facing writeup and packaging. |
| `review.deliverable` | `/review-work` | core skill | Rubric-based critique. |
| `build.approved_scope` | `/autopilot` | core skill | Requires full approved-build payload. |
| `learn.feedback` | `/learn` | core skill | Durable lessons and preferences. |
| `clean.prose` | `/fe-deslop` | core skill | Anti-slop prose cleanup. |

## Provider override format

When a user or company registry exists, prefer entries shaped like this:

```yaml
capabilities:
  research.account:
    preferred:
      - provider: /discovery
        type: core-skill
        when: "default account research"
      - provider: salesforce-actions
        type: company-skill
        when: "CRM account fields are needed"
    fallback: /discovery
```

Markdown registries can use equivalent tables. The delivery agent should read either format as instructions, not as executable code.

Providers can be core skills, company skills, or MCP providers. Use `mcp:<server>` when the server is a family of tools chosen at runtime, and `mcp:<server>/<tool>` when one MCP tool owns the capability.

## Missing provider behavior

Profile-declared sources and tools are hints, not provider mappings. A profile can say that CRM, usage data, internal search, or document tools exist, but the delivery agent should not treat those as callable providers unless `/setup-capabilities` mapped them into the capability registry.

`none` is an intentional missing-provider state, not an absent capability. It means the capability exists but core festack has no vendor-neutral provider for it.

For capabilities with `none` as the default provider:

- Ask for the provider only if the capability is required for the playbook outcome.
- Continue with an explicit caveat if the capability is helpful but optional.
- Never substitute a company-specific skill just because its name sounds plausible.

## Approved-build payload

`build.approved_scope` requires the same payload `/autopilot` requires:

- Approved artifact or pasted scope.
- Asset list or phase list.
- Acceptance checks.
- Target environment.
- Build adapter.
- Deploy or export target.
- Review status or explicit acceptance of review risk.
- Rollback or failure evidence expectations for deployed work.
