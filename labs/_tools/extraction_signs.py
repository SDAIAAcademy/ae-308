"""Figures for the Day 4 slides on signs of model extraction, and for the practice question.

    cd labs && uv run python _tools/extraction_signs.py

Two synthetic days of the importer portal's chapter-suggestion log, other than the lab's
(data/service_log.jsonl, seed 310): the slides' day (seed 311) and the question's day (seed 312).
Nothing is written; the script prints the tables the slides and the question quote.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LABS))

import fanar as U  # noqa: E402
import prepare_data as P  # noqa: E402

SLIDE_PLAN = [("IMP-0128", 1, 31, "importer", ["84", "85"]), ("IMP-0264", 1, 14, "importer", ["61"]),
              ("IMP-0390", 1, 22, "importer", ["39", "69", "72"]), ("BRK-01", 1, 1420, "broker", None),
              ("BRK-03", 1, 610, "broker", None), ("IMP-0072", 1, 940, "copier", None)]
QUESTION_PLAN = [("BRK-03", 1, 1180, "broker", None), ("IMP-0208", 2, 560, "copier", None),
                 ("IMP-0145", 1, 36, "importer", ["09", "04"])]
PER_KEY_CAP = 1000


def signs(s: dict) -> list[str]:
    """The five signs of copying an account shows; three or more raise the alert."""
    found = []
    if s["near_dup"] >= 0.2:
        found.append("near-duplicates")
    if s["all_scores"] >= 0.5:
        found.append("every score asked")
    if s["outside_day"] >= 0.3:
        found.append("round the clock")
    if s["declared"] <= 0.05:
        found.append("no declarations follow")
    if s["chapters"] >= 10:
        found.append("every chapter")
    return found


def report(name: str, seed: int, plan: list) -> None:
    rows = P.service_log(random.Random(seed), plan)
    table = U.service_signs(rows)
    per_key = {}
    for r in rows:
        per_key[r["key"]] = per_key.get(r["key"], 0) + 1
    keys_over = sorted({r["account"] for r in rows if per_key[r["key"]] > PER_KEY_CAP})
    print(f"\n== {name} (seed {seed}): {len(rows)} requests")
    U.show([{**s, "signs": len(signs(s))} for s in table])
    print("busiest account by volume:", table[0]["account"])
    print(f"accounts with a key over {PER_KEY_CAP} a day:", keys_over or "none")
    print("accounts with three or more signs:", [s["account"] for s in table if len(signs(s)) >= 3])
    for s in table:
        print(f"  {s['account']}: {', '.join(signs(s)) or 'no sign'}")


if __name__ == "__main__":
    report("Slides, Day 4 session 4", P.SEED + 3, SLIDE_PLAN)
    report("Practice question", P.SEED + 4, QUESTION_PLAN)
