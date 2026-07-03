---
name: client-debug
description: Answer one ad-hoc client or product question with source-backed evidence, confidence, and uncertainty.
disable-model-invocation: true
---

# /client-debug

A client asks something specific and the honest answer is "I need to check." This skill makes that check systematic: map the question, search the right sources, and answer with cited confidence instead of a guess.

It is the lightweight counterpart to `/discovery`. Discovery builds a broad picture. This answers one question well.

## Modes

- **Fast.** A quick, cited chat answer for a question the declared sources settle quickly. Fast means lighter packaging, not a narrower search: still cover both external and internal source families when both are declared. Default for simple asks.
- **Deep.** A documented answer with full uncertainty handling and references, for a question that matters or has branches. Use when the ask says "create", "document", or the answer will be shared.
- **Provider mode.** When invoked by a playbook as `research.product_question`, return only the research handoff: cited answer, confidence, caveats, client-citable vs internal-only evidence, sources, and open questions. Do not package a final email or document unless the user invoked `/client-debug` directly.

Pick the mode from the ask. When unsure, start fast and offer to deepen.

## Workflow

```
- [ ] 1. Read the ground: research method, decision-gates, profile
- [ ] 2. Map the question
- [ ] 3. Search the declared sources
- [ ] 4. Deep-dive the uncertain
- [ ] 5. Answer with cited confidence
- [ ] 6. Hand off (and document, in deep mode)
```

### 1. Read the ground

Read the research method in the `festack-debate` skill (`references/research-method.md`) and the decision-gate convention (`references/decision-gates.md`). Read `$FESTACK_HOME/profile.md` for the declared knowledge sources and the people or channels to consult. If no source is declared, ask which source families to use with `allow_multiple: true`, because a good answer may need docs plus tickets plus chat.

### 2. Map the question

Name the direct subject, its dependencies, the alternatives, and any branches ("does it support X or Y"). A precise answer often hinges on a nearby fact.

### 3. Search the declared sources

Work the sources in authority order per the research method, but cover breadth before depth. When the profile declares both external and internal source families, consult at least one of each before you answer: external sources tell you what is promised, internal knowledge and chat tell you what is actually true right now. Do not stop at the first source that appears to settle the question, and for feature status, roadmap, or anything in flux, treat an internal confirmation as required. Refer to sources by family, not by tool name. Cite as you go. Weight by recency and authority.

For client-visible answers, distinguish evidence from client-citable sources. Public docs, release notes, or shareable official pages can be cited in the final answer. Internal knowledge base, chat, tickets, or field notes can raise or lower confidence, but do not quote or cite them to the client unless the source is explicitly shareable.

### 4. Deep-dive the uncertain

For anything in flux, preview, or contested, get the specifics: status, timeline, access, current limits. Do not stop at a surface mention.

### 5. Answer with cited confidence

Give the direct answer to the exact question, every branch. Split confident from less-confident from could-not-determine. Carry a confidence level with a one-line reason. Cite key claims inline.

For security, governance, roadmap, pricing, legal, privacy, or contractual answers, separate similar-sounding capabilities before drafting. For example, endpoint ACLs, application-level filters, catalog or workspace permissions, row filters, and row-level security are different controls. Do not let one stand in for another unless the source says so.

### 6. Hand off

In provider mode, return the research handoff and stop. The parent playbook owns `create.client_doc`, review, and final packaging.

In fast mode, deliver the cited chat answer and name anything that needs human confirmation.

In deep mode, stress the answer with `/review-work` against the research-answer rubric first, looping fixes until the answer is cited, its uncertainty is explicit, and no major claim is unsupported. When the answer has branches or compares options (supports X or Y, per-branch confidence, a capability matrix), render that as a canvas (the `canvas` skill) before writing prose when the structure would be hard to scan in text. Then package it for the requested surface:

- **Client-ready prose or email:** return polished prose in chat, with client-citable references and caveats. Do not create a document artifact unless the user asked for one or the profile/delivery flow requires one.
- **Document artifact:** write it as a doc via the document-target rule (like `/doc`), with references, and return the link.

Avoid duplicate review loops. If `/client-debug` already passed `/review-work` on the researched answer, `/doc` only needs to review packaging, sanitization, and audience fit unless new claims were added.

## Notes

- The discipline is the same as `/discovery`; the scope is one question, not a whole account.
- Never present a low-confidence answer as settled. Saying "I could not confirm, ask this person" is a valid result.
- All prose follows the `fe-deslop` skill.

## Closeout receipt

End every direct invocation with these fields so the FE can trust the handoff:

- `recommended_next_step`: the next skill, gate, review, build, stop, or `none` when complete.
- `visual_artifact_receipt`: `canvas`, `docs-canvas`, structured handoff, prose, or `none`, plus the owner.
- `ledger`: when an engagement is active, append this receipt as one line to its `log.md` per `festack/references/ledger-lifecycle.md`. Narrow fast-lane answers append one line and pay no other ceremony.
- `Gate receipt`: include this when any `AskQuestion` ran, using the receipt shape from `festack-debate/references/decision-gates.md`.
