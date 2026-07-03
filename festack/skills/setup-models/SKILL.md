---
name: setup-models
description: Configure festack model roles for debate runners, reviewers, synthesizer, evaluator, and classifier.
disable-model-invocation: true
---

# /setup-models

festack runs work across several models on purpose. Different families disagree, and disagreement is the signal. This skill decides which model plays which role and writes it where the engine reads it.

The engine (`festack-debate`) and the skills reference roles, never model slugs. Slugs and aliases live only in the host's model config and the `festack-debate` fallback table.

## Roles

| Role | What it does | Wants | Cursor default | Claude Code default |
| --- | --- | --- | --- | --- |
| `debate-runners` | The synthesize panel. Each runner proposes an independent candidate, then the candidates are merged. | Diverse lenses, diverse families where available. Disagreement is the point. | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `review-reviewers` | The critique panel. Each reviewer red-teams a draft against a rubric. | Diverse lenses, adversarial. | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `synthesizer` | The single judgment-and-prose model that merges the panel into one package. | Strong reasoning and writing. | `claude-opus-4-8-thinking-high` | `fable` |
| `evaluator` | A fast done / not-done correctness judge at phase boundaries. Used by `/autopilot`. | Fast, cheap, decisive. | `gpt-5.5-high-fast` | `haiku` |
| `classifier` | The cheapest role. Triages an ambiguous fork as observable / reversible / genuine when the orchestrator cannot settle it inline. Used by `/autopilot` and any decision gate. | Cheapest and fastest. Quality matters less than throughput. | `composer-2.5-fast` | `haiku` |

The placement principle: anything that exercises judgment or produces what the client sees
runs the strongest model in the session (`fable` on Claude Code); parallel exploration runs
frontier workers (`opus`); high-frequency checks run the cheapest model (`haiku`). On Cursor,
panel diversity comes from model families; on single-provider hosts it comes from the lenses
in `festack-debate/references/lenses.md`, so a one-family panel is fine there and the lens
assignment is what must not repeat. `evaluator` and `classifier` are always the cheapest
fast model, because they run often.

## Workflow

```
- [ ] 1. Read current config and the available models
- [ ] 2. Present roles with recommended defaults
- [ ] 3. Confirm or customize per role
- [ ] 4. Write the host's model config
- [ ] 5. Confirm and show what was written
```

### 1. Read the ground

Detect the host first, then read its model-role config if it exists to show current mappings: Cursor `~/.cursor/rules/festack-models.mdc`, Claude Code `~/.claude/festack/models.md`, Codex `AGENTS.md` / `config.toml`. The available Cursor model families are typically: `gpt-5.5-high-fast`, `gpt-5.5-high`, `gpt-5.5-extra-high-fast`, `gpt-5.5-extra-high`, `claude-opus-4-8-thinking-high`, `claude-opus-4-8-thinking-xhigh`, `composer-2.5-fast`, `gemini-3.1-pro`. On Claude Code, use model aliases (`fable`, `opus`, `sonnet`, `haiku`), never dated slugs: the host resolves aliases to current models, so the config does not go stale. Confirm against what the user actually has if unsure.

### 2. Present the roles

Show the role table with the recommended defaults and one line on what each role does. Explain why the panels are diverse on purpose. Diversity comes from model families on Cursor and from lenses on single-provider hosts.

### 3. Confirm or customize

Use `AskQuestion`. Offer "accept the recommended defaults" as one option, and "customize per role" as another. If they customize, ask role by role, keeping the diversity guidance in front of them. This is a genuine preference call, so ask rather than decide. Keep panel lists at three entries unless the user also changes panel size; the engine pairs each slot with a lens by position.

Use `allow_multiple: true` for panel roles (`debate-runners` and `review-reviewers`) because they intentionally take several models. Use single-select for `synthesizer`, `evaluator`, and `classifier`, because each is one role owner.

### 4. Write the config

Write to the host's model-role config. In Cursor, write `~/.cursor/rules/festack-models.mdc` in this exact shape so the engine can parse it:

```
---
alwaysApply: true
description: festack model-per-role mapping. Read by the festack-debate engine and festack skills.
---

# festack models

One role per line. Panels take a comma-separated list. The engine reads these; skills never hardcode slugs.

debate-runners: gpt-5.5-high-fast, claude-opus-4-8-thinking-high, composer-2.5-fast
review-reviewers: gpt-5.5-high-fast, claude-opus-4-8-thinking-high, composer-2.5-fast
synthesizer: claude-opus-4-8-thinking-high
evaluator: gpt-5.5-high-fast
classifier: composer-2.5-fast
```

Substitute the user's chosen models. Keep the role keys exactly as written, the engine matches on them.

In Claude Code, write `~/.claude/festack/models.md` (create the directory if needed) in this shape:

```
# festack models

One role per line. Panels take a comma-separated list; the engine pairs each panel slot
with a lens from festack-debate/references/lenses.md by position. Aliases only, no dated slugs.

debate-runners: opus, opus, opus
review-reviewers: opus, opus, opus
synthesizer: fable
evaluator: haiku
classifier: haiku
```

### 5. Confirm

Show the written file. State that `festack-debate` reads it at Step 0 of every panel, and that absent roles fall back to the defaults baked into the engine.

## Notes

- Role values live only in the host's model config; the only festack files that name model slugs or aliases are this skill and the `festack-debate` fallback table. If a model is retired, fix it here.
- If `evaluator` or `classifier` lines are absent, fall back to the host's cheapest fast model: `composer-2.5-fast` on Cursor, `haiku` on Claude Code.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
