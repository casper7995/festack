## Learned User Preferences

- Keep festack vendor-neutral and generalizable across Field Engineer / Solution Architect roles; borrow workflow craft from FE skills without hardcoding vendor-specific details.
- Prefer `/festack` as a lazy front door that can route and carry end-to-end work; direct skill invocation should remain optional for users who know exactly what they want.
- Use `AskQuestion` for structured FE decisions and personalization, including multi-select choices where several defaults can apply.
- Let `/personalize` mine transcripts for profile suggestions, but ask before persisting inferred profile updates.
- Use canvas or docs-canvas for scope, alignment, diagrams, and client-ready deliverables when visual structure helps the user understand or review the work.
- Use multi-model debate, review, and critic loops for high-risk artifacts where iteration improves quality; model choices should come from `festack-models.mdc`, not hardcoded one-off reviewers.
- Use strict FE UX scorecards as quality gates for festack improvements; autopilot-quality work should target 90+/100 across lazy router, smart next steps, AskQuestion, canvas/visuals, multi-agent/review, and overall workflow.
- Architecture diagrams should be deck-ready; Mermaid is acceptable as a starting point, but prefer available Figma, tldraw, Mermaid MCP, or similar visual tools when they improve the deliverable.
- Avoid command or skill naming collisions and duplicate installs; remove deprecated aliases instead of keeping duplicate slash commands.
- Treat `/setup-festack` as the single public setup flow; keep `/personalize`, `/setup-models`, and `/setup-capabilities` as focused subflows or refresh paths.
- In default-only capability mode, continue with core providers instead of forcing setup; ask one focused question only when a required provider is unavailable.

## Learned Workspace Facts

- festack is a vendor-neutral workflow stack for Solution Architects and Field Engineers; its unit of work is a client deliverable, not a code diff.
- `/festack` is the canonical front door; it emits Routing receipts with intent, route, why, setup state, recommended next step, and visual artifact owner.
- `/setup-festack` is the one-command setup path for profile, model roles, and capability wiring; it can also summarize current setup and refresh one part.
- `festack-delivery-agent` is the end-to-end orchestration agent for broad `/festack` situations; it carries Gate receipts, `recommended_next_step`, and `visual_artifact_receipt`, while `festack-agent` remains the stateless panel worker.
- Capability wiring lives in `$FESTACK_HOME/capabilities.md` or `.yaml`; missing user capability files mean default-only mode, not a setup blocker.
- `/problem-frame` structures fuzzy client problems; `/solution-critic` decides among competing approaches with multi-model debate.
- `/personalize` writes the profile to `$FESTACK_HOME/profile.md`; the profile is where company, stack, and user specifics belong so skills stay vendor-neutral.
- Model role mappings live in the host's model-role config (Cursor: `~/.cursor/rules/festack-models.mdc`) and are read by debate, review, evaluator, and classifier flows.
- `/autopilot` executes approved build scopes only after an explicit approved-build payload with acceptance checks, target environment, rollback/failure evidence, and deliverable handoff.
- `/compete` handles quick comparisons; `competitive-proof-asset` owns packaged battlecards, cited proof assets, and competitive demo proofs with scoped claims.
- Pure product fact lookups route to `/client-debug`; client-ready product answers route through `product-question-to-client-answer` for research before packaging.
- The repo-shipped workflow canvas lives at `canvases/festack-workflow.canvas.tsx`; Cursor canvas file openers should use `useCanvasAction` with `openFile`, not web `Link` paths.
