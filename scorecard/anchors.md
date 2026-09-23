# Scorecard — criteria and anchors

**Interviewer only.**

Score after round 3, from the round named against each criterion. If you didn't
see evidence in that round, **leave it blank** rather than inferring it from
elsewhere — weighted rubrics quietly become unweighted when people score on
accumulated impression.

Anchored for **freshers / internship experience**. These are not the anchors a
2–5 year candidate would be held to; see the note at the bottom.

## Rubric

**1** not evident · **2** developing · **3** solid · **4** exceptional

## Criteria

| Weight | Criterion | Evidence from | What it looks for |
|---|---|---|---|
| **×3** | Catches confident wrongness | Round 3, Q3 | See anchors below |
| **×3** | Reads unfamiliar code | Round 1 | Traces control flow in code they've never seen, without a guided tour |
| ×2 | Drives the model | Round 2 | What they ask, what they accept, **what they discard** |
| ×2 | Works inside conventions | Round 3, Q1 | Compares against neighbouring code rather than judging in isolation |
| ×2 | Temperament for exact numbers | Round 3, Q2 | Traces a value end to end instead of stopping at "should be an int" |
| ×2 | Curiosity, self-directed | Rounds 2–3 | What they looked up unprompted; can narrate a bug to root cause |
| ×2 | Fundamentals are theirs | Round 1, second half | The small problems and the SQL query, no AI |
| ×1 | Problem decomposition | Round 1 | Clean approach matters more than speed |

**Maximum: 68.**

## The ×3 anchors

### Catches confident wrongness — round 3, Q3 (`sqlite3.Row.get`)

| | |
|---|---|
| **1** | Reads past it. Row is dict-like, `.get()` is a dict method, looks fine. |
| **2** | Checks it exists once we point at the line. |
| **3** | Checks it *and* can say how — `hasattr`, the REPL, the docs, running it. |
| **4** | Flags it while reading, unprompted, and says why it smelled wrong. |

**The follow-up carries the score, not the finding.** Ask *"how do you know?"*
"I asked Claude and it said Row has no `.get`" is a **2** — unless they then went
and checked. Write down which it was.

### Reads unfamiliar code — round 1 (`active_plan`)

| | |
|---|---|
| **1** | Restates the docstring back. |
| **2** | Explains what the code does. |
| **3** | Predicts where a bug would hide; traces the comparator when asked. |
| **4** | Names a specific input that breaks it, and whether it fails loudly or quietly. |

## The bar

**48 of 68 or higher, and no ×3 criterion below 2.**

A candidate strong everywhere who cannot catch a model being confidently wrong
is not a hire — on a codebase this old, they will erode its conventions faster
than they add to it. That is the entire thesis of the loop; do not average it
away.

## Notes that decide close calls

- **Two defended findings beat six asserted ones.** Someone who finds one
  round-3 defect but can say exactly who can see what, and what they'd change,
  is stronger than someone who lists all three vaguely.
- **Round 2 is not scored on finishing.** Shipping two of six requirements while
  catching the limit defect beats shipping all six with 25 rows on the page.
- **Note every nudge you gave**, and which round. A 3 that needed a file pointed
  at is not the same as an unprompted 3.
- **Silent vs loud.** Across all three rounds, the strongest signal is a
  candidate who distinguishes *this raises* from *this quietly returns the wrong
  thing* — and is more alarmed by the second.

## If you ever run this loop for a mid-level candidate

Raise the bar to 55 of 68, require no ×3 below **3**, and shift the round-3 Q3
anchors up one band — at 3+ years, spotting the invented API unprompted is the
expectation rather than the ceiling.
