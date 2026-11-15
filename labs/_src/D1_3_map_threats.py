# %% [markdown]
# # Lab 1.3 · Ten threats, mapped
#
# Day 1 · Session 3 (Risk lists and technique catalogues) · 25 min.
#
# You state ten threats to Mukhallis in one form and map each to a risk entry (what goes wrong) and an
# adversary technique (how it is done). A linter checks every id against the catalogue file, so a mapping
# cannot cite an entry that does not exist. Work without an AI assistant.
#
# **Tasks**
# - [ ] Read the catalogue file: two lists and the techniques (4 min)
# - [ ] Write threats in the form source, entry, action, harm (6 min)
# - [ ] Map ten threats to risk entries and techniques (10 min)
# - [ ] Lint the mapping and settle two disputes (5 min)
# - [ ] ✱ Stretch · Write threats 11 and 12 for the threat model of the outcome
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
# ## 1 · Read the catalogue file: two lists and the techniques
#
# `data/catalogue.json` holds the ids and names the course uses: the OWASP Top 10 for LLM Applications
# 2026, the OWASP Top 10 for Agentic Applications for 2026, and fifteen techniques of MITRE ATLAS 5.6.
# Editions change: the file carries the names as published when the course was written.

# %%
cat = U.json("catalogue.json")
RISKS = {**cat["owasp_llm_2026"], **cat["owasp_agentic_2026"]}
TECHNIQUES = cat["mitre_atlas_5_6"]
for group in ("owasp_llm_2026", "owasp_agentic_2026", "mitre_atlas_5_6"):
    print(group)
    for key, name in cat[group].items():
        print(f"  {key:<14} {name}")

# %% [markdown]
# ## 2 · Write threats in the form source, entry, action, harm
#
# A threat you can test names four things: who writes the text (**source**), where it enters
# (**entry**), which tool or output it turns (**action**) and what is lost (**harm**).
#
# ✏️ **Exercise** · Write `statement(t)`: one sentence from the four fields, in this shape:
# "TH-01: an importer plants text in the body of an email so that send_email does this: another
# importer's record is emailed to an outside address."

# %%
threats = U.json("threats.json")
U.show(threats, ["id", "source", "entry", "action"], width=48)


def statement(t):
    # BEGIN SOLUTION
    return f"{t['id']}: {t['source']} plants text in {t['entry']} so that {t['action']} does this: {t['harm']}."
    # END SOLUTION

# %%
# Check, with a safety net
try:
    sentences = [statement(t) for t in threats]
except NotImplementedError:
    sentences = U.reference("d1_3_statements")
U.keep("d1_3_statements", sentences)
U.check(all(t["source"] in s and t["entry"] in s and t["action"] in s and t["harm"] in s for t, s in zip(threats, sentences)),
        "every statement names its source, entry, action and harm")
print("\n".join(sentences))

# %% [markdown]
# ## 3 · Map ten threats to risk entries and techniques
#
# ✏️ **Exercise** · Return a dict from threat id to a pair: one risk id (`LLM..` or `ASI..`) and one
# ATLAS technique id. Choose the entry that names the harm's cause and the technique that names the
# adversary's move. TH-01 is done.

# %%
def mapping():
    done = {"TH-01": ("LLM01", "AML.T0051.001")}
    # BEGIN SOLUTION
    done.update({
        "TH-02": ("LLM10", "AML.T0077"), "TH-03": ("LLM02", "AML.T0086"), "TH-04": ("LLM03", "AML.T0053"),
        "TH-05": ("ASI06", "AML.T0080.000"), "TH-06": ("LLM05", "AML.T0070"), "TH-07": ("LLM04", "AML.T0109"),
        "TH-08": ("ASI05", "AML.T0053"), "TH-09": ("ASI03", "AML.T0055"), "TH-10": ("LLM08", "AML.T0056"),
    })
    return done
    # END SOLUTION

# %% [markdown]
# ## 4 · Lint the mapping and settle two disputes
#
# The linter refuses an id that is not in the catalogue, then compares with the key. The key accepts
# more than one answer where two entries are defensible, and says so.

# %%
def lint(mapped):
    problems = []
    for th, (risk, tech) in mapped.items():
        if risk not in RISKS:
            problems.append(f"{th}: {risk} is not a risk entry of the catalogue")
        if tech not in TECHNIQUES:
            problems.append(f"{th}: {tech} is not a technique of the catalogue")
    return problems


key = U.json("reference/threat_key.json")
try:
    mapped = {k: list(v) for k, v in mapping().items()}
except NotImplementedError:
    mapped = U.reference("d1_3_mapping")
U.keep("d1_3_mapping", mapped)
U.check(lint({"TH-01": ("LLM11", "AML.T9999")}) != [], "the linter refuses ids that do not exist")
U.check(len(mapped) == 10 and lint(mapped) == [], "ten threats mapped, every id in the catalogue")
rows, agree = [], 0
for t in threats:
    risk, tech = mapped[t["id"]]
    ok = risk in key[t["id"]]["owasp"] and tech in key[t["id"]]["atlas"]
    agree += ok
    rows.append({"id": t["id"], "risk": f"{risk} {RISKS[risk]}", "technique": f"{tech} {TECHNIQUES[tech]}",
                 "key accepts": "yes" if ok else "also: " + ", ".join(key[t["id"]]["owasp"] + key[t["id"]]["atlas"])})
U.show(rows, width=52)
U.check(agree >= 8, f"{agree} of 10 mappings are among the answers the key accepts")

# %% [markdown]
# **Two disputes to settle in your team, in one sentence each.**
#
# - **TH-07**, the tool description that changes after approval. Supply chain (LLM04, ASI04) or prompt
#   injection (LLM01)? The text is an injection; the cause is that a supplier's component changed
#   under you. The key takes the cause, because the control follows from it: pin what you approved.
# - **TH-09**, the shared key. Excessive agency (LLM03) or identity and privilege abuse (ASI03)? No
#   model is fooled in TH-09: a server acts with authority nobody delegated to it. The key takes ASI03.
#
# A mapping is an argument, not a lookup. Write the reason beside the id in your threat model.
#
# ## ✱ Stretch · Threats 11 and 12
#
# The outcome asks for at least twelve. Write two more in the same form, for example the rate page
# as an entry point, or the cost of an agent made to loop (LLM06, AML.T0034), map them and lint them.
#
# ## Check yourself
#
# 1. What does an ATLAS technique add to an OWASP entry?
# 2. TH-04 and TH-08 map to the same technique. What differs?
# 3. Why does the catalogue file carry a note about editions?
#
# <details><summary>Answers</summary>
#
# 1. The entry names the weakness in your application; the technique names the adversary's step, which is what you reproduce in a test.
# 2. The entry point and the action: an email that turns a case tool, against generated code that reads and overwrites files. One technique, two tests, two controls.
# 3. The lists are revised and entries are renamed and reordered. A threat model cites the edition it used.
#
# </details>
#
# ## Carry forward
#
# Your mapping feeds Lab 1.4, which loads the key's mapping if yours is missing.
