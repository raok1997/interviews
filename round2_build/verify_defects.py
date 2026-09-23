"""Interviewer check: prove all three seeded defects still behave as documented.

Run after any edit to app/flaskr/search.py, and once when preparing the machine.
Exits non-zero if a defect has stopped working — which would mean the round is
silently measuring nothing.

    make verify
"""

import os
import sys
import tempfile

from flaskr import create_app
from flaskr import search
from flaskr.db import get_db, init_db

failures = []


def check(label, ok, detail):
    status = "ok  " if ok else "FAIL"
    print(f"  [{status}] {label}: {detail}")
    if not ok:
        failures.append(label)


def main():
    fd, path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": path})

    try:
        with app.app_context():
            init_db()
            db = get_db()
            db.execute("INSERT INTO user (username, password) VALUES ('t','x')")
            for i in range(1, 26):
                db.execute(
                    "INSERT INTO post (title, body, author_id) VALUES (?,?,1)",
                    (f"apple report {i}", "body"),
                )
            db.commit()

            print("\nDefect 1 - clean_terms mutable default")
            first = search.clean_terms("apple")
            second = search.clean_terms("banana")
            check(
                "accumulates across calls",
                second[0] == "apple" and len(second) == 2,
                f"second call returned {second}",
            )

            print("\nDefect 2 - find_posts limit default")
            unlimited = len(search.find_posts("apple"))
            explicit = len(search.find_posts("apple", 10))
            check(
                "default limit not applied",
                unlimited == 25 and explicit == 10,
                f"no limit -> {unlimited} rows (DEFAULT_LIMIT is "
                f"{search.DEFAULT_LIMIT}), explicit 10 -> {explicit} rows",
            )

            print("\nDefect 3 - count_matches invented API")
            try:
                search.count_matches("apple")
                check("raises AttributeError", False, "it did NOT raise")
            except AttributeError as e:
                check("raises AttributeError", True, str(e))

        print()
        if failures:
            print(f"{len(failures)} defect(s) no longer behave as documented:")
            for f in failures:
                print(f"  - {f}")
            print("Fix search.py or update ANSWER_KEY.md before interviewing.")
            return 1

        print("All three defects verified. ANSWER_KEY.md is accurate.")
        return 0
    finally:
        os.close(fd)
        os.unlink(path)


if __name__ == "__main__":
    sys.exit(main())
