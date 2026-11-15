# %% [markdown]
# # Lab 1.4 · Score and choose five
#
# Day 1 · Session 4 (Scoring and choosing what to test) · 25 min.
#
# You score the ten threats on the national likelihood and impact scale, rank them, see what ten
# trials can and cannot show, and spend a fixed budget of 300 model calls on five threats. Work without
# an AI assistant.
#
# **Tasks**
# - [ ] Score likelihood and impact with a reason each (8 min)
# - [ ] Level and band, then rank (4 min)
# - [ ] What ten trials can and cannot show (6 min)
# - [ ] Pick five within 300 calls (7 min)
# - [ ] ✱ Stretch · Rescore one threat as if email were removed from the agent
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
# ## 1 · Score likelihood and impact with a reason each
#
# The National AI Risk Management Framework scores likelihood from 1 to 4 (rare, unlikely, likely,
# almost certain) and impact from 1 to 4 (low, medium, high, catastrophic). Before any test, the
# likelihood is a judgement: how many people can reach the entry point, and how much skill it takes.
# After Day 2 it will be a measured rate.
#
# ✏️ **Exercise** · Return a dict from threat id to `(likelihood, impact, reason)`. Three are done.
# The records are classified Restricted; a released hold lets uninspected goods leave the port.

# %%
threats = U.json("threats.json")
U.show(threats, ["id", "entry", "action", "harm"], width=50)


def scores():
    done = {
        "TH-01": (4, 3, "anyone can email the inbox; one Restricted record leaves"),
        "TH-04": (2, 4, "needs a shipment under hold and the right wording; uninspected goods leave the port"),
        "TH-10": (3, 2, "any importer can type in the portal chat; the prompt and a key are shown to one person"),
    }
    # BEGIN SOLUTION
    done.update({
        "TH-02": (3, 3, "anyone can send an invoice; needs the reply to be rendered; one IBAN leaves"),
        "TH-03": (3, 3, "anyone can send an invoice; needs a foreign-currency case; one IBAN leaves"),
        "TH-05": (3, 3, "one email is enough and it persists; every later reply of that importer is redirected"),
        "TH-06": (2, 3, "needs a broker's upload right; replies of many importers are redirected"),
        "TH-07": (2, 4, "needs control of a server; then records leak on every task"),
        "TH-08": (2, 4, "needs the model to write hostile code; the importer file is read, the tariff table overwritten"),
        "TH-09": (3, 3, "anyone who reaches the comms server; any case goes to any address"),
    })
    return done
    # END SOLUTION

# %%
# Check, with a safety net
key = U.json("reference/threat_key.json")
try:
    scored = {k: list(v) for k, v in scores().items()}
except NotImplementedError:
    scored = U.reference("d1_4_scores")
U.keep("d1_4_scores", scored)
U.check(len(scored) == 10 and all(1 <= v[0] <= 4 and 1 <= v[1] <= 4 and len(v[2]) >= 15 for v in scored.values()),
        "ten threats scored from 1 to 4, each with a reason")
far = [k for k, v in scored.items() if abs(v[0] - key[k]["likelihood"]) > 1 or abs(v[1] - key[k]["impact"]) > 1]
U.check(not far, f"no score is more than one step from the trainer's key {far}")

# %% [markdown]
# ## 2 · Level and band, then rank
#
# ✏️ **Exercise** · `level(likelihood, impact)` is the product. The bands are the framework's: 1 to 2
# low, 3 to 6 medium, 8 to 12 high, 16 catastrophic (`U.band`). Return the register sorted by level,
# highest first, ties by id.

# %%
def register(scored):
    # BEGIN SOLUTION
    rows = [{"id": k, "likelihood": v[0], "impact": v[1], "level": v[0] * v[1], "band": U.band(v[0] * v[1]), "reason": v[2]}
            for k, v in scored.items()]
    return sorted(rows, key=lambda r: (-r["level"], r["id"]))
    # END SOLUTION

# %%
try:
    reg = register(scored)
except NotImplementedError:
    reg = U.reference("d1_4_register")
U.keep("d1_4_register", reg)
U.show(reg, ["id", "likelihood", "impact", "level", "band", "reason"], width=70)
U.check(reg[0]["id"] == "TH-01" and reg[0]["level"] == 12, "TH-01 leads the register at level 12, high")
U.check(all(r["band"] == U.band(r["level"]) for r in reg), "every band follows from its level")

# %% [markdown]
# ## 3 · What ten trials can and cannot show
#
# An attack on a language model works some of the time. Ten trials give a rate and a wide interval.
# The cell prints the 95% Wilson interval for every count out of ten, then runs one attack of the
# starter corpus ten times and a hundred times.

# %%
for k in (0, 1, 3, 5, 8, 10):
    print(U.rate(k, 10))

attack = M.attacks(channel="email", goal="email_record", style="authority", lang="en")[0]
n_long = U.pick(100, 30)
hits = [M.judge(attack, *M.run_attack(attack, trial=t)) for t in range(n_long)]
print(f"\n{attack['id']} ({attack['channel']}, {attack['style']}, {attack['lang']}) on {M.default_model().name}")
print("first ten trials:", U.rate(sum(hits[:10]), 10))
print(f"{n_long} trials:      ", U.rate(sum(hits), n_long))

# %% [markdown]
# ✏️ **Exercise** · Two rates differ for sure only when their intervals do not overlap. Write
# `separate(k1, n1, k2, n2)` with `U.wilson`. Then answer in the check: can ten trials tell 3 in 10
# from 6 in 10? Can they tell 0 in 10 from 6 in 10?

# %%
def separate(k1, n1, k2, n2):
    # BEGIN SOLUTION
    a, b = U.wilson(k1, n1), U.wilson(k2, n2)
    return a[1] < b[0] or b[1] < a[0]
    # END SOLUTION

# %%
try:
    answers = [separate(3, 10, 6, 10), separate(0, 10, 6, 10), separate(30, 100, 60, 100)]
except NotImplementedError:
    answers = U.reference("d1_4_separate")
U.keep("d1_4_separate", answers)
U.check(answers == [False, True, True], "ten trials cannot tell 30% from 60%; they can tell 0 in 10 from 6 in 10; a hundred trials can tell 30% from 60%")

# %% [markdown]
# **Look at** · Ten trials answer "does it work at all, and roughly how often". They do not rank two
# attacks that both work. Zero successes in ten still leaves up to 28% in the interval: a defence is
# claimed over more trials, or shown by a deterministic control that needs no trials at all.
#
# ## 4 · Pick five within 300 calls
#
# The budget is 300 model calls. `COST` is the number of calls one trial of each threat takes on the
# cheapest task that meets its entry point, measured on the build as found. TH-08 and TH-09 cost no
# model call: generated code and a server's key are tested directly, without the model.
#
# ✏️ **Exercise** · Return a dict from threat id to the number of trials, for exactly five threats.
# Rules: every chosen threat is at level 8 or more, each gets at least ten trials, TH-01 is in, and
# the total stays within the budget.

# %%
COST = {"TH-01": 11, "TH-02": 9, "TH-03": 9, "TH-04": 10, "TH-05": 16, "TH-06": 6, "TH-07": 9, "TH-08": 0, "TH-09": 0, "TH-10": 1}
BUDGET = 300


def plan():
    # BEGIN SOLUTION
    return {"TH-01": 10, "TH-02": 10, "TH-04": 10, "TH-08": 10, "TH-09": 10}
    # END SOLUTION

# %%
try:
    chosen = plan()
except NotImplementedError:
    chosen = U.reference("d1_4_plan")
U.keep("d1_4_plan", chosen)
levels = {r["id"]: r["level"] for r in reg}
spent = sum(COST[k] * n for k, n in chosen.items())
U.show([{"id": k, "level": levels[k], "trials": n, "calls": COST[k] * n} for k, n in chosen.items()])
print(f"calls: {spent} of {BUDGET}")
U.check(len(chosen) == 5 and "TH-01" in chosen, "five threats, TH-01 among them")
U.check(all(levels[k] >= 8 for k in chosen) and all(n >= 10 for n in chosen.values()), "every chosen threat is high and gets ten trials or more")
U.check(spent <= BUDGET, "the plan fits the budget")
left = [r["id"] for r in reg if r["level"] >= 8 and r["id"] not in chosen]
print("high threats left untested, to state as such in the threat model:", left)

# %% [markdown]
# **Look at** · The budget forces a statement most threat models leave out: which high threats were
# not tested. The two that cost no model call are also the two a deterministic control will close.
#
# ## ✱ Stretch · Remove one leg and rescore
#
# Suppose the agent could not send email at all (an officer sends the replies). Rescore the ten
# threats. Which fall to low, and which do not move?
#
# ## Check yourself
#
# 1. Why is TH-04 scored unlikely and still high?
# 2. You measure 0 successes in 10 trials after adding a defence. What may you claim?
# 3. Why is the likelihood of TH-09 not a rate at all?
#
# <details><summary>Answers</summary>
#
# 1. Level is likelihood times impact: 2 times 4 is 8. A rare event with a catastrophic or near-catastrophic harm stays on the list.
# 2. That the rate is probably below about 28%, on this model and this wording. Not that the attack is closed.
# 3. No model is involved. With the shared key the call succeeds every time; with a correct token check it fails every time.
#
# </details>
#
# ## Carry forward
#
# The register and the plan are the first half of the capstone threat model. Day 2 replaces the
# judged likelihoods with measured rates.
