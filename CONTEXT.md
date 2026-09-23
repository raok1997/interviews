# Interview materials — context

Assessment materials for **one** hire: a product engineer who will work on the
First-Tek commercial real-estate platform (`~/Desktop/code/First-Tek`).

This repo is **interviewer-facing and stays private.** Candidates never clone it
— they get generated copies with the answer keys stripped. See *Handing files to
a candidate* below.

## The hire

- **One seat.** Pool is fresh graduates / internship experience.
- The job is **PHP 8 / Yii2**, MySQL, Bootstrap 3 + jQuery, plus AI-integration
  work (tool-calling, RAG over lease PDFs, OCR). Roughly 60% product
  engineering, 40% AI surfaces.
- **We assess in Python, and hire for PHP.** The candidate knows Python; PHP is
  learnable in weeks, thinking is not. This is a deliberate bet on general
  programming ability and learning speed over existing stack fluency.
- The position brief and the scoring instrument live as published artifacts:
  - Brief (shareable): https://claude.ai/code/artifact/ab4d1d02-c52c-4706-acd3-5c6f9bececee
  - Scorecard (internal): https://claude.ai/code/artifact/c1eecad2-7911-4b01-8a08-5aedae7be8cd
  - **Both are stale.** They still say 2–5 years, ₹9–24 L, and list PHP 8 /
    Bootstrap 3 as day-one must-haves. Re-cut them for a fresher band and a
    Python-assessed thesis before sending either to a recruiter.

## The loop

Three rounds, **all on site**, across two visits. Nothing is done unsupervised
— a take-home can be collaborated on and we would never know. Travel is
reimbursed retroactively for **both** visits once the candidate clears visit one.

| # | Round | Length | AI tools | Visit |
|---|---|---|---|---|
| 1 | Code read & fundamentals | 45 min | **off** | one |
| 2 | Observed build session | 90 min | **on, expected** | one |
| 3 | Reverse code review & team conversation | 90 min | on | two |

## Why each round is shaped this way

- **Round 1** is the only no-AI segment. Half code reading, half small practical
  problems (array/string transform, grouping-and-dedupe, one SQL query).
  Deliberately not competitive-programming shaped — that filters for interview
  prep, not for reading ability.
- **Round 2** watches *how they drive a model*: what they ask, what they accept,
  what they discard. Watch the discards. Not judged on finishing.
- **Round 3** is a **guided** review, not an open one — freshers have no review
  experience to draw on. Three fixed questions (below). Scoring is "can they
  verify a claim when pointed at it", not "did they find it unprompted".

## Decisions already locked

- **Write round-1 code ourselves; use a real repo only for rounds 2 and 3.**
  Public repo code rarely has a clean trap in 60 lines, and you burn the round
  explaining context. Code we author = total control, zero memorisation risk.
- **Rounds 2/3 repo: [`pallets/flask` → `examples/tutorial/flaskr`](https://github.com/pallets/flask/tree/main/examples/tutorial), pinned to tag `3.1.0`.**
  Official, tiny, SQLite, ships its own tests, boots in two commands. Pin the
  tag — `main` will rot the seeded diff under us.
  ```
  pip install -e .
  flask --app flaskr init-db
  flask --app flaskr run --debug
  ```
- **No Laravel / Symfony / Django / FastAPI-full-stack.** Too large to read in
  45 minutes, and a model explains them flawlessly — which poisons exactly the
  signal we are buying. The FastAPI starters on GitHub are mostly unmaintained
  community repos; don't shop there.
- **Seeded defects are pre-committed, never generated per candidate.** A trap
  that depends on what a model happens to emit stops measuring anything the
  moment model behaviour shifts. Identical for every candidate so scores compare.
- **Three defect categories, kept across all rounds** — this is what makes the
  scorecard anchors transfer:
  1. **Silent wrong value** — e.g. `request.form.get("price")` is a `str`
     compared against an `int`. No traceback.
  2. **Convention / language trap** — e.g. mutable default argument.
  3. **Invented API** — a call to a method that does not exist. The one that
     matters: it is what unverified model output looks like in a diff.
- **Round 3's three questions**, asked verbatim:
  - *Does this function do what its name says?*
  - *What happens if this value is null?*
  - *Does this method exist — and how would you check?*

## Handing files to a candidate

Answer keys live freely in this repo because **the repo never leaves it.** See
`README.md` for the full list of files that must never be copied out, and the
`grep` check to run on a staged copy.

- **Round 1** — `make candidate-round1`. Hand over the test file only after the
  three questions are done.
- **Rounds 2 and 3** — prepare the machine (`make run-round2` / `make run-round3`)
  and let them work on it. Nothing is copied, so nothing can leak.

## State

Structure note: `app/` holds flaskr **pristine**, vendored at tag 3.1.0. Both
rounds are built from it into `work/` by `make setup`, so `app/` is never edited
and `make reset` between candidates cannot go wrong.

- [x] **Round 1** — `round1_code_read/`. `active_plan.py` (3 traps),
      `test_active_plan.py` (5 passing tests with deliberate gaps),
      `ANSWER_KEY.md` with verified outputs.
- [x] **Round 2** — `round2_build/`. Seeded helper `seed/search.py` carries
      three defects; upstream suite green at 24 passed. `TASK.md`,
      `ANSWER_KEY.md`, `VERIFY.md`, `seed_dev_data.py`, `verify_defects.py`.
- [x] **Round 3** — `round3_review/`. `review.diff` (139 lines, 6 files,
      generated from a real tree so it always applies) adds a drafts feature
      with one defect per category. **The suite is green on that branch — that
      is the point.** `QUESTIONS.md`, `ANSWER_KEY.md`, `verify_defects.py`.
- [x] `scorecard/anchors.md` — 8 weighted criteria, max 68, bar 48 with no x3
      below 2. Anchored for freshers, with a note on raising it for mid-level.
- [x] Repo organised for GitHub — `README.md` (new-machine setup), `Makefile`,
      `.gitignore` covering `.idea/`, venvs, `work/`, and desktop cruft.
- [ ] Round 1 variants — library fines, parking tiers, for a second candidate.
- [ ] Round 1 second half — the small practical problems are Janu's; not written
      here yet.
- [ ] Re-cut the two published artifacts (band, years, must-have list).
- [ ] First git commit — see *Housekeeping*.

**`make verify` must end with `All rounds verified.`** If a defect stops firing,
that round silently measures nothing and you cannot tell from the outside. Run it
after `make reset`, after editing any seeded file, and quarterly.

## Open questions

1. **Will the round-2 machine be pre-booted?** A fresher running
   `pip install -e .` on the clock turns a 90-minute thinking exercise into a
   50-minute one. Install flaskr beforehand, leave the browser on the target
   route.
2. **Does the brief's must-have list change to match the Python assessment?**
   If it keeps "PHP 8 OOP, day one", it screens out the people this loop is
   designed to find.

## Housekeeping

Not a git repo yet, and the first commit lands on the default branch — which
Janu's global git policy blocks Claude from doing. Run it yourself:

```
cd ~/Desktop/code/interviews
git init
git add -A
git commit -m "interview materials: rounds 1-3"
git remote add origin <private repo url>
git push -u origin HEAD
```

**Make it a private repo.** It carries answer keys and names the location of
every seeded defect.

Then on the other machine:

```
git clone <url> interviews && cd interviews
make setup && make verify
```

Expect `All rounds verified.` The PyCharm scaffold `main.py` is already deleted;
`.idea/`, venvs and `work/` are gitignored.
