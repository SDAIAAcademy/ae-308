# %% [markdown]
# # Lab 2.4 · A changed tool, then pins
#
# Day 2 · Session 4 (Hostile tools) · 25 min.
#
# You approve the tools of the two protocol servers, then one server changes what it says about a tool.
# You watch the agent obey the new description, then pin approved descriptions by hash so that a changed
# tool is refused before the model reads it. Synthetic data, this notebook only.
#
# **Tasks**
# - [ ] List and approve the tools of both servers (4 min)
# - [ ] The server changes one description: ten trials (7 min)
# - [ ] Write the manifest of hashes (6 min)
# - [ ] Verify on every listing, rerun, read the refusal (8 min)
# - [ ] ✱ Stretch · Pin the argument schema as well and change a default
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
# ## 1 · List and approve the tools of both servers
#
# At the start of every run the agent asks each server for its tools (`tools/list`) and puts the
# names, descriptions and argument schemas into the model's context. A description is text the
# model reads before any task text.

# %%
world = M.World()
approved = M.Agent(world).listing(M.Run("", ""))
U.show([{"tool": t["name"], "server": M.TOOL[t["name"]]["server"], "description": t["description"]} for t in approved], width=90)

# %% [markdown]
# ## 2 · The server changes one description: ten trials
#
# The operator of the comms server, or someone who took it over, appends one sentence to the
# description of `fetch_rate`. The name and the schema do not change, so nothing looks different in
# a tool picker.

# %%
attack = M.attacks(channel="tool", goal="tool_arg")[0]
changed = M.World()
M.plant(changed, attack)
new = next(t for t in M.Agent(changed).listing(M.Run("", "")) if t["name"] == "fetch_rate")
print("approved:", next(t["description"] for t in approved if t["name"] == "fetch_rate"))
print("now:     ", new["description"])

hits = [M.judge(attack, *M.run_attack(attack, trial=t)) for t in range(10)]
print("\nthe importer's IBAN leaves in a tool argument:", U.rate(sum(hits), 10), "on task", attack["task"])
U.keep("d2_4_before", sum(hits))
U.check(sum(hits) >= 6, "the changed description is obeyed in most trials")

# %% [markdown]
# **Look at** · No email, no invoice and no note is hostile here. Every task that needs an exchange
# rate leaks, for every importer. The stand-in obeys a tool description more often than any other
# text, and so do real models: a description reads as the developer's voice.
#
# ## 3 · Write the manifest of hashes
#
# ✏️ **Exercise** · `manifest(listing)`: a dict from tool name to the SHA-256 hex digest of its
# description (UTF-8). This is what you store when a person approves the tools.

# %%
import hashlib


def manifest(listing):
    # BEGIN SOLUTION
    return {t["name"]: hashlib.sha256(t["description"].encode("utf-8")).hexdigest() for t in listing}
    # END SOLUTION

# %%
# Check, with a safety net
try:
    pinned = manifest(approved)
except NotImplementedError:
    pinned = U.reference("d2_4_pins")
U.keep("d2_4_pins", pinned)
U.check(len(pinned) == 12 and all(len(h) == 64 for h in pinned.values()), "twelve tools pinned")
U.check(pinned["fetch_rate"] == hashlib.sha256(M.TOOL["fetch_rate"]["description"].encode()).hexdigest(), "the pin of fetch_rate is the hash of the approved text")

# %% [markdown]
# ## 4 · Verify on every listing, rerun, read the refusal
#
# ✏️ **Exercise** · `verify(listing, pinned)`: the names of the tools to refuse: every tool whose
# description no longer hashes to its pin, and every tool that has no pin at all (a new tool is not
# an approved tool).

# %%
def verify(listing, pinned):
    # BEGIN SOLUTION
    return [t["name"] for t in listing
            if pinned.get(t["name"]) != hashlib.sha256(t["description"].encode("utf-8")).hexdigest()]
    # END SOLUTION

# %%
def refused(listing):
    try:
        return verify(listing, pinned)
    except NotImplementedError:
        return [t["name"] for t in listing if pinned.get(t["name"]) != hashlib.sha256(t["description"].encode("utf-8")).hexdigest()]


controls = {"verify_tools": refused}
U.check(refused(approved) == [], "nothing is refused while the servers say what was approved")
U.check(refused(approved + [{"name": "export_all", "description": "Export every record."}]) == ["export_all"], "a tool without a pin is refused")
after = [M.run_attack(attack, controls=controls, trial=t) for t in range(10)]
k = sum(M.judge(attack, r, w) for r, w in after)
print("with pins:", U.rate(k, 10))
run, w = after[0]
run.show(100)
U.keep("d2_4_after", k)
U.check(k == 0 and run.refused == ["fetch_rate"], "the changed tool is refused in every trial and the leak is gone")

# %% [markdown]
# **Look at** · Read the trace. The agent lost `fetch_rate`, so this foreign-currency clearance could
# not be computed: the reply says an officer will follow up, and no duty was guessed. Pinning trades
# a leak for a stopped task until a person approves the new text. Count that cost:

# %%
rows = M.run_tasks(controls=controls)
print("benign tasks with pins, servers unchanged:", f"{M.pass_rate(rows):.0%}")
def with_change():
    out = []
    for t in M.tasks():
        w2 = M.World()
        M.plant(w2, attack)
        r2 = M.Agent(w2, controls=controls).run(t["text"])
        out.append(M.grade(t, r2, w2))
    return out
blocked = with_change()
print("benign tasks with pins, after the server's change:", f"{sum(blocked) / len(blocked):.0%}", "(the rest wait for re-approval)")
U.keep("d2_4_cost", {"unchanged": M.pass_rate(rows), "changed": sum(blocked) / len(blocked)})
U.check(M.pass_rate(rows) == 1.0, "pins cost nothing while nothing changes")

# %% [markdown]
# ## ✱ Stretch · Pin the schema too
#
# A server can leave the description alone and change the argument schema: a new optional argument,
# a default that points elsewhere. Hash the description together with
# `json.dumps(t["inputSchema"], sort_keys=True)` and show that a changed default is refused.
#
# ## Check yourself
#
# 1. What does a pin not protect against?
# 2. Why refuse a tool with no pin, when its description may be harmless?
# 3. Where must the manifest be stored?
#
# <details><summary>Answers</summary>
#
# 1. A server whose description stays the same and whose behaviour changes, and hostile text in what a tool returns. A pin covers what the model reads at listing time, nothing else.
# 2. Approval is the control. A tool that appears after approval was approved by nobody, whatever it says.
# 3. Outside the reach of the agent and of the servers: in the repository or the gateway's configuration, changed by review.
#
# </details>
#
# ## Carry forward
#
# The pins are saved as the reference `d2_4_pins`; the hardened build of Day 4 loads them.
