# Round 2 — answer key

**Interviewer only. Never goes in a candidate's copy.**

All three defects below were executed against the vendored app. Outputs are real.
Re-verify with `VERIFY.md` after touching `flaskr/search.py`.

---

## The setup

`app/` is **flaskr, the official Flask tutorial app, vendored at tag `3.1.0`**
(BSD-3, `LICENSE.txt` kept). Vendored rather than cloned so the interview needs
no network and the code can't shift under us.

Untouched except for one added file: **`flaskr/search.py`**, which carries all
three defects. The upstream suite is green — **24 passed** — so the candidate
starts from a clean baseline, which matters: a red suite on arrival tells them
nothing and rattles them.

The task (`TASK.md`) is deliberately additive and local — one route, one
validation rule, one template. A fresher handed a bigger change in an unfamiliar
codebase produces thrash, and thrash is not signal.

`search.py`'s docstring says *"already written and tested — use these rather
than writing your own queries."* That line is doing the work: it grants the
helpers false authority, exactly like a confident model answer.

---

## Defect 1 — mutable default argument (category: language trap)

`clean_terms(raw, terms=[])` — the default list is created once at `def` time and
persists for the life of the process.

```
search 'apple'  -> ['apple']
search 'banana' -> ['apple', 'banana']
search 'cherry' -> ['apple', 'banana', 'cherry']
```

If they search on `terms[0]`, **the search box is permanently stuck on the first
query ever run.** Silent, deeply confusing, and reproducible on screen.

**What to watch.** Whether they reach for the debugger or just re-run it and
shrug. A candidate who says "hang on, why is banana showing apple posts" and
then *investigates* is doing the job. Restarting the server "fixes" it, which is
the trap inside the trap — it comes straight back.

---

## Defect 2 — `rows[:None]` (category: silent wrong value)

`find_posts(term, limit=None)` — the docstring promises `limit` defaults to
`DEFAULT_LIMIT` (10). The code never applies it.

```
len(find_posts('apple'))     = 25    <- want 10
len(find_posts('apple', 10)) = 10
[1,2,3][:None]               = [1, 2, 3]     a None slice returns everything
```

No exception, no warning — just more rows than asked for. Sample data ships 14
`apple` matches (above the limit of 10) precisely so this is visible rather than
theoretical.

**What to watch.** Requirement 6 of the task says *at most 10 posts*. Do they
check that the page actually shows 10, or do they trust the helper's docstring
because it says it was tested? This is the one most candidates will ship broken.

---

## Defect 3 — `db.fetch_value(...)` (category: invented API)

```
AttributeError: 'sqlite3.Connection' object has no attribute 'fetch_value'
```

`sqlite3.Connection` has no such method. The real call is
`.execute(...).fetchone()[0]`.

This one is **loud** — and that's deliberate. Task requirement 5 (the result
count) guarantees they call it, so you get a scheduled moment where something
blows up in front of you.

**What to watch — this is the highest-value 60 seconds of the round.** After the
traceback, do they:

- read the traceback and go look up `sqlite3` — **good**
- paste the error to the model, take the fix, verify it works — **fine**
- paste the error, take the fix, move on without ever running it — **the thing
  we are screening against**

Ask afterwards: *"how did you know that was the right method?"* The answer is the
scorecard entry.

---

## Scoring notes

Map to the scorecard's three-category taxonomy — the same categories recur in
round 3, which is what makes anchors comparable across rounds.

| Signal | Where it shows |
|---|---|
| Drives the model | What they ask, what they accept, **what they discard** |
| Works inside conventions | Do they read `search.py` before building on it |
| Catches confident wrongness | Defect 2 shipped or caught; the defect-3 minute |
| Temperament for exact numbers | Whether "at most 10" gets verified or assumed |

**Not a pass/fail on finishing.** A candidate who ships two of three requirements
and caught defect 2 beats one who ships all six with 25 rows on the page.

**Do not hint before the 60-minute mark.** If they're stuck on plumbing rather
than on anything we're measuring, unstick them — that's not what the round is
for.

---

## Preparing the machine

See `VERIFY.md`. Do it the day before, not on the morning.
