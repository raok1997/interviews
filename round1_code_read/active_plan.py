"""Rate-plan lookup.

A plan is a dict: {"id": int, "starts_on": str | None, "ends_on": str | None}
Dates are ISO strings, e.g. "2026-04-01".
"""


def active_plan(plans, on_date):
    """
    Return the rate plan that applies on on_date.

      1. Keep plans covering on_date (no starts_on = always started,
         no ends_on = never ends).
      2. Latest starts_on wins.
      3. Tie-break: highest id wins.

    Returns None when no plan covers on_date.
    """
    matches = []
    for p in plans:
        started = not p["starts_on"] or p["starts_on"] <= on_date
        ended = not p["ends_on"] or p["ends_on"] >= on_date
        if started and ended:
            matches.append(p)

    if not matches:
        return None

    matches.sort(key=lambda p: (p["starts_on"] or "", -p["id"]), reverse=True)
    return matches[0]
