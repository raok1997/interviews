PY ?= python
WORK := work
R2 := $(WORK)/round2
R3 := $(WORK)/round3

ifeq ($(OS),Windows_NT)
VENV_BIN := Scripts
VENV_RUN := .\.venv\Scripts\python
BLANK_ECHO := echo.
R1_OUT ?= candidate/r1
else
VENV_BIN := bin
VENV_RUN := ./.venv/bin/python
BLANK_ECHO := echo
R1_OUT ?= /tmp/r1
endif

R2_PY := $(R2)/.venv/$(VENV_BIN)/python
R3_PY := $(R3)/.venv/$(VENV_BIN)/python

define REMOVE_DIR
$(PY) -c "import shutil; shutil.rmtree('$(1)', ignore_errors=True)"
endef

define COPY_DIR
$(PY) -c "import shutil; shutil.copytree('$(1)', '$(2)')"
endef

define COPY_FILE
$(PY) -c "import shutil; shutil.copy2('$(1)', '$(2)')"
endef

define MAKE_DIR
$(PY) -c "from pathlib import Path; Path('$(1)').mkdir(parents=True, exist_ok=True)"
endef

define TOUCH_FILE
$(PY) -c "from pathlib import Path; Path('$(1)').touch()"
endef

.DEFAULT_GOAL := help

.PHONY: help setup verify reset clean run-round2 run-round3 seed-round2 test-round1 candidate-round1

help:
	@echo "Interview materials — see README.md"
	@$(BLANK_ECHO)
	@echo "  make setup            build work/round2 and work/round3 from app/ (first thing on a new machine)"
	@echo "  make verify           prove every seeded defect still fires, and both suites are green"
	@echo "  make reset            throw away work/ and rebuild — run between candidates"
	@$(BLANK_ECHO)
	@echo "  make run-round2       start the round-2 app on :5000"
	@echo "  make seed-round2      load sample posts (after registering a user)"
	@echo "  make run-round3       start the round-3 app on :5000"
	@echo "  make test-round1      run the round-1 doctest suite"
	@$(BLANK_ECHO)
	@echo "  make candidate-round1 copy round-1 candidate files to /tmp/r1"
	@echo "  make clean            remove work/ entirely"

# ---------------------------------------------------------------- setup

setup: $(R2)/.ready $(R3)/.ready
	@$(BLANK_ECHO)
	@echo "Ready. 'make verify' to confirm, then see README.md."

$(R2)/.ready:
	@echo "==> building round 2"
	@$(call REMOVE_DIR,$(R2))
	@$(call MAKE_DIR,$(WORK))
	@$(call COPY_DIR,app,$(R2))
	@$(call COPY_FILE,round2_build/seed/search.py,$(R2)/flaskr/search.py)
	@$(PY) -m venv $(R2)/.venv
	@$(R2_PY) -m pip install -q --upgrade pip
	@$(R2_PY) -m pip install -q -e $(R2)
	@$(R2_PY) -m pip install -q pytest
	@$(call TOUCH_FILE,$@)

$(R3)/.ready:
	@echo "==> building round 3"
	@$(call REMOVE_DIR,$(R3))
	@$(call MAKE_DIR,$(WORK))
	@$(call COPY_DIR,app,$(R3))
	@git apply --directory=$(R3) --quiet round3_review/review.diff
	@$(PY) -m venv $(R3)/.venv
	@$(R3_PY) -m pip install -q --upgrade pip
	@$(R3_PY) -m pip install -q -e $(R3)
	@$(R3_PY) -m pip install -q pytest
	@$(call TOUCH_FILE,$@)

# ---------------------------------------------------------------- verify

verify: setup
	@echo "==> round 1 suite (expect 5 passed)"
	@$(R2_PY) -m pytest round1_code_read -q
	@$(BLANK_ECHO)
	@echo "==> round 2 upstream suite (expect 24 passed)"
	@cd $(R2) && $(VENV_RUN) -m pytest -q
	@echo "==> round 2 seeded defects"
	@cd $(R2) && $(VENV_RUN) ../../round2_build/verify_defects.py
	@$(BLANK_ECHO)
	@echo "==> round 3 upstream suite (expect 24 passed — green is the point)"
	@cd $(R3) && $(VENV_RUN) -m pytest -q
	@echo "==> round 3 seeded defects"
	@cd $(R3) && $(VENV_RUN) ../../round3_review/verify_defects.py
	@$(BLANK_ECHO)
	@echo "All rounds verified."

test-round1: $(R2)/.ready
	@$(R2_PY) -m pytest round1_code_read -q

# ---------------------------------------------------------------- running

run-round2: $(R2)/.ready
	@echo "http://127.0.0.1:5000 — register a user, then 'make seed-round2' in another shell"
	@cd $(R2) && $(VENV_RUN) -m flask --app flaskr init-db && $(VENV_RUN) -m flask --app flaskr run --debug

seed-round2: $(R2)/.ready
	@cd $(R2) && $(VENV_RUN) ../../round2_build/seed_dev_data.py

run-round3: $(R3)/.ready
	@echo "http://127.0.0.1:5000"
	@cd $(R3) && $(VENV_RUN) -m flask --app flaskr init-db && $(VENV_RUN) -m flask --app flaskr run --debug

# ---------------------------------------------------------------- handing over

candidate-round1:
	@$(call REMOVE_DIR,$(R1_OUT))
	@$(call MAKE_DIR,$(R1_OUT))
	@$(call COPY_FILE,round1_code_read/active_plan.py,$(R1_OUT)/active_plan.py)
	@echo "$(R1_OUT)/active_plan.py — hand this over."
	@echo "Add test_active_plan.py ONLY after the three questions are done:"
	@echo "  cp round1_code_read/test_active_plan.py /tmp/r1/"

# ---------------------------------------------------------------- cleanup

reset: clean setup
	@echo "Work trees rebuilt from app/. Re-run 'make verify' before the next candidate."

clean:
	@$(call REMOVE_DIR,$(WORK))
	@echo "work/ removed."
