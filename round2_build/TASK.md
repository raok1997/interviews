# Build task — search for posts

**90 minutes. Use whatever AI tools you normally use — we expect you to.**

You're working in Flaskr, the blog app from the official Flask tutorial. It's
already installed and running, and the database already has posts in it.

You won't be judged on finishing. We're interested in how you work.

---

## What to build

A search page that finds posts by title.

1. **A new route:** `GET /search`
2. It takes a query-string parameter `q` — the text typed into the search box.
3. **Validation:** if `q` is missing or shorter than 2 characters, flash the
   message `Search term must be at least 2 characters.` and show no results.
4. Otherwise show the matching posts, newest first — title, author and date, the
   same way the index page shows them.
5. Show a heading with the total number of matches, e.g. `14 results for apple`.
   The total is the number of matching posts, **not** the number displayed.
6. At most 10 posts on the page.

A link to the search page from the nav bar is a nice touch if you have time. It
is not required.

## Where things are

| You'll need | File |
|---|---|
| Routes for the blog | `flaskr/blog.py` |
| **Search helpers — use these, don't write your own queries** | `flaskr/search.py` |
| Templates | `flaskr/templates/blog/` |
| Database access | `flaskr/db.py` |

## Running it

The app is already running at http://127.0.0.1:5000 with reload enabled — save a
file and refresh the page.

To run the tests:

```
python -m pytest
```

They pass right now. Keep them passing.

## Ground rules

- Use AI tools freely. Ask us questions freely too.
- Anything in `flaskr/search.py` is fair game to change if you need to.
- If something behaves oddly, say so out loud — that's useful to us either way.
