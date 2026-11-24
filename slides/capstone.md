---
course: "Securing Language Model and Agent Applications"
code: "AE-308"
version: "2027.2.0"
deck: "capstone"
day: 5
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-308/slides/capstone.html"
---

# Securing Language Model and Agent Applications

## Capstone: Capstone: red-team day and live defence

Attack another team's hardened agent, harden your own, defend the residual risk

#### [capstone#title] Capstone: red-team day and live defence

*SDAIA Academy · Securing Language Model and Agent Applications*

Capstone: Attack another team's hardened agent, harden your own, defend the residual risk

AI Engineering Track · 4 teaching days + capstone day · 10 min talk and demo · 5 min Q&A · AE-308

#### [capstone#agenda] How the red-team day runs

*Capstone*

- **Rules**: teams exchange repositories and state their rules of engagement
- **Attack**: a timed attack on the other team's hardened agent, every trial logged
- **Report**: findings handed over: risk entry, rate and interval, one trace, a proposed test
- **Harden**: each confirmed finding becomes a test that fails, then a fix that makes it pass
- **Defend**: the residual-risk statement, with one attack reproduced live

#### [capstone#rules] Attack the assigned build, on the synthetic data, within the budget

*Rules of engagement*

- **In scope.** The other team's `build.py`, through the task channel, the inbox, the tariff notes, importer memory and the two servers' tool listings.
- **Out of scope.** The other team's laptops, accounts and repository settings. Any real address, host or model account. Any payload that leaves the lab.
- **Stop when.** The time box ends, the budget of 600 model calls is spent, or anything outside the synthetic data is reached: then stop and tell the trainer.

> **A finding counts when** it has at least ten trials, a judge written in code, the trace of one successful trial and the model's name.

#### [capstone#attack-block] Attack · 120 minutes

*Attack*

Record every trial. Ten trials and a judge in code make a finding.

#### [capstone#harden-block] Harden · 90 minutes

*Harden*

For each confirmed finding: a test that fails, a fix, the test passing, benign tasks at 95% or more.

#### [capstone#rubric] The rubric

*How presentations are scored*

| Item | Value |
| --- | --- |
| Threat model | 20% |
| Attack evidence | 20% |
| Containment and authorisation | 30% |
| Guardrails and approvals | 15% |
| Regression suite and report | 15% |

> **The assessors read the evidence.** Attack logs row by row, one trace per finding, the commit history, and the suite running.

#### [capstone#format] Ten minutes of defence, five minutes of questions

*Format*

- **1 · One attack, twice.** Reproduce one attack on the build as found. Run it on your build and show which control refuses it, in the action log.
- **2 · What the others found.** Each confirmed finding: its rate, the test that failed, the fix, the test passing, and what the fix cost benign tasks.
- **3 · What remains.** The residual-risk statement: what is closed exactly, what is lowered to a rate, what is open, and who accepts it.

> **Peer feedback.** After each defence, the attacking team says which open point it would try next.

#### [capstone#running-order] Who defends when

*Running order*

| # | Team | Attacked by |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first defence*

Rehearse the one attack on this screen, on both builds. Record a backup run.

#### [capstone#now-presenting] Now defending

*Now defending*

#### [capstone#review] What the day showed

*Trainer review*

- **Strongest patterns.** Controls that held against every attacker, and why.
- **Common gaps.** Paths most builds left open, and suites that were green without testing.
- **One surprise.** A finding nobody had in a threat model.

#### [capstone#what-next] Keep going

*After the course*

- **In two weeks, the follow-up task:** the supplier changes the model. Rerun your suite with the second model profile, on the build as found and on yours
- **Send one page:** which tests changed, which new entry point the new model obeys, and whether your residual-risk statement still holds
- **Your repository stays yours:** keep the suite running on every change
- **Next Academy course:** AE-407, AI Assurance, Red Teaming and Governance for Engineering Leads

#### [capstone#thanks] Thank you

*SDAIA Academy*

Securing Language Model and Agent Applications
