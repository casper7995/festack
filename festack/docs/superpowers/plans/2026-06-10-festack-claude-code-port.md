# festack Claude Code Port Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make festack a first-class Claude Code plugin from the same source tree, replacing model-family diversity with lens diversity and the opus-workers/fable-judge/haiku-checks role mapping.

**Architecture:** One host-adaptive source tree. The `festack-debate` engine reads a per-host model config (`~/.cursor/rules/festack-models.mdc` on Cursor, `~/.claude/festack/models.md` on Claude Code) and assigns each panel worker a distinct lens from a new `lenses.md`. Skills are prose, so cross-cutting renames (AskQuestion) are handled by one authoritative alias definition in `decision-gates.md`, not 25 file edits. Contract tests in `tests/test_contracts.py` enforce the port invariants.

**Tech Stack:** Markdown skills (Cursor/Claude Code/Codex `SKILL.md` format), Python `unittest` contract tests, bash installer, Claude Code plugin manifest (`.claude-plugin/`).

**Spec:** `docs/superpowers/specs/2026-06-10-festack-claude-code-port-design.md`

**Repo note:** The repo's only commit is the spec (`d0c714e`); the plugin source is untracked. Task 0 baselines it so every later diff is reviewable.

---

### Task 0: Baseline the existing source

**Files:**
- Modify: none (git only)

- [ ] **Step 1: Baseline commit of the current Cursor plugin**

```bash
cd <path-to-festack-repo>
git add -A
git commit -m "chore: baseline Cursor plugin before Claude Code port"
```

- [ ] **Step 2: Verify clean tree**

Run: `git status -sb`
Expected: `## main` with no changes.

---

### Task 1: Contract tests for the port (TDD — written first, all failing)

**Files:**
- Modify: `tests/test_contracts.py` (append a new test class at the end, ~line 683)

- [ ] **Step 1: Append the port contract tests**

```python
class ClaudeCodePortContractTests(unittest.TestCase):
    """Invariants from docs/superpowers/specs/2026-06-10-festack-claude-code-port-design.md."""

    CURSOR_SLUG = re.compile(r"gpt-5\.5|composer-2\.5|gemini-3\.1|claude-opus-4-8")
    # The only files allowed to name Cursor model slugs.
    SLUG_ALLOWED = {"skills/setup-models/SKILL.md", "skills/festack-debate/SKILL.md"}

    def _all_md(self):
        for base in ("skills", "agents"):
            for path in sorted((ROOT / base).rglob("*.md")):
                yield str(path.relative_to(ROOT)), path.read_text(encoding="utf-8")

    def test_no_cursor_slugs_outside_allowed_files(self) -> None:
        offenders = [
            rel for rel, text in self._all_md()
            if rel not in self.SLUG_ALLOWED and self.CURSOR_SLUG.search(text)
        ]
        self.assertEqual(offenders, [], "Cursor model slugs leaked outside setup-models/festack-debate")

    def test_cursor_config_path_always_paired_with_claude_path(self) -> None:
        offenders = [
            rel for rel, text in self._all_md()
            if "festack-models.mdc" in text and "~/.claude/festack/models.md" not in text
        ]
        self.assertEqual(offenders, [], "files naming the Cursor model config must show the Claude Code path too")

    def test_gate_tool_alias_defined(self) -> None:
        text = read("skills/festack-debate/references/decision-gates.md")
        self.assertIn("AskUserQuestion", text)

    def test_lenses_exist_and_engine_references_them(self) -> None:
        lenses_path = ROOT / "skills/festack-debate/references/lenses.md"
        self.assertTrue(lenses_path.exists())
        lenses = lenses_path.read_text(encoding="utf-8")
        for lens in (
            "risk-first skeptic", "pragmatist", "customer-advocate",
            "correctness", "client-readiness", "feasibility",
        ):
            self.assertIn(lens, lenses)
        engine = read("skills/festack-debate/SKILL.md")
        self.assertIn("references/lenses.md", engine)
        self.assertIn("lenses:", engine, "Panel attestation must include a lenses field")

    def test_setup_models_has_claude_defaults(self) -> None:
        text = read("skills/setup-models/SKILL.md")
        self.assertIn("~/.claude/festack/models.md", text)
        for line in (
            "debate-runners: opus, opus, opus",
            "review-reviewers: opus, opus, opus",
            "synthesizer: fable",
            "evaluator: haiku",
            "classifier: haiku",
        ):
            self.assertIn(line, text)

    def test_readme_documents_claude_plugin_install(self) -> None:
        text = read("README.md")
        self.assertIn("/plugin marketplace add", text)
        self.assertIn("~/.claude/festack/models.md", text)
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `python3 -m unittest tests.test_contracts.ClaudeCodePortContractTests -v`
Expected: FAIL — `test_no_cursor_slugs_outside_allowed_files` (slugs in autopilot + decision-gates), `test_lenses_exist...` (no lenses.md), `test_setup_models_has_claude_defaults`, `test_readme_documents_claude_plugin_install`, `test_cursor_config_path_always_paired_with_claude_path`, `test_gate_tool_alias_defined` all fail. (Pre-existing tests still pass.)

- [ ] **Step 3: Commit**

```bash
git add tests/test_contracts.py
git commit -m "test: contract tests for Claude Code port invariants"
```

---

### Task 2: Lenses file + engine update (festack-debate)

**Files:**
- Create: `skills/festack-debate/references/lenses.md`
- Modify: `skills/festack-debate/SKILL.md` (Step 0 ~line 18, fan-out steps ~lines 35 and 47, attestation block ~lines 67-75, reference list ~line 79)

- [ ] **Step 1: Create `skills/festack-debate/references/lenses.md`**

```markdown
# panel lenses

On a single-provider host every panel worker runs the same model family, so disagreement
comes from the lens, not the family. Each runner or reviewer gets exactly one lens,
prepended to its shared prompt. Never give two workers on the same panel the same lens.
On multi-family hosts, vary lens and family together.

## Runner lenses (synthesize mode)

- **risk-first skeptic.** Assume the plan fails. Lead with what breaks, what is irreversible,
  and what the client would punish. Prefer the approach that degrades most gracefully.
- **pragmatist.** MVP-first. Optimize for the smallest thing that proves value this week
  with the team and tools that actually exist. Defer anything speculative.
- **customer-advocate.** Argue from the client's seat. Optimize for their stated success
  criteria, their audience, and their politics, not for technical elegance.

## Reviewer lenses (critique mode)

- **correctness.** Are the claims true, the numbers right, the citations real, the
  reasoning sound? Hunt for anything a sharp client could falsify.
- **client-readiness.** Is this the right shape for the named audience: tone, structure,
  length, jargon, and the so-what on top? Would you present it tomorrow?
- **feasibility.** Can this actually be delivered: effort, dependencies, permissions,
  platform limits, timeline? Flag anything that assumes capabilities not in evidence.

Panels larger than three reuse the list with a stated secondary emphasis. Panels of two
drop the lens least relevant to the question, and say which one was dropped.
```

- [ ] **Step 2: Replace the Step 0 opening paragraph in `skills/festack-debate/SKILL.md`**

Replace (line 18):

```
Read the host's model-role config for the role to model mapping. In Cursor this is `~/.cursor/rules/festack-models.mdc`; other hosts use their supported guidance files. Skills reference role keys, never hardcode slugs. The keys below are the canonical keys, and they match the lines `/setup-models` writes exactly.
```

with:

```
Read the host's model-role config for the role to model mapping. Skills reference role keys, never hardcode slugs. The keys below are the canonical keys, and they match the lines `/setup-models` writes exactly.

| Host | Model config |
| --- | --- |
| Cursor | `~/.cursor/rules/festack-models.mdc` |
| Claude Code | `~/.claude/festack/models.md` |
| Codex | `AGENTS.md` / `config.toml` |
```

- [ ] **Step 3: Replace the fallback table and add the lens rule**

Replace (lines 20-28):

```
If a role line is absent, use these fallbacks (diverse families on purpose):

| Role key | Fallback models |
| --- | --- |
| `debate-runners` | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` |
| `review-reviewers` | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` |
| `synthesizer` | `claude-opus-4-8-thinking-high` |

Default panel size is 3. Use 2 for narrow questions and 4 for high-stakes, contested ones.
```

with:

```
If a role line is absent, use these fallbacks:

| Role key | Cursor fallback (diverse families) | Claude Code fallback |
| --- | --- | --- |
| `debate-runners` | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `review-reviewers` | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `synthesizer` | `claude-opus-4-8-thinking-high` | `fable` |

Every panel worker also gets a distinct lens from `references/lenses.md`. Different lens
per worker always; different model family too when the host offers more than one. On a
single-provider host the lens is the diversity.

Default panel size is 3. Use 2 for narrow questions and 4 for high-stakes, contested ones.
```

- [ ] **Step 4: Update both fan-out steps**

In synthesize mode step 2 (line 35), replace:

```
Each is a `Task` running the `festack-agent` worker with a different `model` from the `debate-runners` role.
```

with:

```
Each is a `Task` running the `festack-agent` worker with a `model` from the `debate-runners` role and a distinct runner lens from `references/lenses.md` prepended to its prompt.
```

and at the end of that same step, replace:

```
Diversity of model family is the point. Do not run the same model N times.
```

with:

```
Diversity is the point: never repeat a lens on one panel, and vary the model family too when the host has more than one. The same model N times with the same prompt is not a panel.
```

In critique mode step 2 (line 47), replace:

```
Each is a `Task` running the `festack-agent` worker with a different `model` from the `review-reviewers` role, addressed the same way as in synthesize.
```

with:

```
Each is a `Task` running the `festack-agent` worker with a `model` from the `review-reviewers` role and a distinct reviewer lens from `references/lenses.md`, addressed the same way as in synthesize.
```

- [ ] **Step 5: Add `lenses` to the attestation block and the reference list**

In the Panel attestation block, after `- model roles:` add the line `- lenses:`.
In `## Reference files`, add:

```
- [references/lenses.md](references/lenses.md): the per-worker lenses that make panels diverse on single-provider hosts.
```

- [ ] **Step 6: Run the lens contract test**

Run: `python3 -m unittest tests.test_contracts.ClaudeCodePortContractTests.test_lenses_exist_and_engine_references_them -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add skills/festack-debate
git commit -m "feat: lens-based panel diversity and per-host model config in festack-debate"
```

---

### Task 3: Lens slots in the runner and reviewer prompts

**Files:**
- Modify: `skills/festack-debate/references/runner-prompt.md:3,7`
- Modify: `skills/festack-debate/references/reviewer-prompt.md:3`

- [ ] **Step 1: Update runner-prompt.md**

Replace (line 3):

```
Use this as the shared instruction for every synthesize runner. The parent appends the framed question and the context below it. Every runner gets the same frame. Only the model family differs.
```

with:

```
Use this as the shared instruction for every synthesize runner. The parent prepends the runner's assigned lens from `references/lenses.md`, then appends the framed question and the context below it. Every runner gets the same frame. Only the lens, and the model when the host has more than one, differ.
```

Replace (line 7):

```
You are one of several independent designers answering the same question. You do not see the other designers. Produce your own best answer. Do not hedge toward a safe middle. Commit to a position and defend it.
```

with:

```
You are one of several independent designers answering the same question. You do not see the other designers. Argue from your assigned lens: it is your starting bias and your evaluation priority, not a costume. Produce your own best answer. Do not hedge toward a safe middle. Commit to a position and defend it.
```

- [ ] **Step 2: Update reviewer-prompt.md**

Replace (line 3):

```
The shared prompt every critique reviewer receives. The calling skill passes this plus the draft and the combined rubric (base rubric plus the per-deliverable rubric). Each reviewer is one `festack-agent` worker on a different model.
```

with:

```
The shared prompt every critique reviewer receives. The calling skill passes this plus the draft, the combined rubric (base rubric plus the per-deliverable rubric), and the reviewer's assigned lens from `references/lenses.md`. Each reviewer is one `festack-agent` worker on a distinct lens, and on a different model when the host has more than one.
```

- [ ] **Step 3: Commit**

```bash
git add skills/festack-debate/references
git commit -m "feat: lens slots in runner and reviewer prompts"
```

---

### Task 4: Host-aware `/setup-models`

**Files:**
- Modify: `skills/setup-models/SKILL.md` (defaults table ~lines 17-21, step 1 ~line 37, step 4 ~lines 49-70, notes)

- [ ] **Step 1: Make the role table host-aware**

Replace the `Default` column header and values (lines 15-21) so the table reads:

```
| Role | What it does | Wants | Cursor default | Claude Code default |
| --- | --- | --- | --- | --- |
| `debate-runners` | The synthesize panel. Each runner proposes an independent candidate, then the candidates are merged. | Diverse lenses, diverse families where available. Disagreement is the point. | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `review-reviewers` | The critique panel. Each reviewer red-teams a draft against a rubric. | Diverse lenses, adversarial. | `gpt-5.5-high-fast`, `claude-opus-4-8-thinking-high`, `composer-2.5-fast` | `opus` ×3, one lens each |
| `synthesizer` | The single judgment-and-prose model that merges the panel into one package. | Strong reasoning and writing. | `claude-opus-4-8-thinking-high` | `fable` |
| `evaluator` | A fast done / not-done correctness judge at phase boundaries. Used by `/autopilot`. | Fast, cheap, decisive. | `gpt-5.5-high-fast` | `haiku` |
| `classifier` | The cheapest role. Triages an ambiguous fork as observable / reversible / genuine when the orchestrator cannot settle it inline. Used by `/autopilot` and any decision gate. | Cheapest and fastest. Quality matters less than throughput. | `composer-2.5-fast` | `haiku` |
```

Immediately after the table, replace the diversity paragraph (line 23) with:

```
The placement principle: anything that exercises judgment or produces what the client sees
runs the strongest model in the session (`fable` on Claude Code); parallel exploration runs
frontier workers (`opus`); high-frequency checks run the cheapest model (`haiku`). On Cursor,
panel diversity comes from model families; on single-provider hosts it comes from the lenses
in `festack-debate/references/lenses.md`, so a one-family panel is fine there and the lens
assignment is what must not repeat. `evaluator` and `classifier` are always the cheapest
fast model, because they run often.
```

- [ ] **Step 2: Make step 1 (read the ground) host-aware**

Replace (line 37):

```
Read the host's model-role config if it exists to show current mappings. In Cursor this is `~/.cursor/rules/festack-models.mdc`; other hosts use their supported guidance/config files. The available Cursor model families are typically: `gpt-5.5-high-fast`, `gpt-5.5-high`, `gpt-5.5-extra-high-fast`, `gpt-5.5-extra-high`, `claude-opus-4-8-thinking-high`, `claude-opus-4-8-thinking-xhigh`, `composer-2.5-fast`, `gemini-3.1-pro`. Confirm against what the user actually has if unsure.
```

with:

```
Detect the host first, then read its model-role config if it exists to show current mappings: Cursor `~/.cursor/rules/festack-models.mdc`, Claude Code `~/.claude/festack/models.md`, Codex `AGENTS.md` / `config.toml`. The available Cursor model families are typically: `gpt-5.5-high-fast`, `gpt-5.5-high`, `gpt-5.5-extra-high-fast`, `gpt-5.5-extra-high`, `claude-opus-4-8-thinking-high`, `claude-opus-4-8-thinking-xhigh`, `composer-2.5-fast`, `gemini-3.1-pro`. On Claude Code, use model aliases (`fable`, `opus`, `sonnet`, `haiku`), never dated slugs: the host resolves aliases to current models, so the config does not go stale. Confirm against what the user actually has if unsure.
```

- [ ] **Step 3: Make step 4 (write the config) host-aware**

After the existing Cursor `festack-models.mdc` block (ends ~line 68), add:

````
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
````

- [ ] **Step 4: Update the notes section**

Replace (line 78):

```
- This is the only festack file that names model slugs. If a slug changes or a model is retired, fix it here.
```

with:

```
- Role values live only in the host's model config; the only festack files that name model slugs or aliases are this skill and the `festack-debate` fallback table. If a model is retired, fix it here.
```

- [ ] **Step 5: Run the setup-models contract test**

Run: `python3 -m unittest tests.test_contracts.ClaudeCodePortContractTests.test_setup_models_has_claude_defaults -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add skills/setup-models
git commit -m "feat: host-aware setup-models with Claude Code role defaults"
```

---

### Task 5: AskQuestion alias + de-slug decision-gates and autopilot

**Files:**
- Modify: `skills/festack-debate/references/decision-gates.md:3,15`
- Modify: `skills/autopilot/SKILL.md:23,64`
- Modify: `skills/autopilot/references/autopilot-loop.md:15,40`

- [ ] **Step 1: Define the gate-tool alias once in decision-gates.md**

Replace (line 3):

```
festack work is decision-heavy. Business calls, stakeholder calls, and product calls run through it. AskQuestion is first-class. But asking the human about things you could check yourself is a tax. Classify every fork before you ask.
```

with:

```
festack work is decision-heavy. Business calls, stakeholder calls, and product calls run through it. AskQuestion is first-class. Throughout festack, `AskQuestion` means the host's structured question gate: the `AskQuestion` tool in Cursor, the `AskUserQuestion` tool in Claude Code, and the host prompt in Codex. Resolve it to your host's tool wherever a festack skill says `AskQuestion`. But asking the human about things you could check yourself is a tax. Classify every fork before you ask.
```

- [ ] **Step 2: De-slug the classifier mention in decision-gates.md**

Replace (line 15):

```
... spend one cheap call on the `classifier` role (default `composer-2.5-fast`) rather than a frontier model, or rather than reflexively interrupting the human.
```

with:

```
... spend one cheap call on the `classifier` role (the cheapest model in the host's model config) rather than a frontier model, or rather than reflexively interrupting the human.
```

- [ ] **Step 3: De-slug autopilot/SKILL.md**

Replace (line 23):

```
- Read the host's model-role config for model roles: `evaluator` for the per-phase correctness check (default `gpt-5.5-high-fast`), and `classifier` (cheapest, default `composer-2.5-fast`) for triaging ambiguous forks.
```

with:

```
- Read the host's model-role config for model roles: `evaluator` for the per-phase correctness check, and `classifier` (the cheapest configured model) for triaging ambiguous forks. `/setup-models` owns the per-host defaults.
```

Replace in line 64 the fragment:

```
that call goes to the `classifier` role (default `composer-2.5-fast`), not a frontier model
```

with:

```
that call goes to the `classifier` role (the cheapest model in the host's model config), not a frontier model
```

- [ ] **Step 4: De-slug autopilot-loop.md**

Replace in line 15 the fragment:

```
run a fast evaluator (the `evaluator` role from `festack-models.mdc`)
```

with:

```
run a fast evaluator (the `evaluator` role from the host's model config)
```

Replace in line 40 the fragment:

```
it spends the cheapest one: the `classifier` role (default `composer-2.5-fast`), never a frontier model
```

with:

```
it spends the cheapest one: the `classifier` role (the cheapest configured model), never a frontier model
```

- [ ] **Step 5: Run the slug and alias contract tests**

Run: `python3 -m unittest tests.test_contracts.ClaudeCodePortContractTests.test_no_cursor_slugs_outside_allowed_files tests.test_contracts.ClaudeCodePortContractTests.test_gate_tool_alias_defined -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add skills/festack-debate/references/decision-gates.md skills/autopilot
git commit -m "feat: gate-tool alias and role-based (slug-free) classifier/evaluator references"
```

---

### Task 6: Per-host model-config references in router, review-work, delivery agent

**Files:**
- Modify: `skills/festack/SKILL.md:15`
- Modify: `skills/festack/references/routing-table.md:37`
- Modify: `skills/review-work/SKILL.md:23`
- Modify: `agents/festack-delivery-agent.md` (Step 0, item 9)

- [ ] **Step 1: festack/SKILL.md**

Replace (line 15):

```
- Check the host's model-role config exists: Cursor `~/.cursor/rules/festack-models.mdc`, Claude Code `CLAUDE.md` or supported project guidance, Codex `AGENTS.md` / `config.toml`. If missing, suggest `/setup-festack` so profile, models, and capability wiring can be handled in one flow.
```

with:

```
- Check the host's model-role config exists: Cursor `~/.cursor/rules/festack-models.mdc`, Claude Code `~/.claude/festack/models.md`, Codex `AGENTS.md` / `config.toml`. If missing, suggest `/setup-festack` so profile, models, and capability wiring can be handled in one flow.
```

- [ ] **Step 2: routing-table.md**

Replace (line 37):

```
| Configure which models festack uses | `/setup-models` | Writes festack-models.mdc. |
```

with:

```
| Configure which models festack uses | `/setup-models` | Writes the host's model config (`festack-models.mdc` on Cursor, `~/.claude/festack/models.md` on Claude Code). |
```

- [ ] **Step 3: review-work/SKILL.md**

Replace (line 23):

```
- [ ] 1. Resolve festack-debate, load the base rubric and per-deliverable extension; read festack-models
```

with:

```
- [ ] 1. Resolve festack-debate, load the base rubric and per-deliverable extension; read the host's model config
```

- [ ] **Step 4: festack-delivery-agent.md Step 0 item 9**

Replace:

```
9. Read the host's model-role config for model roles: Cursor `~/.cursor/rules/festack-models.mdc`, Claude Code `CLAUDE.md` or host-supported project guidance, Codex `AGENTS.md` / `config.toml`.
```

with:

```
9. Read the host's model-role config for model roles: Cursor `~/.cursor/rules/festack-models.mdc`, Claude Code `~/.claude/festack/models.md`, Codex `AGENTS.md` / `config.toml`.
```

- [ ] **Step 5: Run the pairing contract test**

Run: `python3 -m unittest tests.test_contracts.ClaudeCodePortContractTests.test_cursor_config_path_always_paired_with_claude_path -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add skills/festack skills/review-work agents/festack-delivery-agent.md
git commit -m "feat: concrete Claude Code model-config path across router, review-work, delivery agent"
```

---

### Task 7: README — Claude Code install + portability table

**Files:**
- Modify: `README.md` (Install section ~line 178, Portability table ~line 233, Configuration model table ~line 116)

- [ ] **Step 1: Add the Claude Code install section**

After the Cursor install section (after line 202, `Add --copy on any host...`), insert:

````markdown
### Claude Code

festack ships a Claude Code plugin manifest (`.claude-plugin/plugin.json`) and a
single-plugin marketplace (`.claude-plugin/marketplace.json`). Install it as a plugin:

```
/plugin marketplace add <path-or-git-url-of-festack>
/plugin install festack@festack
```

Skills load namespaced (`festack:festack`, `festack:demo`, ...) and the
`festack:festack-agent` worker resolves exactly as `festack-debate` addresses it.
Update with `git pull` in the repo followed by `/plugin update festack`.

Fallback for environments where plugins are restricted:

```bash
scripts/install.sh claude --copy
```

Then run `/setup-models` once; on Claude Code it writes `~/.claude/festack/models.md`
with the defaults: `opus` panel workers, `fable` synthesizer, `haiku` evaluator/classifier.
````

- [ ] **Step 2: Update the configuration model table (line 116)**

Replace:

```
| Claude Code | `~/.claude/festack` | `CLAUDE.md` or host-supported project guidance |
```

with:

```
| Claude Code | `~/.claude/festack` | `~/.claude/festack/models.md` |
```

- [ ] **Step 3: Update the portability table (line 233) and subagent row (line 232)**

Replace:

```
| Model config file | `~/.cursor/rules/festack-models.mdc` (`alwaysApply`) | `CLAUDE.md` or skip | `AGENTS.md` / `config.toml` |
```

with:

```
| Model config file | `~/.cursor/rules/festack-models.mdc` (`alwaysApply`) | `~/.claude/festack/models.md` | `AGENTS.md` / `config.toml` |
```

Replace:

```
| Subagents | `Task` (Cursor model slugs) | `Task` (Claude model names) | subagents (Codex models) |
```

with:

```
| Subagents | `Task` (Cursor model slugs) | `Task` (Claude aliases: `fable`, `opus`, `haiku`) | subagents (Codex models) |
```

- [ ] **Step 4: Run the README contract test**

Run: `python3 -m unittest tests.test_contracts.ClaudeCodePortContractTests.test_readme_documents_claude_plugin_install -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: Claude Code plugin install path and updated portability tables"
```

---

### Task 8: Full test suite + installer checks

**Files:** none (verification only)

- [ ] **Step 1: Run the whole contract suite**

Run: `python3 -m unittest tests.test_contracts -v`
Expected: all tests PASS (pre-existing + `ClaudeCodePortContractTests`).

- [ ] **Step 2: Installer syntax and verify scripts**

```bash
bash -n scripts/install.sh
bash -n scripts/verify-install.sh
scripts/test.sh
```

Expected: exit 0 each.

- [ ] **Step 3: Canvas-fallback spot-check**

Run: `grep -rLi 'fallback\|markdown\|written artifact\|structured handoff' $(grep -rl 'canvas' skills agents --include='SKILL.md' --include='*.md' -l)`

For each listed file, open it and confirm the canvas mention either states or inherits a non-canvas fallback (most defer to the owner skill or `visual_artifact_receipt`, which already names `prose`/`structured handoff` — that counts). Only edit a file if it *requires* canvas with no path for hosts without one; add ", or a written Markdown/HTML artifact on hosts without a canvas tool" at that mention.

- [ ] **Step 4: Commit any straggler fixes (only if Steps 1-3 forced changes)**

```bash
git add -A && git commit -m "fix: address contract-suite findings"
```

---

### Task 9: Live smoke test in Claude Code (manual, in-session)

**Files:** none

- [ ] **Step 1: Install the plugin**

In Claude Code: `/plugin marketplace add <path-to-festack-repo>` then `/plugin install festack@festack`, restart the session.

- [ ] **Step 2: Routing smoke test**

Run `/festack` with: "answer a quick product question for a client". Expected: routes to `/client-debug` with a Routing receipt, no setup crash (first run may suggest `/setup-festack` — accept and complete it; verify it writes `~/.claude/festack/models.md` with the opus/fable/haiku defaults).

- [ ] **Step 3: Panel smoke test**

Run `/review-work` on any short draft doc. Expected: Panel attestation reports `worker count: 3`, model roles resolving to `opus`, three distinct `lenses`, and a fable synthesizer; findings are deduped with overlap counts.

- [ ] **Step 4: Record results**

Report pass/fail of Steps 2-3 to Casper. Any failure goes through superpowers:systematic-debugging before patching.
