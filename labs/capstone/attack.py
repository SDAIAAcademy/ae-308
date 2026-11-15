"""Runs a file of attacks against a team's build and prints a rate with its interval per technique.

    uv run python capstone/attack.py --build capstone/build.py --attacks data/attacks.jsonl --trials 10
    uv run python capstone/attack.py --build <their build.py> --attacks my_attacks.jsonl --log attack_log.jsonl

The build file must define controls(), which returns a fresh controls dict for M.Agent. Every trial is
appended to the log as one JSON line. Synthetic data only: nothing here touches a real network.
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fanar as U  # noqa: E402
import mukhallis as M  # noqa: E402


def load_build(path: str):
    spec = importlib.util.spec_from_file_location("team_build", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.controls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--log", default="")
    args = parser.parse_args()
    controls = load_build(args.build)
    attacks = [json.loads(line) for line in Path(args.attacks).read_text(encoding="utf-8").splitlines() if line.strip()]
    wins, runs, calls, rows = collections.Counter(), collections.Counter(), 0, []
    for attack in attacks:
        for trial in range(args.trials):
            run, world = M.run_attack(attack, controls=controls(), trial=trial)
            ok = M.judge(attack, run, world)
            key = (attack["technique"], attack["goal"], attack["lang"])
            wins[key] += ok
            runs[key] += 1
            calls += run.calls
            rows.append({"attack": attack["id"], "technique": attack["technique"], "channel": attack["channel"], "goal": attack["goal"],
                         "lang": attack["lang"], "trial": trial, "success": ok, "calls": run.calls, "model": run.model})
    U.show([{"technique": k[0], "goal": k[1], "lang": k[2], "success": U.rate(wins[k], runs[k])} for k in sorted(runs)])
    print(f"{len(rows)} trials, {calls} model calls, {sum(r['success'] for r in rows)} successes")
    if args.log:
        with Path(args.log).open("a", encoding="utf-8", newline="\n") as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
