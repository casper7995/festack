---
name: personalize
description: Build or update the festack profile with role, platform, sources, competitors, audiences, delivery defaults, and voice.
disable-model-invocation: true
---

# /personalize

festack skills stay vendor-neutral by pushing every specific into one profile. This skill builds that profile. It is what turns festack from a generic stack into yours: your platform, your research sources, your audience, your voice.

## Workflow

```
- [ ] 1. Read the schema and any existing profile
- [ ] 2. Mine recent transcripts for profile prefill candidates
- [ ] 3. Collect only the anchors still missing
- [ ] 4. Research and propose profile defaults
- [ ] 5. Ask the user to accept, trim, or skip the proposals
- [ ] 6. Write the profile
- [ ] 7. Confirm and point skills at it
- [ ] 8. Hand off to capability setup when adapter hints are present
```

### 1. Read the ground

Resolve `$FESTACK_HOME` first. Use the environment value when set; otherwise default by host: Cursor `~/.cursor/festack`, Claude Code `~/.claude/festack`, Codex `~/.codex/festack`. Read [references/profile-template.md](references/profile-template.md) for the schema. Read `$FESTACK_HOME/profile.md` if it already exists, and treat this as an update rather than a fresh start. Do not re-ask what is already filled.

### 2. Mine transcripts for prefill candidates

Before asking the user to answer setup questions, inspect recent agent transcripts when the host exposes them. In Cursor, use the current project's `agent-transcripts` context if available; on other hosts, use the equivalent recent conversation history if available. Keep this lightweight. The goal is prefill, not a full continual-learning pass.

Extract only durable profile candidates:

- Identity and role.
- Company / vendor and platform represented.
- Common audiences, delivery formats, demo asset types, research sources, adapter tools, and verification expectations.
- Recurring writing preferences and corrections that belong in the voice profile.
- Recurring competitive alternatives, differentiator themes, and proof-point categories.

Exclude secrets, credentials, account-specific confidential details, one-off customer facts, transient task state, temporary bugs, and anything seen only once unless the user explicitly stated it as a preference.

Do not write mined candidates directly to the profile and do not treat them as settled facts. Present them first with `AskQuestion`: use `allow_multiple: true` for additive candidates, and single-select or yes/skip choices for identity anchors and defaults. Each option should be short and evidence-backed, for example "Use Google Docs as a document target (seen in recent doc workflows)" or "Prefer concise prose with no em-dashes (recurring correction)." Anything the user does not accept stays blank.

### 3. Collect the irreducible anchors

Do not open with a long freeform questionnaire. Start with the few things you cannot safely infer:

- Name and role, if missing.
- Company / vendor and platform, if missing. This is the specific that is hardcoded nowhere else in festack.
- Any hard "do not assume this" preference the user wants honored.

Ask these conversationally only after transcript prefill. If the transcript mining produced a plausible value, confirm it with `AskQuestion` instead of asking the user to type it again. Keep it short. Let them skip anything. A partial profile is useful. Mark blanks as blank, do not invent.

### 4. Research and propose profile defaults

Once the company / vendor or platform is known, do a lightweight research pass before asking the user to enumerate everything manually. Use the shared research method from `festack-debate/references/research-method.md`: official docs first, then profile-declared internal sources if present, then recent credible public sources. Keep it bounded; this is setup, not a full `/discovery`.

Propose, with short evidence notes:

- Platform / stack and core capabilities.
- Likely differentiators and proof-point categories.
- Likely named competitors and adjacent alternatives for `/compete`.
- Public docs or knowledge sources that should be in the profile.
- Common client audiences, priorities, and objections for this company / platform.
- Sensible delivery defaults: demo asset types, output surfaces, canvas/docs preferences, document writer adapters, diagram adapters, build adapters, and verification defaults.

Do not write researched guesses directly as facts. Mark them as **proposed** until the user accepts them.

If the company is ambiguous (for example an acronym or a company with multiple products), ask one single-select `AskQuestion` to choose the right company/product before researching. If the user names a company that is not the vendor they represent (for example "my customer is X"), ask whether this profile is for the user's vendor or for a client context.

### 5. Ask the user to accept, trim, or skip the proposals

For finite choices, use batched `AskQuestion` with explicit options and a skip instead of another freeform prompt. Support multiple selection where the profile can hold more than one answer:

- **Multi-select (`allow_multiple: true`).** Typical client audience, client priorities, recurring objections, research source families, demo asset types, output surfaces, adapter skills/tools, verification checks, and delivery defaults. These are naturally additive, so do not force one answer.
- **Also multi-select.** Proposed core capabilities, differentiators, proof-point categories, and named competitors. These feed `/compete`, so let the user accept several or skip the ones that are wrong.
- **Single-select.** Default tone, sentence style, contractions, hedging, humor, formality, em-dash preference, and primary document target when the user must pick a default.

Keep the open-ended fields (what you sell, differentiators, voice samples, the why behind a stance) conversational. The line is simple: finite choices go in `AskQuestion`, additive finite choices use multiple selection, and tell-me-your-story stays in chat.

Ask for 2 to 3 writing samples after the finite setup choices. This is the strongest input for the `fe-deslop` skill, which reads the voice profile. If they skip samples, say the voice match will be weaker.

### 6. Write the profile

Write `$FESTACK_HOME/profile.md` following the schema. Preserve sections the user did not touch. Keep it readable, this file is meant to be edited by hand too.

Keep workflow wiring out of the profile. The profile can name adapter hints such as document writers, diagram tools, build tools, CRM, ticketing, chat, internal search, and usage data sources. It should not decide which provider owns a capability such as `research.account` or `fetch.customer_usage`; `/setup-capabilities` owns that mapping.

### 7. Confirm

Show what was written. Name which skills read it: `fe-deslop` reads the voice profile, `/scope-and-align` and `/demo` read audience and delivery defaults, and `/discovery`, `/client-debug`, and `/compete` read the resources and differentiators. Mention that `/learn` deepens the profile from real engagements over time.

### 8. Hand off to capability setup

If the user accepted adapter skills, tools, or source families, explain the next setup choice:

- Run `/setup-festack` for the normal full setup and repair flow.
- Run `/setup-capabilities` only if they want to wire adapter hints into capability providers now.

Use `AskQuestion` with options:

- Wire adapter hints now with `/setup-capabilities`.
- Run full `/setup-festack`.
- Stop after the profile update.

Default to `/setup-capabilities` when profile and model setup already exist. Default to `/setup-festack` when either is missing.

Do not write `$FESTACK_HOME/capabilities.md` or `capabilities.yaml` from `/personalize`. Capability wiring is a separate setup concern.

## Notes

- This is v1. It captures the profile cleanly but does not yet learn on its own. `/learn` (v2) closes that loop.
- The profile is the boundary between the vendor-neutral skills and the user's world. Everything company-specific belongs here, nowhere else.
- Capability provider mappings do not belong in the profile. Keep them in `/setup-capabilities`.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
