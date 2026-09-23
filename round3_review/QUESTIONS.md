# Code review — drafts feature

**About 40 minutes of the round. Use AI tools if you want to; ask us anything.**

A teammate has opened a pull request against Flaskr — the same blog app you
worked in last time. It adds a **drafts** feature:

- A post can be published or held back as a draft.
- The index page shows only published posts.
- A new `/drafts` page shows the current user's unpublished drafts.
- A draft can be published from there.

The change is in `review.diff` — 139 lines across 6 files. **The test suite
passes on this branch.**

Your job is to review it the way you'd want your own work reviewed. Read it,
say what you find, and tell us what you'd want changed before it merges.

---

## Three questions to work through

Take them in any order. Talk out loud — we're more interested in how you arrive
somewhere than in whether you land on the answer.

1. **Does each function do what its name and docstring say it does?**

2. **What happens when a value is missing or null?** Trace at least one value
   from the form all the way to the database and back onto a page.

3. **Does every method being called actually exist?** Pick one you're not
   certain about and tell us how you'd check.

---

## What you can use

- The app is checked out and installed. You can run it, run the tests, add
  print statements, open a Python shell — whatever you'd normally do.
- The Flask, Jinja and Python docs are open.
- AI tools are fine. If you ask one something, tell us what you asked and what
  you did with the answer.

## What we are not looking for

- Style nits, naming preferences, or anything a formatter would fix.
- A complete list. Two findings you can explain and defend beat six you can't.
