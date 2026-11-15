# %% [markdown]
# # Lab 1.2 · The data-flow diagram
#
# Day 1 · Session 2 (Data flows and trust boundaries) · 25 min.
#
# You write the data-flow diagram of Mukhallis as data: nodes, flows and zones. Then code, not opinion,
# finds the flows that cross a trust boundary and every component where private data, untrusted content
# and an exit path meet. Work without an AI assistant.
#
# **Tasks**
# - [ ] Complete the flows of the diagram (8 min)
# - [ ] Mark private data, untrusted content and exit paths (7 min)
# - [ ] Find the crossings and where the three legs meet (6 min)
# - [ ] Draw it and read it (4 min)
# - [ ] ✱ Stretch · Add the approver as an entity and see which paths change
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
# ## 1 · Complete the flows of the diagram
#
# The supplied diagram has eleven nodes in four zones (`outside`, `authority`, `agent`, `servers`).
# Six flows are missing from it. Each one is a tool you saw in Lab 1.1.

# %%
dfd = U.json("dfd.json")
LEFT_OUT = {"F06", "F07", "F08", "F13", "F17"}
nodes = {n["id"]: n for n in dfd["nodes"]}
flows = [f for f in dfd["flows"] if f["id"] not in LEFT_OUT]
U.show(dfd["nodes"])
print()
U.show(flows)

# %% [markdown]
# ✏️ **Exercise** · Return the six missing flows as dicts with `from`, `to` and `data`: the tariff
# notes the planner reads, the memory it reads and the memory it writes, the rate request the comms
# server makes to an address the model chose, the images the case screen fetches when it renders a
# reply, and what the duty code can send as found (the code runner has the network: `code` to
# `ratesite`).

# %%
def missing_flows():
    # BEGIN SOLUTION
    return [
        {"from": "kb", "to": "planner", "data": "tariff notes (search_tariff)"},
        {"from": "memory", "to": "planner", "data": "notes (recall)"},
        {"from": "planner", "to": "memory", "data": "notes (remember)"},
        {"from": "comms", "to": "ratesite", "data": "request with an address the model chose"},
        {"from": "screen", "to": "ratesite", "data": "image requests of the rendered reply"},
        {"from": "code", "to": "ratesite", "data": "whatever generated code sends"},
    ]
    # END SOLUTION

# %%
# Check, with a safety net
try:
    added = missing_flows()
except NotImplementedError:
    added = U.reference("d1_2_missing")
U.keep("d1_2_missing", added)
pairs = {(f["from"], f["to"]) for f in added}
U.check(pairs == {("kb", "planner"), ("memory", "planner"), ("planner", "memory"), ("comms", "ratesite"), ("screen", "ratesite"), ("code", "ratesite")},
        "the six missing flows are in")
flows = flows + [dict(f, id=f"N{i}") for i, f in enumerate(added, 1)]

# %% [markdown]
# ## 2 · Mark private data, untrusted content and exit paths
#
# Mark sources, not every arrow: taint spreads along the flows by itself.
#
# ✏️ **Exercise** · Return the nodes where **private data** starts and the nodes where **untrusted
# content** starts (an outsider writes there). Then write `exits(flows)`: the flows that end in the
# zone `outside`.

# %%
def sources():
    # BEGIN SOLUTION
    return {"private": {"records"}, "untrusted": {"importer", "ratesite"}}
    # END SOLUTION


def exits(flows):
    # BEGIN SOLUTION
    return [f for f in flows if nodes[f["to"]]["zone"] == "outside"]
    # END SOLUTION

# %%
try:
    src = {k: sorted(v) for k, v in sources().items()}
    out_pairs = sorted([f["from"], f["to"]] for f in exits(flows))
except NotImplementedError:
    ref = U.reference("d1_2_marks")
    src, out_pairs = ref["sources"], ref["exits"]
U.keep("d1_2_marks", {"sources": src, "exits": out_pairs})
U.check(src == {"private": ["records"], "untrusted": ["importer", "ratesite"]}, "one private source, two untrusted sources")
U.check(len(out_pairs) == 4, f"four exit paths: {out_pairs}")

# %% [markdown]
# ## 3 · Find the crossings and where the three legs meet
#
# ✏️ **Exercise** · `crossings(flows)`: the flows whose two ends are in different zones.
# `reach(flows, start)`: every node that data starting in the set `start` can arrive at, following
# flows. A node is a **meeting point** when private data can arrive there, untrusted content can
# arrive there, and from there data can arrive outside.

# %%
def crossings(flows):
    # BEGIN SOLUTION
    return [f for f in flows if nodes[f["from"]]["zone"] != nodes[f["to"]]["zone"]]
    # END SOLUTION


def reach(flows, start):
    # BEGIN SOLUTION
    seen, todo = set(start), list(start)
    while todo:
        here = todo.pop()
        for f in flows:
            if f["from"] == here and f["to"] not in seen:
                seen.add(f["to"])
                todo.append(f["to"])
    return seen
    # END SOLUTION

# %%
try:
    cross = len(crossings(flows))
    inside = [f for f in flows if nodes[f["from"]]["zone"] != "outside"]  # private data that left is gone: do not follow it back in
    private, untrusted = reach(inside, set(src["private"])), reach(flows, set(src["untrusted"]))
    outside = {n for n in nodes if nodes[n]["zone"] == "outside"}
    meet = sorted(n for n in nodes if n in private and n in untrusted and n not in outside and reach(flows, {n}) & outside)
except NotImplementedError:
    ref = U.reference("d1_2_meet")
    cross, meet = ref["crossings"], ref["meet"]
U.keep("d1_2_meet", {"crossings": cross, "meet": meet})
print(f"{cross} of {len(flows)} flows cross a trust boundary")
print("meeting points:", meet)
U.check(cross == 13, "13 flows cross a trust boundary")
U.check(meet == ["case", "code", "comms", "memory", "planner", "screen"], "six components hold all three legs")

# %% [markdown]
# **Look at** · Six of the nine components inside the authority are meeting points. That is what a
# model in a loop does: whatever it reads can shape whatever it sends. The diagram's use is the list
# of four exits and the list of entry flows: each defence of Day 3 removes one leg at one of them.
#
# ## 4 · Draw it and read it
#
# The cell writes the diagram as Mermaid text, which renders in a README on a Git host and in most
# Markdown editors. Read it once from the importer to the exits and name the three legs aloud.

# %%
lines = ["flowchart LR"]
for zone in ("outside", "authority", "agent", "servers"):
    lines.append(f"  subgraph {zone}")
    lines += [f'    {n["id"]}["{n["label"]}"]' for n in dfd["nodes"] if n["zone"] == zone]
    lines.append("  end")
lines += [f'  {f["from"]} -->|{f["data"].split(" (")[0][:28]}| {f["to"]}' for f in flows]
path = U.save("d1_2/dfd.mmd", "\n".join(lines) + "\n")
print("\n".join(lines[:14]), "\n  ...\nsaved to", path.name)

# %% [markdown]
# ## ✱ Stretch · Add the approver
#
# Add a node `approver` in the zone `authority` and route `planner` to `comms` through it for email.
# Which meeting points and exits change? (None: an approval removes no leg. It adds a person at one
# exit. Day 4 asks what that person must see to decide.)
#
# ## Check yourself
#
# 1. Why is the importer's email marked untrusted when it arrives through the authority's own case server?
# 2. Which of the four exits would a rule "the agent may only talk to the case server" close?
# 3. The planner never reads the records store directly. Why is it still a meeting point?
#
# <details><summary>Answers</summary>
#
# 1. Trust follows the author, not the transport. The case server stores what the importer wrote.
# 2. The rate request, the code's requests and the image requests, if they pass the same gateway. Email to the importer stays: it is the purpose of the agent.
# 3. `get_importer` brings a record into its context through the case server: private data reaches it in two hops.
#
# </details>
#
# ## Carry forward
#
# The diagram text is in `artifacts/d1_2/dfd.mmd`. The capstone threat model starts from it.
