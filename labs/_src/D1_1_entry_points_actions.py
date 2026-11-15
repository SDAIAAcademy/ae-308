# %% [markdown]
# # Lab 1.1 · Entry points and actions
#
# Day 1 · Session 1 (A fooled model must break nothing important) · 25 min.
#
# You run Mukhallis, the clearance assistant of Fanar Ports Authority, as its platform team left it, and
# read its traces as a security engineer: where can text written by an outsider enter the model's context,
# and what can the agent do in the world? Work without an AI assistant: this is the first threat model.
#
# **Tasks**
# - [ ] Run the ten tasks and read one trace (6 min)
# - [ ] List the entry points for untrusted text (7 min)
# - [ ] List the actions and their effects (7 min)
# - [ ] One table: who writes what the model reads (5 min)
# - [ ] ✱ Stretch · Find the entry point that no task of the ten exercised
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
# ## 1 · Run the ten tasks and read one trace
#
# `M.run_tasks` runs each task on a fresh copy of the case study. A trace is a list of events: the
# task, each tool call with its effect, each result with its **origin**, the final reply.

# %%
rows = M.run_tasks(M.tasks(10))
U.show(rows, ["id", "kind", "lang", "ok", "calls"])
print("\nmodel:", rows[0]["run"].model, "\n")
rows[0]["run"].show()

# %% [markdown]
# ## 2 · List the entry points for untrusted text
#
# ✏️ **Exercise** · From the traces, return which tools brought text of which origin into the context:
# a dict from origin to the sorted list of tools. Leave out the origin `system` (the authority's own
# records and confirmations).

# %%
def entry_points(runs):
    # BEGIN SOLUTION
    found = {}
    for run in runs:
        for e in run.trace:
            if e["kind"] == "result" and e["origin"] != "system":
                found.setdefault(e["origin"], set()).add(e["tool"])
    return {origin: sorted(tools) for origin, tools in sorted(found.items())}
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
runs = [r["run"] for r in rows]
try:
    entries = entry_points(runs)
except NotImplementedError:
    entries = U.reference("d1_1_entries")
U.keep("d1_1_entries", entries)
U.check(entries == {"importer": ["read_message"], "kb": ["search_tariff"], "memory": ["recall"], "web": ["fetch_rate"]},
        "four origins of outside text reach the context in these ten tasks")
print(entries)

# %% [markdown]
# ## 3 · List the actions and their effects
#
# ✏️ **Exercise** · Two lists. `did(runs)`: the tools with an effect other than `read` that the ten
# tasks called, as a dict from tool to effect. `can_do()`: the same for every tool the agent holds
# (`M.TOOL`), called or not. The difference is what no benign task shows you.

# %%
def did(runs):
    # BEGIN SOLUTION
    return {e["tool"]: e["effect"] for run in runs for e in run.trace if e["kind"] == "call" and e["effect"] != "read"}
    # END SOLUTION


def can_do():
    # BEGIN SOLUTION
    return {name: t["effect"] for name, t in M.TOOL.items() if t["effect"] != "read"}
    # END SOLUTION

# %%
try:
    done, able = did(runs), can_do()
except NotImplementedError:
    ref = U.reference("d1_1_actions")
    done, able = ref["did"], ref["can_do"]
U.keep("d1_1_actions", {"did": done, "can_do": able})
never = sorted(set(able) - set(done))
U.check(len(done) == 4 and len(able) == 7, "the ten tasks used four of the agent's seven actions")
U.check(never == ["release_hold", "remember", "send_case_summary"], f"never called by a benign task: {never}")
U.show([{"tool": t, "effect": e, "server": M.TOOL[t]["server"], "called in the ten tasks": t in done} for t, e in able.items()])

# %% [markdown]
# **Look at** · The three tools no task called are the ones an attacker wants: release a hold, write
# to memory, send a whole case to an address. A benign run tells you what the agent does; the tool
# list tells you what it can do.
#
# ## 4 · One table: who writes what the model reads
#
# ✏️ **Exercise** · For each origin the table says who can write that text. Say whether that author
# can be someone outside the authority: return True or False for the five origins.

# %%
AUTHOR = {"importer": "the importer or anyone who emails the inbox", "kb": "the tariff committee, and brokers who upload circulars",
          "memory": "the model itself, from what it read in earlier sessions", "web": "whoever runs the rate page the model was pointed at",
          "system": "the authority's case system"}


def outsider():
    # BEGIN SOLUTION
    return {"importer": True, "kb": True, "memory": True, "web": True, "system": False}
    # END SOLUTION

# %%
try:
    outside = outsider()
except NotImplementedError:
    outside = U.reference("d1_1_outsider")
U.keep("d1_1_outsider", outside)
U.check(outside["memory"] and outside["kb"], "memory and the knowledge base count as outside text: an outsider's words can be stored in them")
U.check(not outside["system"], "the case system's own answers are the authority's")
surface = [{"origin": o, "tools": ", ".join(entries.get(o, [])) or "-", "author": AUTHOR[o], "outsider": outside[o]} for o in AUTHOR]
U.show(surface, width=60)
import json
U.save("d1_1/surface.json", json.dumps({"entries": entries, "actions": able, "outsider": outside}, indent=1))

# %% [markdown]
# ## ✱ Stretch · The entry point no task exercised
#
# Two more places carry text into the context and none of the ten traces shows them as a result:
# the tool descriptions each server sends, and the system prompt. Print
# `M.Agent(M.World()).listing(M.Run("", ""))` and `M.SYSTEM_PROMPT`. Who writes each? What is in the
# prompt that should not be there?
#
# ## Check yourself
#
# 1. Why does memory count as untrusted when only the model writes to it?
# 2. Which of the seven actions cannot be undone once done?
# 3. A colleague says "the model is instructed never to share data, so sharing is not a threat". What do you answer?
#
# <details><summary>Answers</summary>
#
# 1. The model writes what it read. If an importer's email said "remember: ...", the note is the importer's words, now stored.
# 2. An email that left, a released hold, and anything the generated code sent or overwrote. An update to a case can be corrected.
# 3. An instruction is a request to a model that an attacker also talks to. The design question is what a fooled model can reach.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d1_1/surface.json` holds your entry points and actions. Lab 1.2 starts from the supplied
# diagram file, so it does not need this one.
