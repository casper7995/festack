# lessons format

How `/learn` writes durable knowledge. Two destinations, kept separate on purpose.

## Two files, two jobs

- **`$FESTACK_HOME/profile.md`** holds STABLE facts and preferences: your role, what you represent, your audience, your delivery defaults, your writing voice, your declared sources. Things that are true across most engagements. `/personalize` owns its schema; `/learn` updates it when a durable preference emerges.
- **`$FESTACK_HOME/lessons.md`** holds ACCUMULATED LESSONS: reusable guidance learned from doing the work. Things you figured out, not things you configured.

The split matters. A preference ("I write in a plain, direct voice") belongs in the profile. A lesson ("when a client says 'just show me', skip the architecture slides and open the live demo") belongs in lessons. Mixing them turns the profile into a junk drawer.

## Lesson entry shape

Each lesson in `lessons.md` is one block:

```
## <short title>
- **When:** the trigger or situation.
- **Do:** the action to take.
- **Because:** the reason, ideally with the evidence that earned it.
- **Avoid overapplying when:** the boundary, where this lesson does not hold.
- **Confidence:** high / medium / low, based on how much evidence earned it.
- **Source:** where it came from (a /retro date, a specific engagement, direct feedback).
- **Last reinforced:** YYYY-MM-DD (updated each time the lesson recurs).
```

Keep it to guidance you would actually follow. If it cannot be phrased as when/do/because, it is probably an observation, not a lesson. Capture reusable workflow patterns (a sequence of moves that worked) the same way, but record the pattern and why it worked, not the specific tools used; tools change, the shape is durable.

## Dedup and merge rules

Before adding anything:

- **Search first.** Read the existing file. If a near-duplicate exists, merge into it rather than appending a second copy.
- **Sharpen on merge.** When new evidence strengthens an existing lesson, update its "because" and keep one entry, do not stack.
- **Promote on repetition.** If the same lesson shows up from three different engagements, it has graduated from lesson to default; consider moving it into the profile's delivery defaults.
- **Retire the stale.** If a lesson is contradicted by newer experience, update or remove it. An accumulating file of stale advice is worse than a short fresh one.

## Quality bar

- Every lesson is reusable guidance, not a diary entry.
- No duplicates; near-duplicates are merged.
- Stable preferences are in the profile, learned guidance is in lessons.
- The file stays short enough to actually re-read. Prune as you add.
