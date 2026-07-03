import os
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def skill_names() -> set[str]:
    return {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}


def agent_names() -> set[str]:
    return {path.name for path in (ROOT / "agents").glob("*.md")}


def capability_rows(relative_path: str) -> set[str]:
    return set(re.findall(r"^\|\s*`([a-z_]+\.[a-z_]+)`\s*\|", read(relative_path), re.MULTILINE))


class FestackContractTests(unittest.TestCase):
    def test_test_runner_exists(self) -> None:
        runner = ROOT / "scripts" / "test.sh"
        self.assertTrue(runner.exists(), "scripts/test.sh should run all contract tests")
        self.assertTrue(os.access(runner, os.X_OK), "scripts/test.sh should be executable")

    def test_plugin_only_install_links_only_plugin_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            env = {**os.environ, "HOME": home}
            subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), "cursor", "--plugin-only"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertTrue((Path(home) / ".cursor/plugins/local/festack").exists())
            self.assertFalse((Path(home) / ".cursor/skills/festack").exists())
            self.assertFalse((Path(home) / ".cursor/agents/festack-agent.md").exists())

    def test_normal_cursor_install_links_skills_agents_and_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            env = {**os.environ, "HOME": home}
            subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), "cursor"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertTrue((Path(home) / ".cursor/plugins/local/festack").exists())
            self.assertTrue((Path(home) / ".cursor/skills/festack/SKILL.md").exists())
            self.assertTrue((Path(home) / ".cursor/agents/festack-agent.md").exists())
            self.assertTrue((Path(home) / ".cursor/agents/festack-delivery-agent.md").exists())

    def test_installer_supports_all_hosts_copy_mode_and_verification(self) -> None:
        for host, root_dir in [("cursor", ".cursor"), ("claude", ".claude"), ("codex", ".codex")]:
            with self.subTest(host=host), tempfile.TemporaryDirectory() as home:
                env = {**os.environ, "HOME": home}
                subprocess.run(
                    ["bash", str(ROOT / "scripts" / "install.sh"), host, "--copy"],
                    cwd=ROOT,
                    env=env,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                subprocess.run(
                    ["bash", str(ROOT / "scripts" / "verify-install.sh"), host, "--home", home],
                    cwd=ROOT,
                    env=env,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                skill_path = Path(home) / root_dir / "skills" / "festack" / "SKILL.md"
                self.assertTrue(skill_path.exists())
                self.assertFalse(skill_path.is_symlink())

    def test_installer_does_not_overwrite_non_festack_targets_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            target = Path(home) / ".cursor" / "skills" / "festack"
            target.mkdir(parents=True)
            sentinel = target / "OWNER.txt"
            sentinel.write_text("not festack\n", encoding="utf-8")

            result = subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), "cursor"],
                cwd=ROOT,
                env={**os.environ, "HOME": home},
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertTrue(sentinel.exists())
            self.assertIn("--force", result.stderr + result.stdout)

    def test_installer_force_replaces_unmanaged_targets(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            target = Path(home) / ".cursor" / "skills" / "festack"
            target.mkdir(parents=True)
            sentinel = target / "OWNER.txt"
            sentinel.write_text("not festack\n", encoding="utf-8")

            subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), "cursor", "--force"],
                cwd=ROOT,
                env={**os.environ, "HOME": home},
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertFalse(sentinel.exists())
            self.assertTrue((target / "SKILL.md").exists())
            self.assertTrue((Path(home) / ".cursor/plugins/local/festack").exists())

    def test_symlink_install_passes_verification(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            env = {**os.environ, "HOME": home}
            subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), "cursor"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                ["bash", str(ROOT / "scripts" / "verify-install.sh"), "cursor", "--home", home],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assertTrue((Path(home) / ".cursor/skills/festack").is_symlink())

    def test_verify_install_fails_when_required_links_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            result = subprocess.run(
                ["bash", str(ROOT / "scripts" / "verify-install.sh"), "cursor", "--home", home],
                cwd=ROOT,
                env={**os.environ, "HOME": home},
                capture_output=True,
                text=True,
            )

            output = result.stderr + result.stdout
            self.assertNotEqual(0, result.returncode)
            self.assertIn("MISS /festack", output)
            self.assertIn("Install incomplete", output)

    def test_shell_scripts_have_valid_syntax(self) -> None:
        for script in ["install.sh", "verify-install.sh", "test.sh"]:
            result = subprocess.run(
                ["bash", "-n", str(ROOT / "scripts" / script)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, f"{script}: {result.stderr}")

    def test_readme_explains_simple_setup_architecture_and_transferability(self) -> None:
        readme = read("README.md")

        for expected in [
            "## How festack works",
            "```mermaid",
            "## Simple setup",
            "1. Install the plugin.",
            "2. Reload the host.",
            "3. Run `/setup-festack`.",
            "Profile names sources. Capabilities make them callable.",
            "Databricks field team",
            "Cursor AI field team",
            "OpenAI field team",
            "samples/capabilities-databricks.yaml",
            "samples/capabilities-cursor-ai.yaml",
            "samples/capabilities-openai.yaml",
            "scripts/test.sh",
        ]:
            self.assertIn(expected, readme)

        self.assertNotIn("Compatibility aliases", readme)
        self.assertNotIn("`/solution`", readme)
        self.assertNotIn("`/festack-mode`", readme)

    def test_capability_registry_documents_mcp_provider_contract(self) -> None:
        files = [
            "README.md",
            "skills/festack/references/capability-taxonomy.md",
            "skills/festack/references/default-capability-registry.md",
            "skills/setup-capabilities/SKILL.md",
            "agents/festack-delivery-agent.md",
        ]

        for relative_path in files:
            content = read(relative_path)
            self.assertIn("mcp:<server>", content, relative_path)
            self.assertIn("mcp:<server>/<tool>", content, relative_path)

        delivery_agent = read("agents/festack-delivery-agent.md")
        self.assertIn("Read the tool schema first", delivery_agent)
        self.assertIn("Never infer MCP arguments from the provider name alone", delivery_agent)

    def test_host_neutral_config_paths_are_used_for_profile_capabilities_and_lessons(self) -> None:
        offenders = []
        forbidden = [
            "~/.cursor/festack/profile.md",
            "~/.cursor/festack/capabilities.md",
            "~/.cursor/festack/capabilities.yaml",
            "~/.cursor/festack/lessons.md",
        ]

        for base in ["skills", "agents"]:
            for path in (ROOT / base).rglob("*.md"):
                content = path.read_text(encoding="utf-8")
                for needle in forbidden:
                    if needle in content:
                        offenders.append(f"{path.relative_to(ROOT)} contains {needle}")

        self.assertEqual([], offenders)

    def test_no_vendor_specific_provider_examples_are_presented_as_setup_defaults(self) -> None:
        setup_capabilities = read("skills/setup-capabilities/SKILL.md")
        for vendor_specific in ["Databricks Apps", "Logfood"]:
            self.assertNotIn(vendor_specific, setup_capabilities)

    def test_company_starter_registries_document_provider_contracts(self) -> None:
        for company in ["databricks", "cursor-ai", "openai"]:
            content = read(f"samples/capabilities-{company}.yaml")
            self.assertIn("capabilities:", content)
            self.assertIn("auth_preflight:", content)
            self.assertIn("shareability:", content)
            self.assertIn("handoff:", content)
            self.assertIn("fallback:", content)
            self.assertIn("mcp:", content)

    def test_approved_build_payload_is_consistent_across_enforcement_points(self) -> None:
        required_terms = [
            "Approved artifact",
            "Asset list",
            "Acceptance checks",
            "Target environment",
            "Build adapter",
            "Deploy",
            "Review status",
            "Rollback",
        ]
        files = [
            "skills/autopilot/SKILL.md",
            "skills/demo/SKILL.md",
            "skills/poc/SKILL.md",
            "skills/festack/references/default-capability-registry.md",
            "skills/festack/references/playbooks.md",
            "skills/festack/references/routing-table.md",
        ]

        for relative_path in files:
            normalized = read(relative_path).lower()
            for term in required_terms:
                self.assertIn(term.lower(), normalized, f"{relative_path} missing {term}")

    def test_deprecated_compatibility_alias_skills_are_removed(self) -> None:
        for alias in ["festack-mode", "solution", "review"]:
            self.assertFalse((ROOT / "skills" / alias).exists(), f"deprecated alias /{alias} should be removed")

    def test_review_work_replaces_review_collision_and_keeps_panel_contract(self) -> None:
        self.assertIn("review-work", skill_names())

        review_work = read("skills/review-work/SKILL.md")
        self.assertIn("name: review-work", review_work)
        self.assertIn("# /review-work", review_work)
        self.assertIn("Run festack-debate critique", review_work)
        self.assertIn("fans out the reviewer panel", review_work)
        self.assertIn("AskQuestion", review_work)
        self.assertIn("canvas", review_work)
        self.assertIn("do not hardcode user-machine-specific absolute paths", review_work)
        self.assertIn("same resolved host skill root as `review-work`", review_work)
        self.assertIn("Do not rely on broad whole-home or glob-only searches", review_work)
        self.assertIn("Package/source fallback", review_work)
        self.assertIn("skills/festack-debate", review_work)
        self.assertIn("do not continue with a single-model review", review_work)
        self.assertIn("festack-debate/references/critique-rubric-base.md", review_work)
        self.assertIn("festack-debate/references/reviewer-prompt.md", review_work)

        for relative_path in [
            "README.md",
            "skills/festack/references/routing-table.md",
            "skills/festack/references/default-capability-registry.md",
            "skills/festack/references/capability-taxonomy.md",
            "skills/festack-debate/SKILL.md",
            "agents/festack-delivery-agent.md",
        ]:
            content = read(relative_path)
            self.assertIn("/review-work", content, relative_path)

    def test_experience_differentiators_are_explicit_but_conditional(self) -> None:
        readme = read("README.md")
        festack = read("skills/festack/SKILL.md")
        delivery_agent = read("agents/festack-delivery-agent.md")

        for phrase in [
            "Lazy front door",
            "Smart next steps",
            "Multi-model where it pays",
            "Canvas-first when structure matters",
            "Human-in-the-loop gates",
            "not forced into low-stakes steps",
        ]:
            self.assertIn(phrase, readme)

        for phrase in [
            "Suggest the next useful step",
            "Spend panels where judgment compounds",
            "Use canvas when structure matters",
            "Keep the human in the loop",
            "Do not force",
        ]:
            self.assertIn(phrase, festack)

        self.assertIn("Suggest the next useful skill or gate", delivery_agent)
        self.assertIn("Use canvas for multi-part understanding", delivery_agent)

    def test_fe_gates_use_askquestion_without_reasking_settled_brief(self) -> None:
        delivery_agent = read("agents/festack-delivery-agent.md")
        demo = read("skills/demo/SKILL.md")
        poc = read("skills/poc/SKILL.md")

        self.assertIn("Use `AskQuestion` for genuine decisions", delivery_agent)
        self.assertIn("brief inheritance", delivery_agent.lower())
        self.assertIn("do not re-ask", delivery_agent.lower())

        for relative_path, content in [
            ("skills/demo/SKILL.md", demo),
            ("skills/poc/SKILL.md", poc),
        ]:
            normalized = content.lower()
            self.assertIn("upstream brief", normalized, relative_path)
            self.assertIn("do not re-ask", normalized, relative_path)
            self.assertIn("goal", normalized, relative_path)
            self.assertIn("audience", normalized, relative_path)
            self.assertIn("success", normalized, relative_path)

    def test_brief_handoff_fields_are_consistent_and_skip_align_scope(self) -> None:
        files = {
            "brief": read("skills/scope-and-align/references/brief-template.md"),
            "delivery": read("agents/festack-delivery-agent.md"),
            "demo": read("skills/demo/SKILL.md"),
            "poc": read("skills/poc/SKILL.md"),
            "playbooks": read("skills/festack/references/playbooks.md"),
        }
        handoff_fields = [
            "Goal",
            "Audience",
            "Success criteria",
            "Belief to change",
            "Judges",
            "Decision unblocked",
            "Hard constraints",
        ]

        for label, content in files.items():
            normalized = content.lower()
            for field in handoff_fields:
                self.assertIn(field.lower(), normalized, f"{label} missing {field}")

        self.assertIn("Skip conditional `align.scope`", files["playbooks"])
        self.assertIn("skip conditional `align.scope`", files["delivery"].lower())

    def test_review_work_has_structured_residual_risk_gate(self) -> None:
        review_work = read("skills/review-work/SKILL.md")

        self.assertIn("single-select `AskQuestion`", review_work)
        for option in [
            "Apply all blocker and major fixes",
            "Fix blockers only and accept stated major risks",
            "Choose among competing fixes",
            "Stop and keep the residual risk",
        ]:
            self.assertIn(option, review_work)
        self.assertIn("record the specific residual finding", review_work)

    def test_critique_mode_has_merge_contract_and_panel_attestation(self) -> None:
        debate = read("skills/festack-debate/SKILL.md")
        review_work = read("skills/review-work/SKILL.md")
        delivery_agent = read("agents/festack-delivery-agent.md")
        reviewer_prompt = read("skills/festack-debate/references/reviewer-prompt.md")

        for phrase in [
            "Critique merge contract",
            "dedupe key",
            "overlap weighting",
            "severity reconciliation",
            "ranked output shape",
            "Panel attestation",
            "mode",
            "worker count",
            "model roles",
            "finding count",
        ]:
            self.assertIn(phrase, debate)

        self.assertIn("panel attestation", review_work.lower())
        self.assertIn("panel attestation", delivery_agent.lower())
        self.assertIn("Panel attestation block", debate)
        self.assertIn("treat the panel as incomplete", debate)
        self.assertIn("dedupe key", reviewer_prompt)

    def test_panel_owners_forbid_silent_single_model_downgrade(self) -> None:
        for relative_path in [
            "skills/festack/SKILL.md",
            "agents/festack-delivery-agent.md",
            "skills/review-work/SKILL.md",
            "skills/solution-critic/SKILL.md",
        ]:
            content = read(relative_path).lower()
            self.assertIn("do not silently degrade", content, relative_path)
            self.assertIn("parent-action gate", content, relative_path)

    def test_panel_spend_is_gated_in_compete_and_diagram(self) -> None:
        compete = read("skills/compete/SKILL.md")
        diagram = read("skills/diagram/SKILL.md")

        self.assertIn("single-panel default", compete)
        self.assertIn("extra adversarial critique", compete)
        self.assertIn("contested or high-stakes", compete)

        self.assertIn("full panel on round 1", diagram)
        self.assertIn("lighter delta critique", diagram)
        self.assertIn("final round", diagram)

    def test_canvas_ownership_and_trivial_escapes_are_documented(self) -> None:
        festack = read("skills/festack/SKILL.md")
        delivery_agent = read("agents/festack-delivery-agent.md")
        problem_frame = read("skills/problem-frame/SKILL.md")
        solution_critic = read("skills/solution-critic/SKILL.md")

        for relative_path, content in [
            ("skills/festack/SKILL.md", festack),
            ("agents/festack-delivery-agent.md", delivery_agent),
        ]:
            normalized = content.lower()
            self.assertIn("deliverable owner renders", normalized, relative_path)
            self.assertIn("composed skills return structured results", normalized, relative_path)

        for relative_path, content in [
            ("skills/problem-frame/SKILL.md", problem_frame),
            ("skills/solution-critic/SKILL.md", solution_critic),
        ]:
            normalized = content.lower()
            self.assertIn("trivial", normalized, relative_path)
            self.assertIn("offer the canvas", normalized, relative_path)

    def test_readme_does_not_overclaim_askquestion_frequency(self) -> None:
        readme = read("README.md")

        self.assertNotIn("Every nontrivial skill is Socratic and AskQuestion-driven", readme)
        self.assertIn("System 2 where it counts", readme)
        self.assertIn("reserve `AskQuestion` for genuine", readme)

    def test_operational_receipts_raise_fe_runtime_confidence(self) -> None:
        festack = read("skills/festack/SKILL.md")
        delivery_agent = read("agents/festack-delivery-agent.md")
        decision_gates = read("skills/festack-debate/references/decision-gates.md")
        playbooks = read("skills/festack/references/playbooks.md")
        routing_table = read("skills/festack/references/routing-table.md")
        canvas = read("canvases/festack-workflow.canvas.tsx")

        for relative_path, content in [
            ("skills/festack/SKILL.md", festack),
            ("agents/festack-delivery-agent.md", delivery_agent),
        ]:
            self.assertIn("Routing receipt", content, relative_path)
            self.assertIn("recommended_next_step", content, relative_path)
            self.assertIn("visual_artifact_receipt", content, relative_path)

        self.assertIn("Gate receipt", decision_gates)
        self.assertIn("Gate receipt", festack)
        self.assertIn("Gate receipt", delivery_agent)
        self.assertIn("Routing receipt", routing_table)
        self.assertIn("recommended_next_step", playbooks)
        self.assertIn("Gate receipt", playbooks)
        self.assertIn("setup_state", delivery_agent)

        self.assertNotIn("/Users/casper.hsieh/Projects/festack", canvas)
        self.assertIn("workflow canvas ships with the repo", read("README.md"))
        for journey in [
            "POC scope",
            "Competitive proof asset",
            "Architecture decision to diagram",
        ]:
            self.assertIn(journey, canvas)

    def test_runtime_reference_resolution_is_plugin_portable(self) -> None:
        festack = read("skills/festack/SKILL.md")
        delivery_agent = read("agents/festack-delivery-agent.md")
        review_work = read("skills/review-work/SKILL.md")
        setup_capabilities = read("skills/setup-capabilities/SKILL.md")

        for relative_path, content in [
            ("skills/festack/SKILL.md", festack),
            ("agents/festack-delivery-agent.md", delivery_agent),
        ]:
            self.assertIn("resolved `/festack` skill directory", content, relative_path)
            self.assertIn("package", content.lower(), relative_path)
            self.assertIn("do not hardcode user-machine-specific absolute paths", content, relative_path)
            self.assertNotIn("Read `festack/references/routing-table.md`", content, relative_path)
            self.assertNotIn("Read `festack/SKILL.md`", content, relative_path)
            self.assertNotIn("Cursor: `~/.cursor/skills`", content, relative_path)

        self.assertIn("references/routing-table.md", festack)
        self.assertIn("references/routing-table.md", delivery_agent)
        self.assertIn("skills/festack/references/routing-table.md", festack)
        self.assertIn("skills/festack", delivery_agent)
        self.assertIn("skills/festack/references/capability-taxonomy.md", setup_capabilities)
        self.assertIn("skills/festack/references/default-capability-registry.md", setup_capabilities)
        self.assertIn("caller already resolved the `/festack` skill directory or package root", review_work)

    def test_public_skills_have_closeout_receipts(self) -> None:
        exempt = {"festack", "festack-debate"}
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            if path.parent.name in exempt:
                continue
            relative_path = str(path.relative_to(ROOT))
            content = path.read_text(encoding="utf-8")
            self.assertIn("recommended_next_step", content, relative_path)
            self.assertIn("Gate receipt", content, relative_path)
            self.assertIn("visual_artifact_receipt", content, relative_path)

    def test_installer_removes_stale_review_alias_link(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            stale = Path(home) / ".cursor" / "skills" / "review"
            stale.parent.mkdir(parents=True)
            stale.symlink_to(ROOT / "skills" / "review")

            subprocess.run(
                ["bash", str(ROOT / "scripts" / "install.sh"), "cursor"],
                cwd=ROOT,
                env={**os.environ, "HOME": home},
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertFalse(stale.exists(), "installer should remove stale festack /review link")
            self.assertTrue((Path(home) / ".cursor" / "skills" / "review-work" / "SKILL.md").exists())

    def test_capability_registry_and_playbooks_share_one_taxonomy(self) -> None:
        taxonomy = capability_rows("skills/festack/references/capability-taxonomy.md")
        defaults = capability_rows("skills/festack/references/default-capability-registry.md")
        playbook_capabilities = set(
            re.findall(
                r"^\|\s*\d+\s*\|\s*`([a-z_]+\.[a-z_]+)`",
                read("skills/festack/references/playbooks.md"),
                re.MULTILINE,
            )
        )

        self.assertEqual(taxonomy, defaults)
        self.assertLessEqual(playbook_capabilities, taxonomy)

        default_registry = read("skills/festack/references/default-capability-registry.md")
        for capability, provider, provider_type in re.findall(
            r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
            default_registry,
            re.MULTILINE,
        ):
            provider = provider.strip().strip("`")
            provider_type = provider_type.strip()
            if provider == "none":
                self.assertEqual("external adapter needed", provider_type, capability)
            else:
                self.assertTrue(provider.startswith("/"), capability)
                self.assertIn(provider.removeprefix("/"), skill_names(), capability)

    def test_plugin_manifests_match_skill_and_agent_layout(self) -> None:
        # Cursor takes directory strings. Claude Code must OMIT skills/agents and
        # rely on auto-discovery of skills/ and agents/: a directory string fails
        # `claude plugin validate`, and an explicit file list passes validation but
        # silently registers zero agents (verified against claude plugin details).
        cursor = json.loads(read(".cursor-plugin/plugin.json"))
        self.assertEqual("festack", cursor["name"])
        self.assertEqual("./skills/", cursor["skills"])
        self.assertEqual("./agents/", cursor["agents"])

        claude = json.loads(read(".claude-plugin/plugin.json"))
        self.assertEqual("festack", claude["name"])
        self.assertNotIn("skills", claude)
        self.assertNotIn("agents", claude)

    def test_all_skills_and_agents_have_valid_frontmatter_contracts(self) -> None:
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            relative_path = str(path.relative_to(ROOT))
            content = path.read_text(encoding="utf-8")
            match = re.match(r"^---\n(?P<body>.*?)\n---\n", content, re.DOTALL)
            self.assertIsNotNone(match, f"{relative_path} missing frontmatter")
            metadata = dict(re.findall(r"^([a-zA-Z0-9_-]+):\s*(.+)$", match.group("body"), re.MULTILINE))
            self.assertEqual(path.parent.name, metadata.get("name"), relative_path)
            self.assertTrue(metadata.get("description", "").strip(), relative_path)

        for path in (ROOT / "agents").glob("*.md"):
            relative_path = str(path.relative_to(ROOT))
            content = path.read_text(encoding="utf-8")
            match = re.match(r"^---\n(?P<body>.*?)\n---\n", content, re.DOTALL)
            self.assertIsNotNone(match, f"{relative_path} missing frontmatter")
            metadata = dict(re.findall(r"^([a-zA-Z0-9_-]+):\s*(.+)$", match.group("body"), re.MULTILINE))
            self.assertEqual(path.stem, metadata.get("name"), relative_path)
            self.assertTrue(metadata.get("description", "").strip(), relative_path)

    def test_readme_command_palette_matches_installed_layout(self) -> None:
        readme = read("README.md")
        documented_commands = set(re.findall(r"\| `/([a-z0-9-]+)` \|", readme))
        public_skills = skill_names() - {"festack-debate"}

        self.assertLessEqual(public_skills, documented_commands)
        self.assertLessEqual(documented_commands, skill_names())

        for agent in agent_names():
            self.assertIn(f"`{agent.removesuffix('.md')}`", readme)

    def test_core_instructions_do_not_reference_removed_aliases(self) -> None:
        offenders = []
        for base in ["README.md", "AGENTS.md", "skills", "agents"]:
            paths = [ROOT / base] if (ROOT / base).is_file() else (ROOT / base).rglob("*.md")
            for path in paths:
                content = path.read_text(encoding="utf-8")
                for alias in [
                    "`/solution`",
                    "# /solution\n",
                    "name: solution\n",
                    "skills/solution",
                    "`/festack-mode`",
                    "# /festack-mode\n",
                    "name: festack-mode\n",
                    "skills/festack-mode",
                    "festack-mode/references/routing-table.md",
                ]:
                    if alias in content:
                        offenders.append(f"{path.relative_to(ROOT)} contains {alias}")

        self.assertEqual([], offenders)

    def test_plugin_manifest_metadata_stays_in_sync_across_hosts(self) -> None:
        cursor_manifest = json.loads(read(".cursor-plugin/plugin.json"))
        claude_manifest = json.loads(read(".claude-plugin/plugin.json"))

        for key in ["name", "version", "description", "author", "license"]:
            self.assertEqual(cursor_manifest[key], claude_manifest[key], key)

        for manifest in [cursor_manifest, claude_manifest]:
            self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
            self.assertGreaterEqual(len(manifest["description"]), 80)


class ClaudeCodePortContractTests(unittest.TestCase):
    """Invariants from docs/superpowers/specs/2026-06-10-festack-claude-code-port-design.md."""

    CURSOR_SLUG = re.compile(r"\b(gpt-5\.5|claude-opus|composer-2\.5|gemini-3\.1)")
    # The only files allowed to name Cursor model slugs.
    SLUG_ALLOWED = {"skills/setup-models/SKILL.md", "skills/festack-debate/SKILL.md"}

    def _all_md(self):
        """Yield (posix relative path, text) for every .md under skills/ and agents/."""
        for base in ("skills", "agents"):
            for path in sorted((ROOT / base).rglob("*.md")):
                yield str(path.relative_to(ROOT)), path.read_text(encoding="utf-8")

    # Supersedes test_model_slugs_are_confined_to_model_setup_and_engine_docs: after the
    # Claude Code port, only these two files may name Cursor model slugs.
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
        self.assertIn("AskUserQuestion", text, "skills/festack-debate/references/decision-gates.md")

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

    # opus/fable/haiku are Claude Code model aliases (resolved by the host); defaults
    # defined in the port spec, written by /setup-models to ~/.claude/festack/models.md.
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

    # Vendor names that must never appear in core skills/agents (vendor specifics
    # arrive only via the profile). Samples/ may name vendors; core may not.
    VENDOR_TERMS = re.compile(r"Unity Catalog|Databricks|Snowflake|OpenAI|Salesforce")

    def test_core_skills_are_vendor_neutral(self) -> None:
        offenders = [rel for rel, text in self._all_md() if self.VENDOR_TERMS.search(text)]
        self.assertEqual(offenders, [], "vendor names leaked into core skills/agents")

    def test_competitive_poc_playbook_exists(self) -> None:
        playbooks = read("skills/festack/references/playbooks.md")
        self.assertIn("## competitive-poc", playbooks)
        for capability in ("research.account", "research.competitor", "scope.poc", "review.deliverable"):
            self.assertIn(capability, playbooks)
        routing = read("skills/festack/references/routing-table.md")
        self.assertIn("competitive-poc", routing)

    def test_gate_batching_names_host_question_cap(self) -> None:
        text = read("skills/festack-debate/references/decision-gates.md")
        self.assertIn("four questions per call", text)

    def test_readme_documents_claude_plugin_install(self) -> None:
        text = read("README.md")
        self.assertIn("/plugin marketplace add", text, "README.md")
        self.assertIn("~/.claude/festack/models.md", text, "README.md")


class LedgerV2ContractTests(unittest.TestCase):
    """Invariants from docs/superpowers/specs/2026-06-10-festack-engagement-ledger-design.md."""

    def test_ledger_lifecycle_reference_exists_with_required_sections(self) -> None:
        text = read("skills/festack/references/ledger-lifecycle.md")
        for required in (
            "ENGAGEMENTS.md", "brief.md", "log.md", "## Head and annex",
            "superseded", "## Statuses", "dormant", "## Compaction",
            "## Auto-create", "## Receipt format", "archive/",
        ):
            self.assertIn(required, text, f"ledger-lifecycle.md missing: {required}")

    def test_router_announces_pick_and_hard_asks_collisions(self) -> None:
        text = read("skills/festack/SKILL.md")
        self.assertIn("ledger-lifecycle.md", text)
        self.assertIn("announce", text.lower())
        self.assertIn("collision", text.lower())

    def test_handoff_skill_exists(self) -> None:
        text = read("skills/handoff/SKILL.md")
        self.assertIn("name: handoff", text)
        for required in ("brief", "open gates", "next Monday", "paste", "coverage"):
            self.assertIn(required, text, f"handoff SKILL.md missing: {required}")
        self.assertIn("/handoff", read("skills/festack/references/routing-table.md"))

    def test_closeout_convention_appends_to_ledger(self) -> None:
        # Every public skill closeout must carry the ledger-append line.
        missing = []
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            if "## Closeout receipt" in text and "log.md" not in text:
                missing.append(str(path.relative_to(ROOT)))
        self.assertEqual(missing, [], "closeout sections missing the ledger append line")

    def test_hook_never_blocks(self) -> None:
        text = read("hooks/check_ledger.py")
        self.assertIn("sys.exit(0)", text)
        self.assertNotIn("sys.exit(1)", text)
        self.assertNotIn("sys.exit(2)", text)
        self.assertIn("fail-open", text)

    def test_review_work_persona_seat_is_claim_grounded(self) -> None:
        text = read("skills/review-work/SKILL.md")
        self.assertIn("persona", text.lower())
        self.assertIn("claim inventory", text)

    def test_quick_log_staleness_and_roundtrip_additions(self) -> None:
        lifecycle = read("skills/festack/references/ledger-lifecycle.md")
        self.assertIn("## Quick log", lifecycle)
        self.assertIn("quick-log", lifecycle)
        router = read("skills/festack/SKILL.md")
        self.assertIn("/festack log", router)
        self.assertIn("next step set", router, "index staleness marker missing")
        self.assertIn("step-set", lifecycle, "index step-set column missing")
        self.assertIn("quick-log", read("skills/festack/references/routing-table.md").lower())
        handoff = read("skills/handoff/SKILL.md")
        self.assertIn("## Round-trip format", handoff)
        self.assertIn("rebuild a ledger from this snapshot", handoff)


if __name__ == "__main__":
    unittest.main()
