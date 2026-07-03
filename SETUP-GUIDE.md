# festack

Shareable install repo for **festack**: a vendor-neutral workflow stack for Solution Architects and Field Engineers. This repo contains the plugin source, config templates, and install helpers. It does **not** include anyone's personal profile, engagements, or company-specific capability wiring.

## What's inside

```
festack/
├── SETUP-GUIDE.md          ← detailed setup instructions
├── install.sh              ← one-command install (Cursor, Claude Code, or Codex)
├── festack/                ← plugin source (skills, agents, hooks, scripts)
└── config-templates/       ← starter files for first-time setup
    ├── profile-template.md
    ├── festack-models.cursor.mdc
    ├── festack-models.claude.md
    ├── capabilities-*.yaml
    └── cursor-hooks.merge.json
```

## Prerequisites

- **Cursor** (recommended), **Claude Code**, or **Codex**
- `bash` and `git`
- macOS or Linux (Windows: use WSL or run `install.sh` with `--copy`)

## Quick start (Cursor)

1. Clone this repo:

   ```bash
   git clone https://github.com/casper7995/festack.git
   cd festack
   ```

2. Run the installer:

   ```bash
   ./install.sh cursor
   ```

3. Reload Cursor: **Developer → Reload Window**.
4. In chat, type `/setup-festack` and follow the guided setup (profile, model roles, optional capability wiring).
5. Type `/festack` to confirm the front door loads.

## Quick start (Claude Code)

```bash
./install.sh claude
```

Then in Claude Code:

```
/plugin marketplace add https://github.com/casper7995/festack.git
/plugin install festack@festack
```

Run `/setup-festack` once. On Claude Code, `/setup-models` writes `~/.claude/festack/models.md`.

Fallback when plugins are restricted:

```bash
./install.sh claude --copy
```

## Quick start (Codex)

```bash
./install.sh codex
```

Run `/setup-festack` once after install.

## What the installer does

`install.sh` symlinks (or copies with `--copy`) festack skills and agents into the host's config directory:

| Host   | Skills / agents target              | Plugin manifest                    | Hooks target              |
|--------|-------------------------------------|------------------------------------|---------------------------|
| Cursor | `~/.cursor/skills`, `~/.cursor/agents` | `~/.cursor/plugins/local/festack` | `~/.cursor/festack/hooks` |
| Claude | `~/.claude/skills`, `~/.claude/agents` | (use plugin marketplace)           | `~/.claude/festack/hooks` |
| Codex  | `~/.codex/skills`, `~/.codex/agents`   | —                                  | `~/.codex/festack/hooks`  |

Then reload the host and run `/setup-festack`.

## First-time configuration

`/setup-festack` is the recommended path. It coordinates three layers:

| Layer | File | Purpose |
|-------|------|---------|
| Profile | `$FESTACK_HOME/profile.md` | Role, platform, sources, audience, voice |
| Models | Host model config (see below) | Multi-model panel roles |
| Capabilities | `$FESTACK_HOME/capabilities.md` or `.yaml` | Map neutral workflows to your MCP/skills |

**Config roots by host:**

| Host | `$FESTACK_HOME` default | Model config |
|------|-------------------------|--------------|
| Cursor | `~/.cursor/festack` | `~/.cursor/rules/festack-models.mdc` |
| Claude Code | `~/.claude/festack` | `~/.claude/festack/models.md` |
| Codex | `~/.codex/festack` | `AGENTS.md` / `config.toml` |

Starter templates are in `config-templates/`. Copy and edit them, or let `/setup-festack` write them interactively.

### Capability registry samples

Pick the sample closest to your stack and copy it to `$FESTACK_HOME/capabilities.yaml`:

- `capabilities-databricks.yaml` — Databricks field team (Glean, Salesforce, Databricks MCP, etc.)
- `capabilities-cursor-ai.yaml` — Cursor AI field team
- `capabilities-openai.yaml` — OpenAI field team

Adjust provider names to match the skills and MCP servers installed in your host.

## Optional: engagement ledger hooks (Cursor)

festack can watch outbound sends (email, Drive, Slack) and append awareness receipts to engagement ledgers. This is optional but recommended for client-facing work.

1. After install, hooks live at `~/.cursor/festack/hooks/`.
2. Merge `config-templates/cursor-hooks.merge.json` into `~/.cursor/hooks.json` (create the file if missing).
3. Set `FESTACK_ORG_DOMAIN` in the hook environment (e.g. `yourcompany.com`) so external vs internal recipients are detected correctly.

## Verify install

From the `festack/` directory:

```bash
festack/scripts/verify-install.sh cursor   # or claude / codex
```

All skills and agents should show `OK`.

## Command cheat sheet

| Command | What it does |
|---------|--------------|
| `/festack` | Front door — routes to one skill or the delivery agent |
| `/setup-festack` | One-command setup and repair |
| `/personalize` | Update profile only |
| `/setup-models` | Update model-role mapping |
| `/setup-capabilities` | Wire company MCP/skills to neutral capabilities |
| `/scope-and-align` | Align on vision, success criteria, deliverable |
| `/demo` | Design a customer demo (before build) |
| `/autopilot` | Build after design is approved |

Full command palette: see `festack/README.md`.

## Sharing this package

- Safe to share: the plugin source and blank templates contain no personal or client data.
- Do **not** bundle someone's filled-in `profile.md`, `engagements/`, or `capabilities.yaml` unless you intend to share that configuration explicitly.
- Recipients should run `/setup-festack` to create their own profile.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `/festack` not in slash menu | Reload window; confirm `~/.cursor/skills/festack/SKILL.md` exists |
| Multi-model panels fail | Run `/setup-models`; confirm model slugs match your host |
| Split engagement ledger | Point both hosts at one `FESTACK_HOME` (export in shell profile) |
| Hooks silent on outbound sends | Merge `cursor-hooks.merge.json`; set `FESTACK_ORG_DOMAIN` |

## Version

Packaged from festack plugin source. See `festack/README.md` and `festack/.cursor-plugin/plugin.json` for plugin metadata.
