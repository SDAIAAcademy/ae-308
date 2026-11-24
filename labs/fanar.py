"""Shared helpers of the AE-308 labs (Fanar Ports Authority, synthetic data).

    import fanar as U

U.DATA, U.ART       labs/data and labs/artifacts (lab outputs, not committed)
U.QUICK             True when AE308_QUICK=1: fewer trials in the long runs
U.pick(a, b)        a normally, b in quick mode
U.jsonl(name), U.json(name)    a file of labs/data
U.reference(name)   the reference result of an exercise, for the safety-net cells
U.keep(name, obj)   returns obj; the trainer's tool also writes it as the reference result
U.check(ok, msg)    prints a tick, or raises AssertionError with the message
U.show(rows)        a list of dicts as a text table
U.wilson(k, n)      the 95% Wilson interval of k successes in n trials, as (low, high)
U.rate(k, n)        "3/10 = 30% [11%, 60%]"
U.band(level)       the national band of a level: low, medium, high, catastrophic
U.save(name, text)  write a lab output under labs/artifacts/
U.service_signs(rows)  per account of a service log: volume and the signs of copying (Lab 4.4)
"""

from __future__ import annotations

import json as _json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REF = DATA / "reference"
ART = HERE / "artifacts"
QUICK = os.environ.get("AE308_QUICK", "0") == "1"
LIKELIHOOD = {1: "rare", 2: "unlikely", 3: "likely", 4: "almost certain"}
IMPACT = {1: "low", 2: "medium", 3: "high", 4: "catastrophic"}


def pick(full, quick):
    return quick if QUICK else full


def jsonl(name: str) -> list[dict]:
    return [_json.loads(line) for line in (DATA / name).read_text(encoding="utf-8").splitlines() if line.strip()]


def json(name: str):
    return _json.loads((DATA / name).read_text(encoding="utf-8"))


def reference(name: str):
    """The reference result of exercise `name`, so later cells run when it is not done yet."""
    print(f"(safety net: using the reference result for {name})")
    return _json.loads((REF / f"{name}.json").read_text(encoding="utf-8"))


def keep(name: str, obj):
    if os.environ.get("AE308_WRITE_REF") == "1":
        REF.mkdir(parents=True, exist_ok=True)
        (REF / f"{name}.json").write_text(_json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return obj


def check(ok, message: str):
    if not ok:
        raise AssertionError("❌ " + message)
    print("✅ " + message)


def show(rows: list[dict], columns: list[str] | None = None, width: int = 44):
    if not rows:
        print("(no rows)")
        return
    columns = columns or list(rows[0])
    cells = [[str(r.get(c, ""))[:width] for c in columns] for r in rows]
    sizes = [max(len(c), *(len(row[i]) for row in cells)) for i, c in enumerate(columns)]
    print("  ".join(c.ljust(s) for c, s in zip(columns, sizes)))
    print("  ".join("-" * s for s in sizes))
    for row in cells:
        print("  ".join(v.ljust(s) for v, s in zip(row, sizes)))


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def rate(k: int, n: int) -> str:
    low, high = wilson(k, n)
    return f"{k}/{n} = {k / n:.0%} [{low:.0%}, {high:.0%}]"


def band(level: int) -> str:
    return "catastrophic" if level >= 16 else "high" if level >= 8 else "medium" if level >= 3 else "low"


def service_signs(rows: list[dict]) -> list[dict]:
    """One row per account of a service log: volume, keys, busiest hour and five shares.

    near_dup: requests that differ from the same key's previous request in exactly one word.
    outside_day: requests outside the working day (the log's minutes before 7 h or from 18 h).
    """
    acc, prev = {}, {}
    for r in sorted(rows, key=lambda r: (r["t"], r["key"])):
        a = acc.setdefault(r["account"], {"account": r["account"], "keys": set(), "requests": 0, "hours": {},
                                          "chapters": set(), "near": 0, "scores": 0, "outside": 0, "declared": 0})
        words, last = r["text"].split(), prev.get(r["key"])
        a["near"] += bool(last and len(last) == len(words) and sum(x != y for x, y in zip(last, words)) == 1)
        prev[r["key"]] = words
        a["keys"].add(r["key"])
        a["requests"] += 1
        a["hours"][r["t"] // 60] = a["hours"].get(r["t"] // 60, 0) + 1
        a["chapters"].add(r["chapter"])
        a["scores"] += r["all_scores"]
        a["outside"] += not (420 <= r["t"] < 1080)
        a["declared"] += r["declared"]
    out = []
    for a in acc.values():
        n = a["requests"]
        out.append({"account": a["account"], "keys": len(a["keys"]), "requests": n, "busiest_hour": max(a["hours"].values()),
                    "chapters": len(a["chapters"]), "near_dup": round(a["near"] / n, 2), "all_scores": round(a["scores"] / n, 2),
                    "outside_day": round(a["outside"] / n, 2), "declared": round(a["declared"] / n, 2)})
    return sorted(out, key=lambda s: -s["requests"])


def save(name: str, text: str) -> Path:
    path = ART / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path
