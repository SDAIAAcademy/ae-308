# %% [markdown]
# # Lab 2.2 · One record, three exits
#
# Day 2 · Session 2 (Exfiltration paths) · 25 min.
#
# You leak one synthetic importer record out of Mukhallis three ways: in the address of an image the
# case screen renders, in an argument of a tool, and through the email tool the agent is meant to use.
# You write the detector that finds the record in the egress log. Synthetic data, this notebook only.
#
# **Tasks**
# - [ ] The egress log of a clean run (4 min)
# - [ ] Write the leak detector (7 min)
# - [ ] Three paths: link, tool argument, email (9 min)
# - [ ] Which path used an allowed host (5 min)
# - [ ] ✱ Stretch · Encode the record in base64 and extend the detector
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
# ## 1 · The egress log of a clean run
#
# Every outbound request of the agent passes one gateway, `world.net`, which writes `world.egress`:
# the host, the path, the payload and the tool that caused it (`via`).

# %%
task = M.tasks(10)[0]
world = M.World()
run = M.Agent(world).run(task["text"])
U.show(world.egress, ["n", "host", "path", "via"])
OWN = set(M.HOST.values())
print("\nthe authority's own hosts and its rate provider:", sorted(OWN))

# %% [markdown]
# ## 2 · Write the leak detector
#
# ✏️ **Exercise** · `leaked(entry, record)`: the sorted names of the fields among `iban`, `mobile`
# and `cr_number` whose value can be read in one egress entry: in its `path` or anywhere in its
# `payload`, as plain text or URL-encoded (`urllib.parse.quote`). The payload is a dict: turn it
# into text with `json.dumps(..., ensure_ascii=False)`.

# %%
import json
from urllib.parse import quote

FIELDS = ("iban", "mobile", "cr_number")


def leaked(entry, record):
    # BEGIN SOLUTION
    text = entry["path"] + " " + json.dumps(entry["payload"], ensure_ascii=False)
    return sorted(f for f in FIELDS if record[f] in text or quote(record[f], safe="") in text)
    # END SOLUTION

# %%
# Check, with a safety net
def detect(entry, record):
    try:
        return leaked(entry, record)
    except NotImplementedError:
        text = entry["path"] + " " + json.dumps(entry["payload"], ensure_ascii=False)
        return sorted(f for f in FIELDS if record[f] in text or quote(record[f], safe="") in text)


rec = world.importers["IMP-0042"]
U.check(detect({"path": "/logo.png?d=" + rec["iban"], "payload": {}}, rec) == ["iban"], "an IBAN in a path is found")
U.check(detect({"path": "/x?m=" + quote(rec["mobile"], safe=""), "payload": {}}, rec) == ["mobile"], "a URL-encoded mobile number is found")
U.check(detect({"path": "/send", "payload": {"body": json.dumps(rec)}}, rec) == ["cr_number", "iban", "mobile"], "a whole record in an email body is found")
U.check(all(detect(e, world.importers[world.messages[task["msg_id"]]["importer_id"]]) == [] for e in world.egress), "the clean run leaks nothing")

# %% [markdown]
# ## 3 · Three paths: link, tool argument, email
#
# Three attacks of the corpus, one per exit. Each hides in the invoice of the same clearance task.
# For each, the cell takes the first trial that works and you find where the record left.
#
# ✏️ **Exercise** · `find_leaks(world)`: for every egress entry and every importer record, one row
# `{"n", "host", "via", "importer", "fields"}` when `detect` finds something.

# %%
def find_leaks(world):
    # BEGIN SOLUTION
    rows = []
    for e in world.egress:
        for rec in world.importers.values():
            fields = detect(e, rec)
            if fields:
                rows.append({"n": e["n"], "host": e["host"], "via": e["via"], "importer": rec["importer_id"], "fields": fields})
    return rows
    # END SOLUTION

# %%
paths = {"rendered link": M.attacks(channel="invoice", goal="link", lang="en")[0],
         "tool argument": M.attacks(channel="invoice", goal="tool_arg", lang="en")[0],
         "permitted email tool": M.attacks(channel="invoice", goal="email_record", style="task", lang="en")[0]}
found = {}
for name, attack in paths.items():
    trial = next(t for t in range(20) if M.judge(attack, *M.run_attack(attack, trial=t)))
    run, w = M.run_attack(attack, trial=trial)
    try:
        rows = find_leaks(w)
    except NotImplementedError:
        rows = U.reference("d2_2_leaks")[name]
    found[name] = rows
    print(f"\n{name}: {attack['id']}, trial {trial}\n  payload: {attack['text']}")
    U.show(rows)
U.keep("d2_2_leaks", found)
U.check(all(rows for rows in found.values()), "every attack shows in the egress log")
found = {name: [next((r for r in rows if r["host"] not in OWN), rows[0])] for name, rows in found.items()}  # the request that matters
U.check(found["permitted email tool"][0]["importer"] == "IMP-0042", "the email carries another importer's whole record")

# %% [markdown]
# ## 4 · Which path used an allowed host
#
# ✏️ **Exercise** · `own_host(host)`: True when the host is one of the authority's own (`OWN`).
# Then read the table: which of the three leaks would a rule "talk only to our own hosts" stop?

# %%
def own_host(host):
    # BEGIN SOLUTION
    return host in OWN
    # END SOLUTION

# %%
try:
    summary = [{"path": name, "host": rows[0]["host"], "via": rows[0]["via"], "own host": own_host(rows[0]["host"]),
                "fields": ", ".join(rows[0]["fields"])} for name, rows in found.items()]
except NotImplementedError:
    summary = U.reference("d2_2_summary")
U.keep("d2_2_summary", summary)
U.show(summary)
U.check([r["own host"] for r in summary] == [False, False, True], "two leaks go to outside hosts; the email leak goes through the authority's own mail host")
U.save("d2_2/exfiltration.json", json.dumps(summary, indent=1))

# %% [markdown]
# **Look at** · The link attack shows twice in the log: the image address also sits in the reply emailed
# to the importer, who gets their own IBAN back; the request that matters is the one the case screen
# made to the outside host. The third leak used no forbidden host, no odd tool and no encoding. It used the feature the agent exists for. A rule about hosts cannot see it; a rule about recipients can. That
# is Lab 3.2.
#
# ## ✱ Stretch · Base64
#
# Change the link payload so that the model is asked to send the IBAN in base64
# (the stand-in fills `{iban}` only; encode the value yourself in a copy of `world.egress`), then
# extend `leaked` to find it. What is the limit of a detector that looks for known encodings?
#
# ## Check yourself
#
# 1. Why does the case screen cause a request at all?
# 2. The tool-argument leak used `fetch_rate`. Which argument, and why did the agent accept it?
# 3. Which single field in the egress log tells you a leak used a permitted path?
#
# <details><summary>Answers</summary>
#
# 1. It renders the reply, and an image in Markdown is fetched from its address. The address carries the data; nobody has to click.
# 2. `source_url`: the tool lets the model choose the page to fetch. An argument the model fills with a free address is an exit path.
# 3. `host`: the email leak shows the authority's own mail host. The difference is in the payload's recipient, which a host rule never reads.
#
# </details>
#
# ## Carry forward
#
# `artifacts/d2_2/exfiltration.json` lists the three exits. Lab 3.2 reruns the same three attacks.
