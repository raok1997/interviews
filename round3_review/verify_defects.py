"""Interviewer check: prove the three seeded defects in review.diff still fire.

Run against a prepared round-3 work tree (see the Makefile):

    make verify          # runs this with the right venv and cwd

Exits non-zero if a defect has stopped behaving as ANSWER_KEY.md documents —
which would mean the round is silently measuring nothing.
"""

import os
import sqlite3
import sys
import tempfile

from flaskr import create_app
from flaskr.db import get_db, init_db
from werkzeug.security import generate_password_hash

failures = []


def check(label, ok, detail):
    print(f"  [{'ok  ' if ok else 'FAIL'}] {label}: {detail}")
    if not ok:
        failures.append(label)


def main():
    fd, path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": path})

    try:
        with app.app_context():
            init_db()
            db = get_db()
            for name in ("alice", "bob"):
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (name, generate_password_hash("x")),
                )
            db.execute(
                "INSERT INTO post (title, body, author_id, published)"
                " VALUES ('Alice secret draft', 'b', 1, 0)"
            )
            db.execute(
                "INSERT INTO post (title, body, author_id, published)"
                " VALUES ('Bob secret draft', 'b', 2, 0)"
            )
            db.commit()

        client = app.test_client()

        print("\nQ1 defect - drafts() has no login gate and no author filter")
        anon = client.get("/drafts")
        check(
            "logged-out stranger sees every user's drafts",
            anon.status_code == 200
            and b"Alice secret draft" in anon.data
            and b"Bob secret draft" in anon.data,
            f"status {anon.status_code}, both drafts visible while logged out",
        )
        client.post("/auth/login", data={"username": "alice", "password": "x"})
        as_alice = client.get("/drafts")
        check(
            "alice sees bob's drafts",
            b"Bob secret draft" in as_alice.data,
            "author_id is never filtered",
        )

        print("\nQ2 defect - checkbox value stored verbatim")
        client.post(
            "/create", data={"title": "Ticked post", "body": "b", "published": "on"}
        )
        with app.app_context():
            row = (
                get_db()
                .execute(
                    "SELECT published, typeof(published) AS t"
                    " FROM post WHERE title = 'Ticked post'"
                )
                .fetchone()
            )
        on_index = b"Ticked post" in client.get("/").data
        on_drafts = b"Ticked post" in client.get("/drafts").data
        check(
            "post ticked 'publish' lands on neither page",
            row is not None
            and row["published"] == "on"
            and row["t"] == "text"
            and not on_index
            and not on_drafts,
            f"stored {row['published']!r} as {row['t']}; "
            f"index={on_index}, drafts={on_drafts}",
        )

        print("\nQ3 defect - sqlite3.Row has no .get()")
        check(
            "Row.get does not exist",
            not hasattr(sqlite3.Row, "get"),
            "hasattr(sqlite3.Row, 'get') is False",
        )
        try:
            client.post("/1/publish")
            check("publish() raises AttributeError", False, "it did NOT raise")
        except AttributeError as e:
            check("publish() raises AttributeError", True, str(e))

        print()
        if failures:
            print(f"{len(failures)} defect(s) no longer behave as documented:")
            for f in failures:
                print(f"  - {f}")
            print("Fix review.diff or update ANSWER_KEY.md before interviewing.")
            return 1

        print("All three defects verified. ANSWER_KEY.md is accurate.")
        return 0
    finally:
        os.close(fd)
        os.unlink(path)


if __name__ == "__main__":
    sys.exit(main())
