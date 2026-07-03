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

For a panel of four, double the lens most relevant to the question and give the doubled
worker a stated secondary emphasis, naming which lens was doubled and why. Panels of two
drop the lens least relevant to the question, and say which one was dropped.
