<!-- academy:title -->
# Securing Language Model and Agent Applications

تأمين تطبيقات النماذج اللغوية والوكلاء

AI Engineering Track · SDAIA Academy · AE-308 · Level 300

Attack a working agent over repeated trials, then contain it so that a fooled model breaks nothing important

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
| Capstone | Capstone: red-team day and live defence |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**Fanar Ports Authority.** It is a fictional Gulf-coast port authority. Its platform team built Mukhallis, a clearance assistant that reads importers' emails and invoices, searches the tariff notes, remembers each importer, runs code to compute duties and acts through two protocol servers, the case system and outbound communications. Participants take it as found, threat-model it, attack it over repeated trials and contain it. Every one of the 400 importer records, the 200 emails and invoices, the tariff notes and the attack texts is synthetic, generated with a fixed seed, and planted with the weaknesses the labs find: one API key shared by both servers, a server that acts for anyone, a link inside the duty tool's work folder, a tool description that changes after approval, and legitimate Arabic requests that a guardrail blocks.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Entry points and actions | [`D1_1_entry_points_actions.ipynb`](labs/D1_1_entry_points_actions.ipynb) |
| 1.2 | Day 1 · Session 2 | The data-flow diagram | [`D1_2_data_flow_diagram.ipynb`](labs/D1_2_data_flow_diagram.ipynb) |
| 1.3 | Day 1 · Session 3 | Ten threats, mapped | [`D1_3_map_threats.ipynb`](labs/D1_3_map_threats.ipynb) |
| 1.4 | Day 1 · Session 4 | Score and choose five | [`D1_4_score_and_choose.ipynb`](labs/D1_4_score_and_choose.ipynb) |
| 2.1 | Day 2 · Session 1 | Injection over ten trials | [`D2_1_injection_trials.ipynb`](labs/D2_1_injection_trials.ipynb) |
| 2.2 | Day 2 · Session 2 | One record, three exits | [`D2_2_exfiltration_paths.ipynb`](labs/D2_2_exfiltration_paths.ipynb) |
| 2.3 | Day 2 · Session 3 | Plant now, trigger later | [`D2_3_memory_kb_poisoning.ipynb`](labs/D2_3_memory_kb_poisoning.ipynb) |
| 2.4 | Day 2 · Session 4 | A changed tool, then pins | [`D2_4_hostile_tools.ipynb`](labs/D2_4_hostile_tools.ipynb) |
| 3.1 | Day 3 · Session 1 | The duty tool in a sandbox | [`D3_1_sandbox.ipynb`](labs/D3_1_sandbox.ipynb) |
| 3.2 | Day 3 · Session 2 | Egress, then recipients | [`D3_2_egress_recipients.ipynb`](labs/D3_2_egress_recipients.ipynb) |
| 3.3 | Day 3 · Session 3 | Exchanged tokens, two servers | [`D3_3_token_exchange.ipynb`](labs/D3_3_token_exchange.ipynb) |
| 3.4 | Day 3 · Session 4 | Split the agent | [`D3_4_quarantined_calls.ipynb`](labs/D3_4_quarantined_calls.ipynb) |
| 4.1 | Day 4 · Session 1 | Tune the input guardrail | [`D4_1_guardrail_error_rates.ipynb`](labs/D4_1_guardrail_error_rates.ipynb) |
| 4.2 | Day 4 · Session 2 | Validate arguments, escape output | [`D4_2_validate_arguments_output.ipynb`](labs/D4_2_validate_arguments_output.ipynb) |
| 4.3 | Day 4 · Session 3 | One approval on outbound email | [`D4_3_approvals.ipynb`](labs/D4_3_approvals.ipynb) |
| 4.4 | Day 4 · Session 4 | Three attacks as a suite | [`D4_4_regression_suite.ipynb`](labs/D4_4_regression_suite.ipynb) |
<!-- /academy:labs -->

## Capstone

Red-team day: a timed attack on another team's hardened agent, then a final hardening pass on one's own, submitted as a public repository with threat model, attack log, findings and regression suite and defended live; the follow-up task re-runs the suite after a scripted model change

**Submission:** A public GitHub repository per team holding the threat model (at least 12 threats, mapped and scored), the attack log with a success rate and interval per technique, the findings report keyed to risk-list entries, the hardened build and the regression suite passing in continuous integration, with the prompts of any attacker model logged and the commit history kept. Then a ten-minute live defence of the residual-risk statement and five minutes of questions: the team reproduces one attack on the build as found and shows why it now fails.

## Prerequisites

- AE-207 Responsible and Secure AI Engineering Practice
- AE-302 Agentic Systems Engineering: Loops, Context and Harnesses
- Has built a tool-calling agent and read its traces
- Runs containers locally and changes their network settings

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Locally served open-weight models:** a free hosted open-weight model (the labs' option), Ollama, vLLM, llama.cpp
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

### Risk lists and technique catalogues

- [OWASP Top 10 for LLM Applications 2026 (OWASP GenAI Security Project)](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [OWASP Top 10 for Agentic Applications for 2026 (OWASP GenAI Security Project)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [MITRE ATLAS data, version 5.6.0](https://github.com/mitre-atlas/atlas-data)

### Injection, exfiltration and design patterns

- [Simon Willison: The lethal trifecta for AI agents (June 2025)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [Simon Willison: The Dual LLM pattern for building AI assistants that can resist prompt injection (2023)](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)
- [Debenedetti and others: Defeating Prompt Injections by Design (CaMeL), 2025](https://arxiv.org/abs/2503.18813)
- [Beurer-Kellner and others: Design Patterns for Securing LLM Agents against Prompt Injections, 2025](https://arxiv.org/abs/2506.08837)
- [Debenedetti and others: AgentDojo, a dynamic environment to evaluate prompt injection attacks and defenses for LLM agents, 2024](https://arxiv.org/abs/2406.13352)

### Protocols, identity and authorisation

- [Model Context Protocol specification: authorization](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Model Context Protocol specification: security best practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707)
- [Keycloak: configuring and using token exchange](https://www.keycloak.org/securing-apps/token-exchange)
- [agentgateway](https://agentgateway.dev/)

### Tools named as examples

- [garak, the LLM vulnerability scanner](https://github.com/NVIDIA/garak)
- [PyRIT, the Python Risk Identification Tool for generative AI](https://github.com/Azure/PyRIT)
- [promptfoo: red teaming guide](https://www.promptfoo.dev/docs/red-team/)
- [Python documentation: audit events](https://docs.python.org/3/library/audit_events.html)
- [scikit-learn: LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)

### National references

- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Data Classification Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)
- [National AI Risk Management Framework, English executive summary (SDAIA, April 2026)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf)
- [National AI Risk Management Framework, full text in Arabic (SDAIA, April 2026)](https://sdaia.gov.sa/ar/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryAr.pdf)
- [Generative AI Guidelines for Government (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf)
- [National Cybersecurity Authority: controls list (Essential Cybersecurity Controls; AI Cybersecurity Guidelines AICG-1:2026, consultation draft)](https://nca.gov.sa/en/regulatory-documents/controls-list/)
<!-- /academy:sources -->
