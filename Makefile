PY ?= python3
WORK := work
R2 := $(WORK)/round2
R3 := $(WORK)/round3

.DEFAULT_GOAL := help

.PHONY: help setup verify reset clean run-round2 run-round3 seed-round2 test-round1 candidate-round1

help:
	@echo "Interview materials — see README.md"
	@echo
	@echo "  make setup            build work/round2 and work/round3 from app/ (first thing on a new machine)"
	@echo "  make verify           prove every seeded defect still fires, and both suites are green"
	@echo "  make reset            throw away work/ and rebuild — run between candidates"
	@echo
	@echo "  make run-round2       start the round-2 app on :5000"
	@echo "  make seed-round2      load sample posts (after registering a user)"
	@echo "  make run-round3       start the round-3 app on :5000"
	@echo "  make test-round1      run the round-1 doctest suite"
	@echo
	@echo "  make candidate-round1 copy round-1 candidate files to /tmp/r1"
	@echo "  make clean            remove work/ entirely"

# ---------------------------------------------------------------- setup

setup: $(R2)/.ready $(R3)/.ready
	@echo
	@echo "Ready. 'make verify' to confirm, then see README.md."

$(R2)/.ready:
	@echo "==> building round 2"
	@rm -rf $(R2) && mkdir -p $(WORK)
	@cp -R app $(R2)
	@cp round2_build/seed/search.py $(R2)/flaskr/search.py
	@$(PY) -m venv $(R2)/.venv
	@$(R2)/.venv/bin/pip install -q --upgrade pip
	@$(R2)/.venv/bin/pip install -q -e $(R2)
	@$(R2)/.venv/bin/pip install -q pytest
	@touch $@

$(R3)/.ready:
	@echo "==> building round 3"
	@rm -rf $(R3) && mkdir -p $(WORK)
	@cp -R app $(R3)
	@cd $(R3) && patch -p1 --silent < ../../round3_review/review.diff
	@$(PY) -m venv $(R3)/.venv
	@$(R3)/.venv/bin/pip install -q --upgrade pip
	@$(R3)/.venv/bin/pip install -q -e $(R3)
	@$(R3)/.venv/bin/pip install -q pytest
	@touch $@

# ---------------------------------------------------------------- verify

verify: setup
	@echo "==> round 1 suite (expect 5 passed)"
	@$(R2)/.venv/bin/python -m pytest round1_code_read -q
	@echo
	@echo "==> round 2 upstream suite (expect 24 passed)"
	@cd $(R2) && .venv/bin/python -m pytest -q
	@echo "==> round 2 seeded defects"
	@cd $(R2) && .venv/bin/python ../../round2_build/verify_defects.py
	@echo
	@echo "==> round 3 upstream suite (expect 24 passed — green is the point)"
	@cd $(R3) && .venv/bin/python -m pytest -q
	@echo "==> round 3 seeded defects"
	@cd $(R3) && .venv/bin/python ../../round3_review/verify_defects.py
	@echo
	@echo "All rounds verified."

test-round1: $(R2)/.ready
	@$(R2)/.venv/bin/python -m pytest round1_code_read -q

# ---------------------------------------------------------------- running

run-round2: $(R2)/.ready
	@echo "http://127.0.0.1:5000 — register a user, then 'make seed-round2' in another shell"
	@cd $(R2) && .venv/bin/flask --app flaskr init-db && .venv/bin/flask --app flaskr run --debug

seed-round2: $(R2)/.ready
	@cd $(R2) && .venv/bin/python ../../round2_build/seed_dev_data.py

run-round3: $(R3)/.ready
	@echo "http://127.0.0.1:5000"
	@cd $(R3) && .venv/bin/flask --app flaskr init-db && .venv/bin/flask --app flaskr run --debug

# ---------------------------------------------------------------- handing over

candidate-round1:
	@rm -rf /tmp/r1 && mkdir -p /tmp/r1
	@cp round1_code_read/active_plan.py /tmp/r1/
	@echo "/tmp/r1/active_plan.py — hand this over."
	@echo "Add test_active_plan.py ONLY after the three questions are done:"
	@echo "  cp round1_code_read/test_active_plan.py /tmp/r1/"

# ---------------------------------------------------------------- cleanup

reset: clean setup
	@echo "Work trees rebuilt from app/. Re-run 'make verify' before the next candidate."

clean:
	@rm -rf $(WORK)
	@echo "work/ removed."
