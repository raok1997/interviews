"""Interviewer prep: load sample posts into the dev database.

Run once when setting up the interview machine, AFTER `flask --app flaskr init-db`.
Gives the candidate enough rows that a broken limit is visible on screen.

    make seed-round2
"""

from flaskr import create_app
from flaskr.db import get_db

TITLES = [
    "Apple harvest report 2024",
    "Apple harvest report 2025",
    "Apple storage costs",
    "Apple pricing review",
    "Banana shipping delays",
    "Banana ripening study",
    "Cherry orchard survey",
    "Cherry pest control",
    "Quarterly apple summary",
    "Quarterly banana summary",
    "Cold chain audit",
    "Cold storage maintenance",
    "Packing line downtime",
    "Packing materials cost",
    "Export licence renewal",
    "Export volume forecast",
    "Retail contract terms",
    "Retail shelf placement",
    "Apple variety trials",
    "Apple export pricing",
    "Weekly apple stock",
    "Weekly banana stock",
    "Warehouse lease notes",
    "Warehouse safety check",
    "Season close-out apple",
    "Apple juice line proposal",
    "Apple crate standards",
    "Apple grower contacts",
    "Apple freight quotes",
    "Apple insurance renewal",
]


def main():
    app = create_app()
    with app.app_context():
        db = get_db()
        user = db.execute("SELECT id FROM user LIMIT 1").fetchone()
        if user is None:
            print("No user yet. Register one in the app first, then re-run.")
            return
        author_id = user["id"]

        existing = db.execute("SELECT COUNT(*) AS n FROM post").fetchone()["n"]
        for title in TITLES:
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, f"Body text for: {title}", author_id),
            )
        db.commit()
        total = db.execute("SELECT COUNT(*) AS n FROM post").fetchone()["n"]
        matching = sum(1 for t in TITLES if "apple" in t.lower())
        print(f"Added {len(TITLES)} posts ({existing} -> {total}).")
        print(
            f"{matching} titles match 'apple' — above DEFAULT_LIMIT (10), so a "
            "broken limit is visible on screen."
        )


if __name__ == "__main__":
    main()
