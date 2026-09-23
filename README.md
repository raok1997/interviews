# Interview materials

Assessment materials for one engineering hire. Three rounds, all run on site.

> **This repo is for interviewers only.** It holds the answer keys. Candidates
> never see it. They get a stripped machine (see below). Read
> **[CONTEXT.md](CONTEXT.md)** first.

## The rounds

| Round | Candidate gets | AI tools |
|---|---|---|
| 1: code read | `active_plan.py`, then `test_active_plan.py` after the three questions | **off** |
| 2: observed build | `work\round2` + `TASK.md`, app running with sample posts | on |
| 3: reverse code review | `review.diff` + `QUESTIONS.md`, app running from `work\round3` | on |

The round 3 test suite passes on purpose. Answer keys are in each round's
`ANSWER_KEY.md`.

## Preparing the candidate workstation (Windows)

Needs **Python 3.11+**, **git** and **make** on `PATH`. Use **PowerShell**,
and run each command on its own line. Windows PowerShell 5.1 has no `&&`.
No network is needed at interview time.

The candidate gets a shell on this machine, so anything left on disk can be
read. Build everything first, copy out what the candidate needs, then delete
the interviewer files.

### 1. Build and verify

```powershell
git clone <private repo url> interviews
cd interviews
make setup
make verify
```

`make verify` must end with `All rounds verified.` If it doesn't, **stop**. A
round whose defect no longer triggers measures nothing.

### 2. Seed round 2

```powershell
make run-round2
```

Open http://127.0.0.1:5000 and register a user. Then run this in a **second**
PowerShell window:

```powershell
make seed-round2
```

It should report 14 posts matching "apple". Stop the server with Ctrl+C.
**Don't run `make run-round2` again after this:** it resets the database and
deletes the seeded posts.

### 3. Initialise round 3's database

```powershell
make run-round3
```

Once it's serving, stop it with Ctrl+C.

### 4. Stage the candidate files

```powershell
make candidate
```

This creates everything the candidate needs:

| Round | Files on the stripped machine |
|---|---|
| 1 | `candidate\r1\active_plan.py` |
| 2 | `candidate\r2\TASK.md` + the app in `work\round2` |
| 3 | `candidate\r3\QUESTIONS.md`, `candidate\r3\review.diff` + the app in `work\round3` |

Round 1 has no app, so it has no folder under `work\`.

Copy `round1_code_read\test_active_plan.py` to a USB stick or your laptop, **not**
this machine. You hand it over only after the round 1 questions.

### 5. Strip the machine

```powershell
make strip
```

It checks the machine first: all the files in the table above, both
virtualenvs, a round 2 database with a user and 14 "apple" posts, and a round 3
database. If anything is missing, it lists the problem and **deletes nothing**.
Fix it and run `make strip` again.

When every check passes, it deletes all the interviewer files, including
`.git`, whose history holds every answer key. It ends by listing what's left:
only `work` and `candidate`.

**Don't move or rename `work\`.** Its virtualenvs are tied to its absolute path.

### 6. Start the apps during the interview

The Makefile is gone after the strip, so start the apps directly. **Don't run
`init-db`,** because it wipes the database.

```powershell
cd work\round2
.\.venv\Scripts\python -m flask --app flaskr run --debug
```

For round 3, do the same from `work\round3`. Only one app can use port 5000 at
a time.

## Between candidates

The stripped machine can't be reset in place. Delete the whole `interviews`
folder and repeat the steps above from a fresh clone.

## Never hand over

Only the contents of `work\` and `candidate\` are safe to give a candidate.
Never give them any `ANSWER_KEY.md`, `VERIFY.md`, `verify_defects.py`,
`seed_dev_data.py`, `round2_build\seed\`, `CONTEXT.md` or `scorecard\`.

## Maintenance (on an interviewer machine, not the candidate's)

`make` lists all targets. Run `make verify` every quarter. Rotate a defect if a
candidate already knows it. `app\` is the pristine Flask tutorial app
(BSD-3-Clause, see `app\LICENSE.txt`). Never edit it.
