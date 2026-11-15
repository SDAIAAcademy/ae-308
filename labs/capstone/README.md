# Capstone: red-team day

A timed attack on another team's hardened agent, a final hardening pass on your own, and a live defence of what risk remains. AI assistants are allowed all day, attacker models included: log every prompt you give one, and be ready to defend every line you submit.

## Before the day

Each team owns a repository that holds:

| File | What it is |
|---|---|
| `build.py` | Your hardened build: a function `controls()` that returns the controls of your agent. Start from the copy in this folder, which returns the course's reference build, and change it: remove what you can show is not needed, add what your threat model asks for |
| `threat_model.md` | Start from `threat_model_template.md`: the data-flow diagram, at least 12 threats, each mapped to a risk entry and a technique and scored on the national scale |
| `attack_log.jsonl` | Your own attack evidence from Days 2 to 4: one row per trial |
| `ci/` | The regression suite of Lab 4.4, extended, passing in the pipeline |

## The day

| Block | Time | What happens |
|---|---|---|
| Rules | 20 min | Teams exchange repositories. Each attacker states its rules of engagement (Lab 4.4): target, scope, budget of model calls, stop conditions |
| Attack | 120 min | Attack the other team's `build.py` with `attack.py`. Record every trial. A finding needs at least ten trials and a judge written in code |
| Report | 40 min | Hand over `findings.md` (from `findings_template.md`): each finding keyed to a risk-list entry, with its rate and interval, the trace of one successful trial, and a proposed regression test |
| Harden | 90 min | Fix what the other team found in your build. Every confirmed finding becomes a test in `ci/security_suite.py` that fails before the fix and passes after it. Benign tasks stay at 95% or more |
| Defend | 15 min per team | Ten minutes of defence, five of questions: your residual-risk statement (`residual_risk_template.md`). You reproduce one attack on the build as found and show why it now fails |

```bash
cd labs
uv run python capstone/attack.py --build capstone/build.py --attacks data/attacks.jsonl --trials 10
uv run python capstone/attack.py --build ../../other-team/build.py --attacks my_attacks.jsonl --trials 10 --log attack_log.jsonl
```

The first line runs all thirty starter attacks at ten trials against your own build: about 2,500 model calls, so run it with the stand-in, never against a hosted model and never out of the attack budget of 600 calls. The attack budget counts the calls made against the other team's build.

An attack is one JSON line with the fields of `data/attacks.jsonl`: `id`, `technique`, `channel` (`email`, `invoice`, `kb`, `tool`, `chat`), `goal`, `lang`, `msg_id`, `task`, `text`, `attacker`. The judge decides by `goal` from the state of the world. With the stand-in model the wording that works is bounded by what it recognises (see `PATTERNS` in `mukhallis.py`); the channel, the goal, the victim task and what you combine are yours to choose. With a hosted model, any wording is in scope: report the model's name with every rate.

## What you submit

A public repository link per team. The assessors read the attack logs, the tool-call traces and the commit history.

| Rubric criterion | Weight | Evidence in the repository |
|---|---|---|
| Threat model | 20 | `threat_model.md`: diagram, 12 or more threats, mapped and scored, the untested ones named |
| Attack evidence | 20 | `attack_log.jsonl` and `findings.md`: a rate and an interval per technique, in Arabic and English |
| Containment and authorisation | 30 | `build.py`: the rerun in which every logged exfiltration path fails with 95% of benign tasks passing; the token audit; the confused-deputy test failing |
| Guardrails and approvals | 15 | The tuning report with both error rates; the approval placement with its counts |
| Regression suite and report | 15 | `ci/` passing in the pipeline; `residual_risk.md` |

## Follow-up task, two weeks later

The supplier changes the model. Run your suite again with `MUKHALLIS_PROFILE=v2`, on the build as found and on your build, and send one page: which tests changed, which new entry point the new model obeys, and whether your residual-risk statement still holds.

## Ground rules

Synthetic data only. No payload leaves the lab. Out of scope: the other team's laptops, accounts and repository settings, and anything that is not the agent. Stop and tell the trainer if anything real is reached.
