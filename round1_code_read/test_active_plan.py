"""The test suite that ships with active_plan.py.

Shown to the candidate AFTER the three reading questions, with one prompt:
"What case is missing?"
"""

from active_plan import active_plan


def plan(id, starts_on, ends_on):
    return {"id": id, "starts_on": starts_on, "ends_on": ends_on}


def test_single_plan_covering_the_date_is_returned():
    p = plan(1, "2025-06-01", "2027-05-31")
    assert active_plan([p], "2026-04-01") is p


def test_latest_start_wins_among_covering_plans():
    older = plan(1, "2025-06-01", "2027-05-31")
    newer = plan(2, "2026-01-01", "2027-05-31")
    assert active_plan([older, newer], "2026-04-01") is newer

def test_returns_none_when_no_plan_covers_the_date():
    p = plan(1, "2024-01-01", "2024-12-31")
    assert active_plan([p], "2026-04-01") is None


def test_missing_start_means_always_started():
    p = plan(1, None, "2026-06-30")
    assert active_plan([p], "2026-04-01") is p


def test_missing_end_means_never_ends():
    p = plan(1, "2025-06-01", None)
    assert active_plan([p], "2026-04-01") is p
