# the autopilot loop

How `/autopilot` keeps grinding without going off the rails. The goal is sustained autonomous execution that still stops for the decisions a human must own. Momentum, not recklessness.

## The shape

```
scope (canvas)  ->  plan (todolist)  ->  [ build phase -> evaluate -> gate? ] x N  ->  done
```

Build proceeds phase by phase. Each phase ends with a fast self-evaluation. Routine evaluation happens at phase boundaries, but a genuine decision gate stops the loop immediately, the moment it is encountered, even mid-phase. A destructive action or a scope change does not wait for the evaluator.

## Per-phase evaluator

After each phase, run a fast evaluator (the `evaluator` role from the host's model config) over just that phase's output. It answers three questions:

1. Did this phase meet its acceptance check from the todolist?
2. Did it introduce a problem the next phase will inherit?
3. Is there a genuine decision the human must make before continuing?

If 1 is no, the phase repeats (within budget). If 3 is yes, stop and ask. Otherwise, continue. The evaluator is cheap and runs every phase; that is what keeps small errors from compounding across a long run.

## Iteration budget

Every phase gets a retry budget (default 2 retries). If a phase fails its acceptance check past budget, autopilot stops and reports: what it tried, why it is stuck, and the specific decision or input it needs. It does not loop forever, and it does not silently ship a phase that failed its check.

A global budget caps the whole run: default 12 phases or 20 total retries across all phases, whichever comes first, or an elapsed-time cap for time-boxed runs. The defaults are overridable in the profile. When the budget is exhausted, autopilot stops and summarizes progress against the todolist rather than pushing past the limit.

## What stops the loop (and what does not)

Stop and ask the human only for **genuine decisions** as defined in `skills/festack-debate/references/decision-gates.md`: irreversible, expensive, or true judgment calls. Examples: a destructive action, a scope change, a fork with no clear default and real consequences.

Do NOT stop for:

- **Observable forks.** Resolve them by checking (run it, read it, test it).
- **Reversible forks.** Pick the sensible default, note it, keep moving. The human can change it later.

The discipline: classify before you ask. Autopilot's value is that it does not interrupt for things it can settle itself.

**Cost of classifying.** Classification must be cheap, because it happens at every fork. Obvious forks are classified inline by the orchestrator for free. Only a genuinely ambiguous fork spends a model call, and it spends the cheapest one: the `classifier` role (the cheapest configured model), never a frontier model. The frontier models are budgeted for synthesize and critique, where iteration under human review actually pays off. If the cheap classifier is still unsure, default to genuine and ask the human.

## Showing work

Autopilot is autonomous, not opaque. It keeps the canvas and todolist current as it goes, so the human can glance in at any time and see: what is done, what is in flight, what each phase produced, and any decision waiting at a gate. A silent agent that grinds for an hour and dumps a result is not autopilot, it is a black box.

## The build gate

Autopilot never starts building until the scope and plan are approved once, up front. The whole point of the upstream festack skills (`/scope-and-align`, `/demo`, `/solution-critic`) is that design happens before build. Autopilot executes an approved design; it does not invent one mid-grind.
