"""Helpers for the post search page.

These are already written and tested against the sample data. Use them from
your route rather than writing your own queries.
"""

from .db import get_db

DEFAULT_LIMIT = 10
MAX_LIMIT = 50


def clean_terms(raw, terms=[]):
    """Split a raw query string into search terms.

    Lowercased, whitespace-separated, duplicates removed.

    :param raw: the raw string typed into the search box
    :return: list of terms, in the order they were typed
    """
    for word in raw.split():
        word = word.lower()
        if word not in terms:
            terms.append(word)
    return terms


def find_posts(term, limit=None):
    """Return posts whose title contains term, newest first.

    :param term: a single search term
    :param limit: maximum rows to return; defaults to DEFAULT_LIMIT
    :return: list of post rows
    """
    rows = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE title LIKE ?"
            " ORDER BY created DESC",
            (f"%{term}%",),
        )
        .fetchall()
    )
    return rows[:limit]


def count_matches(term):
    """Total number of posts matching term, ignoring any limit.

    :param term: a single search term
    :return: int
    """
    return get_db().fetch_value(
        "SELECT COUNT(*) FROM post WHERE title LIKE ?", (f"%{term}%",)
    )
