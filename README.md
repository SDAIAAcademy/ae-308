<!-- academy:title -->
# Securing Language Model and Agent Applications

تأمين تطبيقات النماذج اللغوية والوكلاء

AI Engineering Track · SDAIA Academy · AE-308 · Level 300

REPLACE: one line under the title: what participants can do after the course

Participants attack and then defend a working agent: a synthetic clearance assistant for a fictional port authority that reads importers' emails and invoices, searches a tariff knowledge base, remembers each importer, runs code to compute duties and acts through Model Context Protocol (MCP) servers. They threat-model it, run injection, exfiltration and poisoning attacks over repeated trials, then contain it with a sandbox and egress rules, scoped short-lived delegated tokens, separated privileged and quarantined model calls, measured guardrails and approvals placed where a person adds safety. Red-team programmes are AE-407.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ae-308/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Prepare a threat model with data flows, trust boundaries and threats mapped to recognised risk lists and adversary-technique catalogues, given the clearance agent, its tool list and the classification of its data | Applied | a threat model with at least 12 threats, each mapped and scored on the national four-by-four likelihood and impact scale |
| LO2 | Test the application with direct, indirect, memory and tool-poisoning attacks in Arabic and English over repeated trials, given a starter attack corpus and a fixed budget of model calls | Applied | an attack log with a success rate and interval for each technique |
| LO3 | Design containment for generated code and outbound actions with a sandbox, an egress allowlist and recipient rules, given the attack log and 50 benign tasks | Performance | a rerun in which every logged exfiltration path fails while at least 95% of benign tasks still pass |
| LO4 | Build delegated authorisation in which each tool call carries an exchanged token with one audience, a narrow scope and a short lifetime, given two protocol servers that share one API key and a containerised identity provider | Performance | a token audit and a confused-deputy test that fails against the hardened design |
| LO5 | Configure input guardrails and output validation and measure their false-positive and false-negative rates, given bilingual attack and benign sets | Applied | a tuning report with the chosen thresholds and both error rates |
| LO6 | Defend a residual-risk statement after another team attacks the hardened agent, with each confirmed finding turned into a regression test, given a timed red-team exercise | Performance | a findings report keyed to risk-list entries, a passing regression suite and a live defence |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Model the threats | A fooled model must break nothing important; Data flows and trust boundaries; Risk lists and technique catalogues; Scoring and choosing what to test | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Attack | Direct and indirect injection; Exfiltration paths; Memory and retrieval poisoning; Hostile tools | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Contain | Sandboxes for generated code; Egress rules as capability grants; Delegated authorisation; Privileged and quarantined calls | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Guard, approve and verify | Guardrails and their error rates; Validating outputs and tool arguments; Approvals that people can judge; Audit logs and regression suites | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Run the agent on ten tasks and list every entry point for untrusted text and every action it can take | [`D1_1_run_agent_ten.ipynb`](labs/D1_1_run_agent_ten.ipynb) |
| 1.2 | Day 1 · Session 2 | Draw the data-flow diagram and mark private data, untrusted content and exit paths | [`D1_2_draw_data_flow.ipynb`](labs/D1_2_draw_data_flow.ipynb) |
| 1.3 | Day 1 · Session 3 | Map ten threats to OWASP risk entries and MITRE ATLAS techniques | [`D1_3_map_ten_threats.ipynb`](labs/D1_3_map_ten_threats.ipynb) |
| 1.4 | Day 1 · Session 4 | Score the threats on the national likelihood and impact scale and pick five to attack | [`D1_4_score_threats_national.ipynb`](labs/D1_4_score_threats_national.ipynb) |
| 2.1 | Day 2 · Session 1 | Inject through an importer email and a poisoned invoice, ten trials each, and record success rates | [`D2_1_inject_through_importer.ipynb`](labs/D2_1_inject_through_importer.ipynb) |
| 2.2 | Day 2 · Session 2 | Leak a synthetic importer record through a rendered link, a tool argument and the permitted email tool | [`D2_2_leak_synthetic_importer.ipynb`](labs/D2_2_leak_synthetic_importer.ipynb) |
| 2.3 | Day 2 · Session 3 | Plant an instruction in the knowledge base and in importer memory and trigger it in a later session | [`D2_3_plant_instruction_knowledge.ipynb`](labs/D2_3_plant_instruction_knowledge.ipynb) |
| 2.4 | Day 2 · Session 4 | Change a protocol server's tool description after approval, observe the agent, then pin approved descriptions by hash | [`D2_4_change_protocol_server.ipynb`](labs/D2_4_change_protocol_server.ipynb) |
| 3.1 | Day 3 · Session 1 | Run the duty-calculation tool with no network and read-only mounts, then fix a symbolic-link escape | [`D3_1_run_duty_calculation.ipynb`](labs/D3_1_run_duty_calculation.ipynb) |
| 3.2 | Day 3 · Session 2 | Allow only the case-system host, show that email still leaks data, then close it with recipient rules | [`D3_2_allow_only_case.ipynb`](labs/D3_2_allow_only_case.ipynb) |
| 3.3 | Day 3 · Session 3 | Replace the shared API key with exchanged, audience-bound short-lived tokens across two servers | [`D3_3_replace_shared_api.ipynb`](labs/D3_3_replace_shared_api.ipynb) |
| 3.4 | Day 3 · Session 4 | Split the agent so the model that reads invoices cannot call tools, and rerun the supplied attacks | [`D3_4_split_agent_so.ipynb`](labs/D3_4_split_agent_so.ipynb) |
| 4.1 | Day 4 · Session 1 | Tune an input classifier on bilingual attack and benign sets and report both error rates | [`D4_1_tune_input_classifier.ipynb`](labs/D4_1_tune_input_classifier.ipynb) |
| 4.2 | Day 4 · Session 2 | Check tool arguments against schemas and policy rules and escape model output before rendering | [`D4_2_check_tool_arguments.ipynb`](labs/D4_2_check_tool_arguments.ipynb) |
| 4.3 | Day 4 · Session 3 | Place one approval on outbound email, design what the approver sees and count approvals over 50 tasks | [`D4_3_place_one_approval.ipynb`](labs/D4_3_place_one_approval.ipynb) |
| 4.4 | Day 4 · Session 4 | Turn three supplied attacks into a regression suite in continuous integration, then choose the capstone target | [`D4_4_turn_three_supplied.ipynb`](labs/D4_4_turn_three_supplied.ipynb) |
<!-- /academy:labs -->

## Capstone

Red-team day: a timed attack on another team's hardened agent, then a final hardening pass on one's own, submitted as a public repository with threat model, attack log, findings and regression suite and defended live; the follow-up task re-runs the suite after a scripted model change

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- AE-207 Responsible and Secure AI Engineering Practice
- AE-302 Agentic Systems Engineering: Loops, Context and Harnesses
- Has built a tool-calling agent and read its traces
- Runs containers locally and changes their network settings

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Locally served open-weight models:** Ollama, vLLM, llama.cpp
- **Protocol servers and tool code:** official Model Context Protocol SDKs, plain function-calling tools
- **Container runtime with egress control:** Podman, Docker, gVisor
- **Identity provider supporting OAuth token exchange:** Keycloak, any OAuth 2 provider in a container
- **Agent and tool gateway:** agentgateway, a reverse proxy with allowlist rules written in the lab
- **Guardrail layer:** an open-source guardrail framework, an open-weight safety classifier
- **Attack tooling:** garak, PyRIT, promptfoo
- **Tracing and audit:** OpenTelemetry with Jaeger, Langfuse
- **Risk and technique references:** OWASP GenAI Security Project lists and testing guide, MITRE ATLAS
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- NDMO Data Classification Policy: REPLACE: the address of the official text
- National AI Risk Management Framework: REPLACE: the address of the official text
- SDAIA Generative AI Guidelines for Government: REPLACE: the address of the official text
- NCA Essential Cybersecurity Controls: REPLACE: the address of the official text
- NCA AI Cybersecurity Guidelines (AICG-1:2026, consultation draft): REPLACE: the address of the official text
