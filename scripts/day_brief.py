#!/usr/bin/env python
"""Print one day's working set, projected out of the plan instead of read from it whole.

Writing a day used to mean opening `docs/00_MASTER_PLAN.md` (120 KB), the tracker, the
curriculum index and two neighbouring days to find, in the end, two rows and a list of what
has already been taught. This prints those, and only those, copied verbatim with their
source paths.

**Nothing here is generated**, so it cannot invent a requirement the plan does not contain
— which is the only reason it is safe to substitute for reading those tables. It is a
projection, and a projection may replace a *lookup*. It may never replace a *judgement*:
plan §24 (the depth contract), §6 (the five silent failures) and §4.2 (the ethics rule) are
prose that decides whether a day is good enough. They are read in full, every time. If you
are ever choosing between loading fewer tokens and reading the depth contract, read the
depth contract.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from plan_check import CURRICULA, PHASES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DAYS = ROOT / "days"
DOCS = ROOT / "docs"


def concept_text(cid: str) -> str:
    prefix, num = cid.rsplit("-", 1)
    name, concepts = CURRICULA[prefix]
    return concepts[int(num) - 1]


def day_dir_for(n: int) -> Path | None:
    if not DAYS.is_dir():
        return None
    for d in sorted(DAYS.iterdir()):
        if d.is_dir() and d.name.startswith(f"day-{n:03d}-"):
            return d
    return None


def part_list(n: int) -> list[str]:
    d = day_dir_for(n)
    if d is None:
        return []
    parts = d / "parts"
    if not parts.is_dir():
        return []
    out = []
    for f in sorted(parts.rglob("*.md"), key=lambda p: (p.parent.name, p.name)):
        title = ""
        for line in f.read_text(encoding="utf-8").splitlines()[1:12]:
            if line.startswith("title:"):
                title = line.partition(":")[2].strip().strip("\"'")
                break
        out.append(f"{f.relative_to(parts).as_posix()} — {title}")
    return out


def last_progress_row() -> str:
    p = DOCS / "PROGRESS.md"
    if not p.exists():
        return "docs/PROGRESS.md does not exist yet"
    rows = [
        ln
        for ln in p.read_text(encoding="utf-8").splitlines()
        if re.match(r"^\|\s*\d{1,3}\s*\|", ln)
    ]
    return rows[-1] if rows else "no rows yet — nothing is complete"


def ledger_tail(name: str, n: int = 4) -> list[str]:
    p = DOCS / name
    if not p.exists():
        return [f"{name} does not exist yet"]
    rows = [
        ln
        for ln in p.read_text(encoding="utf-8").splitlines()
        if ln.startswith("|") and not re.match(r"^\|\s*[-: ]+\|", ln)
    ]
    return rows[-n:] if rows else [f"{name} has no rows yet"]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: day_brief.py <day>")
        return 1
    n = int(sys.argv[1])

    phase = next((p for p in PHASES for d in p.days if d.n == n), None)
    day = next((d for p in PHASES for d in p.days if d.n == n), None)
    if phase is None or day is None:
        print(f"FAIL day {n} is not in the plan's day map (§23)")
        return 1

    w = 86
    print("=" * w)
    print(f"DAY {n} BRIEF — projected from scripts/plan_check.py and docs/")
    print("=" * w)
    print()
    print("  This is a LOOKUP, not the contract. Read plan §24 (depth), §6 (the five silent")
    print("  failures) and §4.2 (the ethics rule) in full before writing a line.")
    print()

    print("-" * w)
    print(f"PHASE {phase.n} — {phase.name}")
    print("-" * w)
    ns = [d.n for d in phase.days]
    print(f"  days  : {ns[0]}" + ("" if len(ns) == 1 else f"–{ns[-1]}"))
    print("  gate  :")
    for line in re.findall(r".{1,76}(?:\s|$)", phase.gate):
        print(f"          {line.strip()}")
    print()

    print("-" * w)
    print(f"DAY {n} — the assignment (plan §23.2, authoritative)")
    print("-" * w)
    print(f"  title : {day.title}")
    print(f"  IDs   : {', '.join(day.ids) if day.ids else '— (this day closes no ID)'}")
    for cid in day.ids:
        print(f"          {cid}  {concept_text(cid)}")
    print()
    print("  Close EXACTLY these IDs. No more, no fewer (§23.2).")
    print()

    print("-" * w)
    print("WHERE WE ACTUALLY ARE (docs/PROGRESS.md — last row)")
    print("-" * w)
    print(f"  {last_progress_row()}")
    print()
    print(f"  Day {n} is writable only if the last row is day {n - 1}.")
    print()

    print("-" * w)
    print(f"THE DAY BEFORE — day {n - 1}")
    print("-" * w)
    prev = part_list(n - 1)
    if prev:
        for line in prev:
            print(f"  {line}")
    else:
        print(f"  day {n - 1} is not written on disk")
    print()

    print("-" * w)
    print("LEDGER TAILS — what is already pinned, read, built and measured")
    print("-" * w)
    for name in ("PACKAGES.md", "SPECS.md", "TOPOLOGIES.md", "MEASUREMENTS.md"):
        print(f"  docs/{name}")
        for row in ledger_tail(name):
            print(f"    {row[:80]}")
        print()

    print("=" * w)
    print("Sources: scripts/plan_check.py (§23 day map) · docs/PROGRESS.md · docs/*.md")
    print("=" * w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
