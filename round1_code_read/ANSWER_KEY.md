# Round 1 — answer key

**Interviewer only. Never goes in a candidate's copy.**

Everything below was run against `active_plan.py` and is verified output, not
expectation. Re-verify after any edit to the file.

---

## The artifact

`active_plan.py` — 25 lines, one function, no imports, no framework. The
docstring states the intended rule, so the candidate is checking *code against
spec*, not guessing intent. That is the whole design: it lets a fresher be
right or wrong for a reason.

Give them the file and ~2 minutes to read before asking anything.

---

## Q1 — "Two plans both have `starts_on = None`. Which wins, and why?"

**Spec says:** highest id.
**Code returns:** lowest id.

```
ids 7 and 11, same start   -> returns 7   (want 11)
ids 3 and 9, both start None -> returns 3 (want 9)
```

**Why:** the sort key is `(starts_on or "", -p["id"])` with `reverse=True`.
The id is negated *and* the whole sort is reversed — two inversions, so the
tie-break runs backwards. It looks deliberate, which is what makes it good.

**What to listen for.** The pass condition is tracing to the comparator at all.
A candidate who says "it sorts descending so highest id wins" read the
`reverse=True` and stopped — that is a 1 or 2. A candidate who notices the
minus sign is doing real work.

*This is also a bug a model gets wrong when asked casually — which is why the
same shape reappears in round 3.*

---

## Q2 — "These are strings. When does that comparison break?"

Unpadded dates. The failure is **silent exclusion**, not mis-ordering:

```
plan starts "2026-1-5",  asked about "2026-04-01" -> None   (plan vanishes)
plan starts "2026-01-05", asked about "2026-04-01" -> the plan
```

because `'2026-1-5' <= '2026-04-01'` is `False` — at index 5, `'1' > '0'`.

A plan that has genuinely been active since January is reported as not yet
started. Nothing raises; the caller just gets `None`.

**What to listen for.** "Strings compare character by character" is a 2.
Reaching a concrete failing pair is a 3. Saying *and* that it fails silently
rather than raising is a 4 — that is the instinct the job actually needs.

---

## Q3 — "You're handed a plan dict with no `ends_on` key. What happens?"

`KeyError: 'ends_on'`.

Distinguishes people who have **run** Python from people who have read it.
Follow-up: "how would you change it?" — looking for `p.get("ends_on")` and,
better, a question about whether a missing key should mean *never ends* or
should be rejected as malformed data.

---

## Follow-up — hand them `test_active_plan.py`: "what case is missing?"

All 5 tests pass. Verified gaps:

| Missing case | Why it matters |
|---|---|
| **Tie-break on equal `starts_on`** | This is exactly the Q1 bug. The bug survives *because* the suite never covers it. |
| **Non-padded dates** | The Q2 failure. |
| **A dict missing a key** | The Q3 failure. |
| Empty `plans` list | Minor — shares the `not matches` path with the covered case. |

The teaching point, if they do not get there themselves: **the bug lives in the
one behaviour the tests do not cover.** Worth saying out loud even to a
candidate who misses it — it is the most useful thing in the round.

---

## Stretch probe — only for someone who has cleared everything

"A plan starts `2027-01-01`, has no end date. Does it match a 2026 date?"

Correct answer: no, returns `None` — verified. This one is *not* a bug; it is a
pure control-flow trace. Use it to separate a 3 from a 4 without introducing a
new defect.

---

## Variants

Same structure, different domain, if you need a second candidate to get a fresh
problem: **library fines** (due date, grace period, per-day accrual, a cap) and
**parking tiers** (first hour free, tiered rates, daily maximum). Both rehearse
the same date-range-plus-cap logic. Not yet written — see `../CONTEXT.md`.
