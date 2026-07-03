# POC scoping document

The artifact `/poc` produces and maintains. A POC document is a living contract between you and the client about what "success" means, written before the work starts and updated as it runs. Its job is to prevent the two ways POCs die: scope creep and a moving definition of done.

## The non-negotiable: measurable exit criteria

A POC needs measurable success criteria; without them it becomes an open-ended science project that never ends. Every criterion must be something you can point at and say "met" or "not met" with no argument.

- **Bad:** "Demonstrate good performance." (Whose definition? How good?)
- **Good:** "Process the 50M-row sample in under 10 minutes, baseline is 45 minutes today."

Each criterion needs: the metric, the current baseline, the target, and how it will be measured. No baseline, no criterion.

## Structure

1. **Summary.** What this POC proves and for whom, in three sentences.
2. **Business context.** The problem, why it matters now, what a win unblocks for the client. Pull from `/scope-and-align` output if it exists.
3. **Stakeholders and cadence.** Executive sponsor, technical owner, day-to-day contacts, decision-maker, meeting cadence, and escalation path.
4. **Mutual success plan.** What each side contributes: data, environment, access, subject-matter experts, delivery owners, review dates, and decision date.
5. **Success criteria.** The measurable exit criteria, as a table: criterion, metric, baseline, target, how measured, owner, status. This is the heart of the document.
6. **Scope.** What is in. Equally important, what is explicitly out. The out-of-scope list is your defense against creep.
7. **Architecture / approach.** How the POC is built, at the level a technical stakeholder needs. Link a `/diagram` if one exists.
8. **Plan and timeline.** Phases, owners on both sides, dates, dependencies.
9. **Risks and assumptions.** What could derail it, what you are assuming is true. Each risk gets an owner and a mitigation.
10. **Evaluation results.** Updated as the POC runs: evidence, screenshots or links, measured values, pass/fail by criterion, and notes on deviations.
11. **Open questions / decisions log.** Running list, dated, with how each was resolved. This is what makes it a living doc.
12. **Status.** Updated as the POC runs: which criteria are met, what changed, what is blocked.

## Living-document discipline

- The document is updated, not rewritten. The decisions log and status section accumulate.
- When scope changes, it changes here, in writing, with both sides aware. A verbal scope change that never hits the doc is how POCs blow up.
- At the end, the success-criteria table is the verdict. Met or not, per criterion. No reinterpreting the goal after the fact.

## Quality bar

- Every success criterion is measurable, with a baseline.
- The out-of-scope list is real, not empty.
- Every risk has an owner and a mitigation.
- Stakeholders and owners are named on both sides.
- Cadence and decision date are explicit.
- Evaluation results are tied back to criteria, not written as a narrative victory lap.
- The doc reads like a contract a client would sign, not a wishlist.
