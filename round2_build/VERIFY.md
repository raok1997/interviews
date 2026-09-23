# Round 2 — preparing the machine

**Do this the day before, not on the morning.** A fresher who spends 40 of 90
minutes on environment friction turns this into a 50-minute round, and you
measure nothing.

## One-time setup

```bash
cd ~/Desktop/code/interviews/round2_build

python3 -m venv .venv
.venv/bin/pip install -e app
.venv/bin/pip install pytest

# confirm the starter is green - expect "24 passed"
cd app && ../.venv/bin/python -m pytest -q && cd ..

# confirm the seeded defects still work - expect "All three defects verified"
.venv/bin/python verify_defects.py
```

## On the interview machine, before they sit down

```bash
cd ~/Desktop/code/interviews/round2_build/app

../.venv/bin/flask --app flaskr init-db
../.venv/bin/flask --app flaskr run --debug
```

Then, in a browser:

1. Register a user (the app has no seeded login) — something obvious like
   `test` / `test`.
2. Load the sample posts:
   ```bash
   cd ~/Desktop/code/interviews/round2_build
   .venv/bin/python seed_dev_data.py
   ```
   Expect `Added 30 posts` and `14 titles match 'apple'`. The 14 matters —
   it is above `DEFAULT_LIMIT` (10), which is what makes defect 2 visible on
   screen rather than theoretical.
3. Leave the browser open on http://127.0.0.1:5000, logged in, posts showing.
4. Open the editor on `flaskr/blog.py` and `flaskr/search.py`.
5. Confirm their AI tool of choice is installed and signed in. **Ask them the
   day before which one they use.**

## Handing over the files

The candidate gets `TASK.md` and the `app/` directory. They must **not** get:

- `ANSWER_KEY.md`
- `verify_defects.py`
- `VERIFY.md` (this file)
- `seed_dev_data.py`

Safest is to prepare the machine yourself and let them work on it — no copying,
nothing to leak. If you do need to hand over a copy:

```bash
mkdir -p /tmp/round2 && cp -R app /tmp/round2/ && cp TASK.md /tmp/round2/
grep -ril "answer\|defect\|seeded" /tmp/round2 || echo "clean"
```

## After each candidate

Reset so the next one starts identically:

```bash
cd ~/Desktop/code/interviews/round2_build
git -C ~/Desktop/code/interviews checkout -- round2_build/app   # if under git
rm -f app/instance/flaskr.sqlite
```

Then re-run the setup steps above. **Re-run `verify_defects.py` too** — if a
previous candidate edited `search.py` and it wasn't reset, the round is
measuring nothing and you won't be able to tell from the outside.

## Quarterly

Re-run `verify_defects.py` and re-read `ANSWER_KEY.md`. Rotate the defects if a
candidate ever turns up already knowing what's in them.
