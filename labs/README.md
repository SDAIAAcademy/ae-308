# Securing Language Model and Agent Applications: labs

Sixteen 25-minute labs on one synthetic agent: **Mukhallis (مُخلِّص)**, the clearance assistant of the fictional **Fanar Ports Authority**. It reads importers' emails and invoices, searches the tariff notes, remembers each importer, runs code to compute duties and acts through two protocol servers. You take it as found, model its threats, attack it over repeated trials, then contain it. Every lab starts from a supplied reference state and has a solution in `solutions/`, so none depends on an earlier one.

**The attack labs.** The payloads are run against this course's own agent, in your own notebook, on this synthetic data, and nowhere else. The kit has no real network: every host name ends in `.example` and outbound requests only write a log.

## Quick start

- **Google Colab:** open a notebook from the table below; its first cell clones this repository. Run `00_setup_check.ipynb` first.
- **Locally** (Python 3.11 to 3.13, [uv](https://docs.astral.sh/uv/)):

  ```bash
  git clone https://github.com/SDAIAAcademy/ae-308.git
  cd ae-308/labs
  uv run jupyter lab
  ```

  On Windows, run `git config --global core.longpaths true` once and set `UV_PROJECT_ENVIRONMENT` to a short folder outside the course before `uv run`.

Nothing downloads a model and no key is needed. A laptop processor is enough: no accelerator, no container runtime, no cluster.

| Unit | Session | Notebook |
|---|---|---|
| Setup | Before Day 1 | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/00_setup_check.ipynb) |
| Day 1 | 1.1 · Entry points and actions | [`D1_1_entry_points_actions.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_1_entry_points_actions.ipynb) |
| Day 1 | 1.2 · The data-flow diagram | [`D1_2_data_flow_diagram.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_2_data_flow_diagram.ipynb) |
| Day 1 | 1.3 · Ten threats, mapped | [`D1_3_map_threats.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_3_map_threats.ipynb) |
| Day 1 | 1.4 · Score and choose five | [`D1_4_score_and_choose.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_4_score_and_choose.ipynb) |
| Day 2 | 2.1 · Injection over ten trials | [`D2_1_injection_trials.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_1_injection_trials.ipynb) |
| Day 2 | 2.2 · One record, three exits | [`D2_2_exfiltration_paths.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_2_exfiltration_paths.ipynb) |
| Day 2 | 2.3 · Plant now, trigger later | [`D2_3_memory_kb_poisoning.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_3_memory_kb_poisoning.ipynb) |
| Day 2 | 2.4 · A changed tool, then pins | [`D2_4_hostile_tools.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_4_hostile_tools.ipynb) |
| Day 3 | 3.1 · The duty tool in a sandbox | [`D3_1_sandbox.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_1_sandbox.ipynb) |
| Day 3 | 3.2 · Egress, then recipients | [`D3_2_egress_recipients.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_2_egress_recipients.ipynb) |
| Day 3 | 3.3 · Exchanged tokens, two servers | [`D3_3_token_exchange.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_3_token_exchange.ipynb) |
| Day 3 | 3.4 · Split the agent | [`D3_4_quarantined_calls.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_4_quarantined_calls.ipynb) |
| Day 4 | 4.1 · Tune the input guardrail | [`D4_1_guardrail_error_rates.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_1_guardrail_error_rates.ipynb) |
| Day 4 | 4.2 · Validate arguments, escape output | [`D4_2_validate_arguments_output.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_2_validate_arguments_output.ipynb) |
| Day 4 | 4.3 · One approval on outbound email | [`D4_3_approvals.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_3_approvals.ipynb) |
| Day 4 | 4.4 · Three attacks as a suite | [`D4_4_regression_suite.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_4_regression_suite.ipynb) |

Before Day 1: [`PREWORK.md`](PREWORK.md). For the red-team day: [`capstone/`](capstone/README.md).

Exercises are marked **✏️ Exercise** and raise `NotImplementedError` until you fill them in. The cell after each exercise has a safety net: it falls back on the reference result in `data/reference/`, so an unfinished exercise never blocks the next one. Cells marked **✱ Stretch** are optional. Labs write their outputs to `artifacts/`, which is not committed.

## The model

| Setting | Model | Use |
|---|---|---|
| default, or `MUKHALLIS_MODEL=standin` | A scripted stand-in (`StandIn` in `mukhallis.py`). It does each task step by step and, when it reads instruction-like text, obeys it at a rate that depends on where the text came from (chat, email, invoice, tariff note, memory, tool description), on its style and on its language. The draw is seeded by the wording and the trial number | Everyone gets the same runs, and a rate over ten trials is reproducible. Its rates are its own: the decks say so wherever a number is the stand-in's |
| `MUKHALLIS_MODEL=hosted` and `OPENROUTER_API_KEY` | A free hosted open-weight model on OpenRouter (`MUKHALLIS_HOSTED_MODEL`, default `google/gemma-4-31b-it:free`), called over the chat-completions shape with tools | Optional, synthetic data only. Results vary from run to run: repeat each attempt and report a rate with the model's name. If a call fails, the stand-in finishes the run and the run's `model` says so |
| `MUKHALLIS_PROFILE=v2` | The stand-in after a scripted model change: stricter in English, weaker in Arabic, and it now obeys text on the rate page | The follow-up task: re-run the regression suite |

The stand-in recognises instructions of seven kinds, in English and Arabic (`PATTERNS` in `mukhallis.py`): send a record to an address, send replies to an address, remember a note, include an image, take a rate from an address, release the hold on this shipment, print the instructions. A hosted model needs no such list. Labs 1.1, 1.4, 2.1 to 2.4, 3.2 to 3.4 and 4.1 to 4.4 call the model. Labs 1.2, 1.3 and 3.1 call none.

## What stands in for what

The course's tool slots name a container runtime, an identity provider and a gateway. A Colab runtime has none of them, so the kit carries each mechanism in Python. The decisions you make in the labs are the ones you would make with the real tools.

| In production | In the labs | Real or simulated |
|---|---|---|
| Two Model Context Protocol servers | `Server` in `mukhallis.py`: two objects in process whose `list_tools()` and `call()` carry the shapes of `tools/list` and `tools/call` | Simulated transport, real tool logic |
| A container for generated code, with no network and read-only mounts | `sandbox.py`: a Python audit hook asks your policy before every file the code opens; no network | The policy and the link escape are real (a real symbolic link or junction, `os.path.realpath`); the isolation is a teaching stand-in, not a security boundary |
| An egress gateway with an allowlist | `world.net`, the one place every outbound request passes, and its log `world.egress` | Simulated network, real allowlist logic |
| An identity provider with OAuth token exchange (for example Keycloak in a container) | `Idp` in `mukhallis.py`: signed tokens (JWT, HS256) and the request and response of RFC 8693 | Real tokens and messages, in process |
| An open-weight safety classifier | A character n-gram classifier trained in the lab with scikit-learn | Real training and measurement, a small model |
| A person approving email | `Approver` in `mukhallis.py`, a scripted stand-in whose attention falls with every request | Simulated; its numbers are not measurements of people |

## The case and its data

All of it is synthetic, written by `prepare_data.py` (seed 308, standard library only). No real person, company, address or account is described: identifiers have the right shape and belong to nobody.

| File | What it is |
|---|---|
| `data/importers.csv` | 400 importer records, classified Restricted: contact, registered broker, mobile, commercial registration, IBAN, credit limit |
| `data/inbox.jsonl` | 200 messages in English and Arabic: 80 clearance requests with an invoice, 70 tariff questions, 50 status requests |
| `data/kb.jsonl`, `data/tariff/rates.json` | 12 bilingual tariff notes; the duty rates, exchange rates and the GCC origin list the duty code reads |
| `data/tasks.jsonl` | 50 benign tasks with their expected result. A task passes when one email went to exactly the registered recipients with the right figure |
| `data/attacks.jsonl` | The starter attack corpus: 30 attacks by technique, channel, goal, style and language, each mapped to OWASP entries and a MITRE ATLAS technique |
| `data/guardrail_set.jsonl` | 640 attack and benign texts for Lab 4.1, with `train`, `tune` and `test` splits |
| `data/service_log.jsonl` | One day of the importer portal's chapter-suggestion service log for the Lab 4.4 stretch: 3,844 requests from 22 accounts, with the minute of the day, key, goods description, chapter returned, whether every score was asked, whether a declaration followed |
| `data/threats.json`, `data/catalogue.json`, `data/dfd.json` | Day 1: ten threats, the risk lists and techniques, the data-flow diagram |
| `data/reference/` | The result of every exercise, which the safety-net cells read |

| Module | What it is |
|---|---|
| `mukhallis.py` | The agent as found: tools, the two servers, the identity provider, the stand-in and hosted models, the loop with its named places for controls, the attack and benign runners |
| `sandbox.py` | The duty-code runner and its policy layer |
| `reference_build.py` | The hardened build: every control of the course, switched on. Read it after you tried a lab, not before |
| `fanar.py` | Helpers: loading, checks, tables, the Wilson interval, the national risk bands |
| `ci/security_suite.py`, `ci/security-regression.yml` | The regression suite as a program, and a pipeline file to copy into the capstone repository |

Planted weaknesses, each found by a lab: one API key shared by both servers and written in the system prompt (3.3); the comms server asks the case server for anything on anyone's behalf (3.3); the duty code runs with the network and the whole disk (3.1); a link in the work folder (3.1); `fetch_rate` takes any address (2.2, 4.2); the case screen fetches images (2.2, 4.2); six benign tasks need a registered broker in copy (3.2); a guardrail that learns that an email address is an attack (4.1).

## For trainers

- Headless run of one lab: `uv run jupyter execute solutions/D2_1_injection_trials.ipynb`. `AE308_QUICK=1` shortens the long runs; the numbers in the decks come from the full runs.
- Reference results: running a source of `_src/` as a script with `AE308_WRITE_REF=1` writes that lab's results into `data/reference/`. Do it after changing the kit or the data, then rebuild the notebooks with `uv run python _tools/py2nb.py`.
- On Windows set `PYTHONUTF8=1` before a headless run.
- `solutions/answer_key.md` lists every planted weakness, the lab that finds it and the expected numbers. `solutions/capstone_trainer_notes.md` says what the hardened build still leaves open.
- Delete `artifacts/` before the course's own checks. Lab 3.1 leaves a link inside it: remove it as a link (`sandbox.workdir("d3_1")` empties that folder safely).
