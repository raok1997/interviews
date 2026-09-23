# Round 3 — answer key

**Interviewer only. Never goes in a candidate's copy.**

Every output below was produced by running the patched app. Re-verify with
`make verify` after touching `review.diff`.

---

## The setup

`review.diff` — 139 lines, 6 files — applies cleanly to the pristine baseline in
`app/` and adds a plausible drafts feature. It was **generated** from a real
working tree, not hand-written, so it always applies.

**The suite is green on this branch: 24 passed.** That is the point of the
round. Round 1 taught *the bug lives where the tests don't look*; round 3 says
*the tests can all pass and the code can still be wrong*. Say this out loud at
the end regardless of how they did — it is the most portable thing they take
away.

One defect per category, each in a different function, mapped 1:1 onto the three
questions in `QUESTIONS.md`.

---

## Q1 → Defect: `drafts()` does not do what its name says

**Category: convention violation. Consequence: security.**

```python
@bp.route("/drafts")
def drafts():
    """Show the current user's unpublished drafts."""
```

Two things are missing and they compound:

- no `@login_required` — every other authenticated route in `blog.py` has it
- no `WHERE author_id = ?` — the query filters on `published` only

Verified against the running app:

```
logged out   -> status 200 | Alice's draft visible: True | Bob's: True
as alice     -> sees Bob's draft: True
```

**A logged-out stranger can read every user's unpublished drafts.** The
docstring says "the current user's". The function has no concept of a current
user at all.

**What to listen for.** The gettable version is "it's missing `@login_required`"
— compare it against `create`/`update`/`delete` two screens up and it stands
out. A **4** notices the second half: even *with* login, the query still returns
everyone's rows. Most candidates stop at the decorator; ask *"suppose I add
`@login_required` — is it fixed?"* to separate 3 from 4.

---

## Q2 → Defect: the checkbox value reaches the database intact

**Category: silent wrong value.**

```python
published = request.form.get("published")
...
    "INSERT INTO post (title, body, author_id, published) VALUES (?, ?, ?, ?)",
    (title, body, g.user["id"], published),
```

An HTML checkbox submits the string `"on"` when ticked and **is not submitted at
all** when unticked. So `published` is `"on"` or `None` — never `1` or `0`.
SQLite is dynamically typed and stores it as-is:

```
stored published = 'on'  typeof = text
on index page?  False        (index filters WHERE published = 1)
on drafts page? False        (drafts filters WHERE published = 0)
```

**A post created with "Publish immediately" ticked appears on neither page.** It
is in the database. Nothing raised. No error was shown to the user.

The unticked case is just as bad in the other direction: `None` → `NULL`, and
`NULL = 0` is not true in SQL, so the draft never shows on the drafts page
either.

**What to listen for.** A **2** says "it should be converted to an integer". A
**3** knows unchecked boxes aren't submitted, so `None` is the default path. A
**4** gets to *where* it fails — that a column declared `INTEGER` accepted the
text `'on'` without complaint, which is the part people assume can't happen.

If they head for the debugger, `SELECT typeof(published)` is the fastest route
and worth pointing at if they're close.

---

## Q3 → Defect: `post.get("published")` — the method doesn't exist

**Category: invented API.**

```python
post = get_post(id)
if post.get("published") == 1:
```

```
AttributeError: 'sqlite3.Row' object has no attribute 'get'
```

`get_post` returns a `sqlite3.Row`. Row supports `row["published"]` and
`row.keys()` — it looks dict-like, which is exactly why this passes a skim — but
it has no `.get()`. Verified: `hasattr(sqlite3.Row, "get")` is `False`.

Not covered by the suite, which is why the branch is green.

**What to listen for — this is the criterion the whole loop is built around.**

| | |
|---|---|
| **1** | Reads past it. Row is dict-like, `.get()` is a dict method, looks fine. |
| **2** | Checks it exists when we point at the line. |
| **3** | Checks it *and* can say how — `hasattr`, the REPL, the docs, running it. |
| **4** | Flags it while reading, unprompted, and says why it smelled wrong. |

The follow-up matters more than the finding: **"how do you know?"** An answer of
"I asked Claude and it said Row has no `.get`" is a 2, not a 3 — unless they
then went and checked. Say so in your notes.

---

## Running the round

- Give them `QUESTIONS.md` and the checked-out branch. Let them run it.
- **Don't confirm or deny as they go.** "Interesting — keep going" for everything,
  right or wrong. A candidate who reads your face stops reasoning.
- If 15 minutes pass with nothing, point at a *file* — not a line. "Anything
  stand out in `drafts()`?" is a legitimate nudge; note that you gave it.
- Last 10 minutes are the team conversation. Ask how they'd want this fed back
  to the teammate who wrote it — you learn more about whether they can work on a
  team from that than from anything in the diff.

## Scoring

Feeds the same criteria as rounds 1 and 2; see `../scorecard/anchors.md`.

- **Catches confident wrongness (×3)** — anchors above, from Q3.
- **Works inside conventions (×2)** — Q1: did they compare against the
  neighbouring routes, or judge the function in isolation?
- **Temperament for exact numbers (×2)** — Q2: did they trace the value end to
  end, or stop at "should be an int"?
- **Curiosity / self-directed (×2)** — what did they go and look up unprompted?

**Two defended findings beat six asserted ones.** A candidate who finds only Q1
but can say exactly who can see what, and what they'd change, is a stronger hire
than one who lists all three vaguely.
