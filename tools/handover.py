"""Interviewer prep: stage the candidate files, then strip the workstation.

    make candidate    copy every file the candidate needs into candidate/
    make strip        check everything is in place, then delete the interviewer files

Plain Python, so it behaves the same from PowerShell, cmd.exe or bash. `strip`
refuses to delete anything until every check passes, because once the repo is
gone the missing files can't be recovered on this machine.
"""

import os
import shutil
import sqlite3
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# candidate path -> source in the repo. test_active_plan.py is deliberately not
# here: it stays off the machine until the round 1 questions are done.
STAGED = {
    "candidate/r1/active_plan.py": "round1_code_read/active_plan.py",
    "candidate/r2/TASK.md": "round2_build/TASK.md",
    "candidate/r3/QUESTIONS.md": "round3_review/QUESTIONS.md",
    "candidate/r3/review.diff": "round3_review/review.diff",
}

INTERVIEWER_ONLY = [
    "app", "round1_code_read", "round2_build", "round3_review", "scorecard",
    "tools", "README.md", "CONTEXT.md", "Makefile", ".gitignore",
    ".pytest_cache", ".git",
]

FORBIDDEN_NAMES = {
    "ANSWER_KEY.md", "VERIFY.md", "CONTEXT.md", "verify_defects.py",
    "seed_dev_data.py", "anchors.md",
}

KEEP = {"work", "candidate"}


def venv_python(work_tree):
    sub = "Scripts/python.exe" if os.name == "nt" else "bin/python"
    return work_tree / ".venv" / sub


def stage():
    for dest, src in STAGED.items():
        src_path, dest_path = ROOT / src, ROOT / dest
        if not src_path.is_file():
            sys.exit(f"Missing source {src}. Is this a full clone?")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)
        print(f"  {dest}")
    print("Staged. Put round1_code_read/test_active_plan.py on a USB stick or")
    print("your laptop, not this machine, then run 'make strip'.")


def problems_before_strip():
    problems = []
    for dest in STAGED:
        path = ROOT / dest
        if not path.is_file() or path.stat().st_size == 0:
            problems.append(f"{dest} is missing. Run 'make candidate'.")

    for name in ("round2", "round3"):
        tree = ROOT / "work" / name
        if not venv_python(tree).is_file():
            problems.append(f"work/{name} has no virtualenv. Run 'make setup'.")

    db2 = ROOT / "work/round2/instance/flaskr.sqlite"
    if not db2.is_file():
        problems.append("Round 2 database missing. Do step 2 (run-round2, register, seed-round2).")
    else:
        con = sqlite3.connect(db2)
        try:
            users = con.execute("SELECT COUNT(*) FROM user").fetchone()[0]
            apples = con.execute(
                "SELECT COUNT(*) FROM post WHERE lower(title) LIKE '%apple%'"
            ).fetchone()[0]
        except sqlite3.Error as exc:
            problems.append(f"Round 2 database unreadable ({exc}). Redo step 2.")
        else:
            if users == 0:
                problems.append("Round 2 has no user. Register one, then run 'make seed-round2'.")
            if apples < 14:
                problems.append(
                    f"Round 2 has {apples} posts matching 'apple', expected 14. Run 'make seed-round2'."
                )
        finally:
            con.close()

    if not (ROOT / "work/round3/instance/flaskr.sqlite").is_file():
        problems.append("Round 3 database missing. Do step 3 (make run-round3).")

    return problems


def force_writable(func, path, _exc):
    # .git pack files are read-only on Windows and rmtree can't delete them otherwise.
    os.chmod(path, stat.S_IWRITE)
    func(path)


def strip():
    problems = problems_before_strip()
    if problems:
        print("Not stripping. Nothing was deleted. Fix these first:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    for name in INTERVIEWER_ONLY:
        path = ROOT / name
        if path.is_dir():
            shutil.rmtree(path, onerror=force_writable)
        elif path.exists():
            path.unlink()

    leftovers = sorted(p.name for p in ROOT.iterdir() if p.name not in KEEP)
    leaked = sorted(
        str(Path(dirpath, f).relative_to(ROOT))
        for dirpath, _, files in os.walk(ROOT)
        for f in files
        if f in FORBIDDEN_NAMES
    )
    if leftovers or leaked:
        print("Stripped, but these are still on disk. Delete them before the candidate sits down:")
        for p in leftovers + leaked:
            print(f"  - {p}")
        sys.exit(1)

    print("Stripped. Left on disk:")
    for p in sorted(ROOT.iterdir()):
        print(f"  {p.name}")
    for dest in STAGED:
        print(f"  {dest}")


if __name__ == "__main__":
    commands = {"stage": stage, "strip": strip}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit("usage: handover.py stage|strip")
    commands[sys.argv[1]]()
