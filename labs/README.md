# Securing Language Model and Agent Applications: labs

## Quick start

- Google Colab: open a notebook from the course page; its first cell clones this repository.
- Locally: clone the repository, then open the notebooks in `labs/` with Jupyter.

| Unit | Session | Notebook |
|---|---|---|
| Day 1 | Session 1 · A fooled model must break nothing important | [`D1_1_run_agent_ten.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_1_run_agent_ten.ipynb) |
| Day 1 | Session 2 · Data flows and trust boundaries | [`D1_2_draw_data_flow.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_2_draw_data_flow.ipynb) |
| Day 1 | Session 3 · Risk lists and technique catalogues | [`D1_3_map_ten_threats.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_3_map_ten_threats.ipynb) |
| Day 1 | Session 4 · Scoring and choosing what to test | [`D1_4_score_threats_national.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D1_4_score_threats_national.ipynb) |
| Day 2 | Session 1 · Direct and indirect injection | [`D2_1_inject_through_importer.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_1_inject_through_importer.ipynb) |
| Day 2 | Session 2 · Exfiltration paths | [`D2_2_leak_synthetic_importer.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_2_leak_synthetic_importer.ipynb) |
| Day 2 | Session 3 · Memory and retrieval poisoning | [`D2_3_plant_instruction_knowledge.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_3_plant_instruction_knowledge.ipynb) |
| Day 2 | Session 4 · Hostile tools | [`D2_4_change_protocol_server.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D2_4_change_protocol_server.ipynb) |
| Day 3 | Session 1 · Sandboxes for generated code | [`D3_1_run_duty_calculation.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_1_run_duty_calculation.ipynb) |
| Day 3 | Session 2 · Egress rules as capability grants | [`D3_2_allow_only_case.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_2_allow_only_case.ipynb) |
| Day 3 | Session 3 · Delegated authorisation | [`D3_3_replace_shared_api.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_3_replace_shared_api.ipynb) |
| Day 3 | Session 4 · Privileged and quarantined calls | [`D3_4_split_agent_so.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D3_4_split_agent_so.ipynb) |
| Day 4 | Session 1 · Guardrails and their error rates | [`D4_1_tune_input_classifier.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_1_tune_input_classifier.ipynb) |
| Day 4 | Session 2 · Validating outputs and tool arguments | [`D4_2_check_tool_arguments.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_2_check_tool_arguments.ipynb) |
| Day 4 | Session 3 · Approvals that people can judge | [`D4_3_place_one_approval.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_3_place_one_approval.ipynb) |
| Day 4 | Session 4 · Audit logs and regression suites | [`D4_4_turn_three_supplied.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ae-308/blob/main/labs/D4_4_turn_three_supplied.ipynb) |

The notebooks are generated from the percent-format sources in `labs/_src/` by `labs/_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `labs/solutions/`. Edit the sources, not the notebooks.
