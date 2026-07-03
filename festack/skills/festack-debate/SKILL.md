---
name: festack-debate
description: Internal engine for multi-perspective synthesize and critique passes used by other festack skills.
disable-model-invocation: true
---

# festack-debate

The shared reasoning engine for festack. Other skills call it. It has two modes.

- **synthesize**: explore a question across several independent runners, then merge into one package. Used by `/solution-critic`.
- **critique**: stress a draft across several adversarial reviewers against a rubric, then dedupe and rank. Used by `/review-work`.

Apply this engine where the work iterates heavily under human review (design debate, demo design, diagrams, research, contested alignment). Low-stakes steps stay single-model. Do not tax every step with a panel.

## Step 0: read the models

Read the host's model-role config for the role to model mapping. Skills reference role keys, never hardcode slugs. The keys below are the canonical keys, and they match the lines `/setup-models` writes exactly.

| Host | Model config |
| --- | --- |
| Cursor | `~/.cursor/rules/festack-models.mdc` |
| Claude Code | `~/.claude/festack/models.md` |
| Codex | `AGENTS.md` / `config.toml` |

If a role line is absent, use these fallbacks:

| Role key | Cursor fallback (diverse families) | Claude Code fallback |
| --- | --- | --- |
| `debate-runners` | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `review-reviewers` | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `synthesizer` | `claude-opus-4-8-thinking-high` | `fable` |

Every panel worker also gets a distinct lens from `references/lenses.md`, paired with its
panel slot by position (the first slot gets the first lens, and so on). Different lens
per worker always; different model family too when the host offers more than one. On a
single-provider host the lens is the diversity.

Default panel size is 3. Use 2 for narrow questions and 4 for high-stakes, contested ones.

## synthesize mode

Use when a skill needs the best version of a design, approach, or plan and the space has real alternatives.

1. **Frame the question.** State the one question the panel answers, the inputs they get, and the decision criteria. Pass the same frame to every runner.
2. **Fan out.** In one message, launch the panel in parallel. Each is a `Task` running the `festack-agent` worker with a `model` from the `debate-runners` role and a distinct runner lens from `references/lenses.md` prepended to its prompt. Address the worker as `subagent_type: "festack:festack-agent"` when the plugin is installed; if the host does not resolve that, use a `generalPurpose` subagent and paste the `festack-agent` role plus the runner prompt into its prompt unchanged. Give each runner the shared prompt in `references/runner-prompt.md` plus the framed question and context. Diversity is the point: never repeat a lens on one panel, and vary the model family too when the host has more than one. The same model N times with the same prompt is not a panel.
3. **Collect candidates.** Each runner returns a candidate in the structure named in the runner prompt (approach, key choices, trade-offs, risks, what would change the recommendation).
4. **Synthesize.** Merge into one package using `references/synthesis-template.md`. The synthesizer is a single judgment-and-prose model (synthesizer role). Record the synthesis decision: what was taken from each candidate, what was rejected, and why. Name the real forks that remain.
5. **Gate.** Apply the decision-gate convention in `references/decision-gates.md`. Resolve observable forks yourself. Reserve `AskQuestion` for genuine product, stakeholder, or preference calls.

The output is one merged package plus a short, honest record of disagreement. Never average the candidates into mush. Pick, justify, and keep the strongest dissent visible.

## critique mode

Use when a skill has a draft (a brief, a design, a doc, a diagram, a demo plan) and wants it stressed toward client-ready.

1. **Set the rubric.** Start from `references/critique-rubric-base.md`. The calling skill extends it with a per-deliverable rubric (a demo rubric, a diagram rubric, an alignment rubric).
2. **Fan out.** In one message, launch the reviewers in parallel. Each is a `Task` running the `festack-agent` worker with a `model` from the `review-reviewers` role and a distinct reviewer lens from `references/lenses.md` prepended to its prompt, addressed the same way as in synthesize. Give each the draft, the combined rubric, and the shared reviewer prompt in `references/reviewer-prompt.md` so every reviewer returns the same output structure and you can merge mechanically.
3. **Collect findings.** Each reviewer returns findings with severity, evidence, and a concrete fix.
4. **Dedupe and rank.** Merge findings with the Critique merge contract below. Weight overlaps higher (more than one reviewer found it). Resolve disagreements with judgment. Rank by severity and by distance from client-ready.
5. **Report.** Findings first, highest signal at top, each with evidence and a fix. State what is already strong so the human knows what not to touch. Include Panel attestation so the caller can verify whether the panel actually ran.

### Critique merge contract

Use a stable dedupe key for every finding: affected claim or section, failure mode, and proposed fix direction. Apply overlap weighting when multiple reviewers raise the same dedupe key; more independent reviewers means higher confidence and higher ranking inside a severity tier. Use severity reconciliation when reviewers disagree: keep the highest justified severity, but lower it if the evidence does not support the impact. The ranked output shape is:

- **Panel attestation:** mode, worker count, model roles, lenses, finding count, and fan-out status (`launched`, `blocked`, or `parent-action gate returned`).
- **Findings:** severity, dedupe key, overlap count, evidence, concrete fix, and residual risk if unfixed.
- **Already strong:** items reviewers agreed should not be changed.
- **Open human decisions:** only genuine trade-offs that need `AskQuestion`.

For synthesize mode, the same Panel attestation records mode, worker count, model roles, lenses, candidate count, and fan-out status.

### Panel attestation block

Every panel-backed output must include this block. If it is absent, treat the panel as incomplete and rerun it or return a parent-action gate.

```text
Panel attestation
- mode:
- worker count:
- model roles:
- lenses:
- candidate count:
- finding count:
- fan-out status:
```

## Reference files

- [references/runner-prompt.md](references/runner-prompt.md): shared prompt for synthesize runners.
- [references/synthesis-template.md](references/synthesis-template.md): structure for the merged package.
- [references/reviewer-prompt.md](references/reviewer-prompt.md): shared prompt and output contract for critique reviewers.
- [references/lenses.md](references/lenses.md): the per-worker lenses that make panels diverse on single-provider hosts.
- [references/critique-rubric-base.md](references/critique-rubric-base.md): base reviewer rubric that callers extend.
- [references/decision-gates.md](references/decision-gates.md): the classify-before-you-ask convention for AskQuestion.

## Prose

All engine output and everything the calling skills produce follows the `fe-deslop` skill.
