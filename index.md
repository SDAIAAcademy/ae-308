---
course: "Securing Language Model and Agent Applications"
code: "AE-308"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-308/index.html"
---

# Securing Language Model and Agent Applications

تأمين تطبيقات النماذج اللغوية والوكلاء

AI Engineering Track · 4 teaching days + capstone day · 26 hours · Level 300

Attack a working agent over repeated trials, then contain it so that a fooled model breaks nothing important

Participants attack and then defend a working agent: a synthetic clearance assistant for a fictional port authority that reads importers' emails and invoices, searches a tariff knowledge base, remembers each importer, runs code to compute duties and acts through Model Context Protocol (MCP) servers. They threat-model it, run injection, exfiltration and poisoning attacks over repeated trials, then contain it with a sandbox and egress rules, scoped short-lived delegated tokens, separated privileged and quarantined model calls, measured guardrails and approvals placed where a person adds safety. Red-team programmes are AE-407.

**Who it is for:** Practitioners. Engineers who have completed the level 200 set or can show equivalent work: a deployed model or language model application they built and can explain.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Fanar Ports Authority.** Fanar Ports Authority is a fictional Gulf-coast port authority. Its platform team built Mukhallis, a clearance assistant that reads importers' emails and invoices, searches the tariff notes, remembers each importer, runs code to compute duties and acts through two protocol servers, the case system and outbound communications. Participants take it as found, threat-model it, attack it over repeated trials and contain it. Every one of the 400 importer records, the 200 emails and invoices, the tariff notes and the attack texts is synthetic, generated with a fixed seed, and planted with the weaknesses the labs find: one API key shared by both servers, a server that acts for anyone, a link inside the duty tool's work folder, a tool description that changes after approval, and legitimate Arabic requests that a guardrail blocks.

## The course

### Day 1: Model the threats

Slides: https://sdaiaacademy.github.io/ae-308/slides/day1.md

- **Session 1: A fooled model must break nothing important**
  - Explain why a design must hold when the model is fooled
  - List the entry points for untrusted text from run traces
  - List every action the agent can take and its effect
  - [Lab 1.1: Entry points and actions (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D1_1_entry_points_actions.ipynb)
- **Session 2: Data flows and trust boundaries**
  - Draw the agent as processes, stores, external entities and flows
  - Mark trust boundaries and the flows that cross them
  - Find where private data, untrusted content and an exit path meet
  - [Lab 1.2: The data-flow diagram (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D1_2_data_flow_diagram.ipynb)
- **Session 3: Risk lists and technique catalogues**
  - Tell a risk entry from an adversary technique
  - Map a threat to an OWASP entry and a MITRE ATLAS technique
  - State a threat as source, entry point, action and harm
  - [Lab 1.3: Ten threats, mapped (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D1_3_map_threats.ipynb)
- **Session 4: Scoring and choosing what to test**
  - Score a threat on the national four-by-four scale with a stated reason
  - Choose what to test under a fixed budget of model calls
  - Plan trials so that a success rate has a useful interval
  - [Lab 1.4: Score and choose five (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D1_4_score_and_choose.ipynb)

### Day 2: Attack

Slides: https://sdaiaacademy.github.io/ae-308/slides/day2.md

- **Session 1: Direct and indirect injection**
  - Tell direct injection from indirect injection by who writes the text
  - Run an attack over repeated trials and judge success by code
  - Report a success rate with an interval, in Arabic and English
  - [Lab 2.1: Injection over ten trials (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D2_1_injection_trials.ipynb)
- **Session 2: Exfiltration paths**
  - Name the exit paths of an agent from its tool list
  - Leak a record through a link, a tool argument and a permitted tool
  - Detect a leak in an egress log, encoded or not
  - [Lab 2.2: One record, three exits (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D2_2_exfiltration_paths.ipynb)
- **Session 3: Memory and retrieval poisoning**
  - Explain why stored text is more dangerous than passing text
  - Plant an instruction that retrieval returns for a chosen query
  - Trigger a memory instruction in a later session and measure it
  - [Lab 2.3: Plant now, trigger later (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D2_3_memory_kb_poisoning.ipynb)
- **Session 4: Hostile tools**
  - Explain why a tool description is an entry point
  - Observe an agent after a description changes post approval
  - Pin approved descriptions by hash and refuse a changed tool
  - [Lab 2.4: A changed tool, then pins (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D2_4_hostile_tools.ipynb)

### Day 3: Contain

Slides: https://sdaiaacademy.github.io/ae-308/slides/day3.md

- **Session 1: Sandboxes for generated code**
  - State what a sandbox for generated code must deny
  - Run a code tool with no network and read-only mounts
  - Fix a path check that a symbolic link escapes
  - [Lab 3.1: The duty tool in a sandbox (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D3_1_sandbox.ipynb)
- **Session 2: Egress rules as capability grants**
  - Write an egress allowlist by host for the agent's gateway
  - Show which leak an allowed host still carries
  - Close it with recipient rules while benign tasks still pass
  - [Lab 3.2: Egress, then recipients (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D3_2_egress_recipients.ipynb)
- **Session 3: Delegated authorisation**
  - Explain token passthrough and the confused deputy
  - Exchange a user token for an audience-bound short-lived token
  - Audit every tool call's token and test the deputy
  - [Lab 3.3: Exchanged tokens, two servers (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D3_3_token_exchange.ipynb)
- **Session 4: Privileged and quarantined calls**
  - Describe the privileged and the quarantined call
  - Split the agent so invoice text never reaches the planner
  - Rerun the attacks and state what the split leaves open
  - [Lab 3.4: Split the agent (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D3_4_quarantined_calls.ipynb)

### Day 4: Guard, approve and verify

Slides: https://sdaiaacademy.github.io/ae-308/slides/day4.md

- **Session 1: Guardrails and their error rates**
  - Compute false-positive and false-negative rates at a threshold
  - Tune a threshold on bilingual attack and benign sets
  - Report both error rates by language with intervals
  - [Lab 4.1: Tune the input guardrail (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D4_1_guardrail_error_rates.ipynb)
- **Session 2: Validating outputs and tool arguments**
  - Write an argument schema that rejects wrong types and ranges
  - Add policy rules that depend on the case in hand
  - Escape model output so that a link or image cannot fire
  - [Lab 4.2: Validate arguments, escape output (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D4_2_validate_arguments_output.ipynb)
- **Session 3: Approvals that people can judge**
  - Explain approval fatigue with counts from 50 tasks
  - Place one approval where a person adds safety
  - Design what the approver sees so that the decision is possible
  - [Lab 4.3: One approval on outbound email (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D4_3_approvals.ipynb)
- **Session 4: Audit logs and regression suites**
  - Read an action log to reconstruct what an agent did
  - Turn a confirmed attack into a regression test over trials
  - Gate a change on the suite in continuous integration
  - [Lab 4.4: Three attacks as a suite (25 min)](https://sdaiaacademy.github.io/ae-308/labs/D4_4_regression_suite.ipynb)

### Capstone: Capstone: red-team day and live defence

Slides: https://sdaiaacademy.github.io/ae-308/slides/capstone.md

## Capstone

Red-team day: a timed attack on another team's hardened agent, then a final hardening pass on one's own, submitted as a public repository with threat model, attack log, findings and regression suite and defended live; the follow-up task re-runs the suite after a scripted model change

**What you submit:** A public GitHub repository per team holding the threat model (at least 12 threats, mapped and scored), the attack log with a success rate and interval per technique, the findings report keyed to risk-list entries, the hardened build and the regression suite passing in continuous integration, with the prompts of any attacker model logged and the commit history kept. Then a ten-minute live defence of the residual-risk statement and five minutes of questions: the team reproduces one attack on the build as found and shows why it now fails.

**Rubric:**

- Threat model: 20%
- Attack evidence: 20%
- Containment and authorisation: 30%
- Guardrails and approvals: 15%
- Regression suite and report: 15%

## Outcomes

- **LO1** Prepare a threat model with data flows, trust boundaries and threats mapped to recognised risk lists and adversary-technique catalogues, given the clearance agent, its tool list and the classification of its data (Applied) Evidence: a threat model with at least 12 threats, each mapped and scored on the national four-by-four likelihood and impact scale
- **LO2** Test the application with direct, indirect, memory and tool-poisoning attacks in Arabic and English over repeated trials, given a starter attack corpus and a fixed budget of model calls (Applied) Evidence: an attack log with a success rate and interval for each technique
- **LO3** Design containment for generated code and outbound actions with a sandbox, an egress allowlist and recipient rules, given the attack log and 50 benign tasks (Performance) Evidence: a rerun in which every logged exfiltration path fails while at least 95% of benign tasks still pass
- **LO4** Build delegated authorisation in which each tool call carries an exchanged token with one audience, a narrow scope and a short lifetime, given two protocol servers that share one API key and a containerised identity provider (Performance) Evidence: a token audit and a confused-deputy test that fails against the hardened design
- **LO5** Configure input guardrails and output validation and measure their false-positive and false-negative rates, given bilingual attack and benign sets (Applied) Evidence: a tuning report with the chosen thresholds and both error rates
- **LO6** Defend a residual-risk statement after another team attacks the hardened agent, with each confirmed finding turned into a regression test, given a timed red-team exercise (Performance) Evidence: a findings report keyed to risk-list entries, a passing regression suite and a live defence

## Tools

- **Locally served open-weight models:** a free hosted open-weight model (the labs' option), Ollama, vLLM, llama.cpp
- **Protocol servers and tool code:** official Model Context Protocol SDKs, plain function-calling tools
- **Container runtime with egress control:** Podman, Docker, gVisor
- **Identity provider supporting OAuth token exchange:** Keycloak, any OAuth 2 provider in a container
- **Agent and tool gateway:** agentgateway, a reverse proxy with allowlist rules written in the lab
- **Guardrail layer:** an open-source guardrail framework, an open-weight safety classifier
- **Attack tooling:** garak, PyRIT, promptfoo
- **Tracing and audit:** OpenTelemetry with Jaeger, Langfuse
- **Risk and technique references:** OWASP GenAI Security Project lists and testing guide, MITRE ATLAS

## Prerequisites

- AE-207 Responsible and Secure AI Engineering Practice
- AE-302 Agentic Systems Engineering: Loops, Context and Harnesses
- Has built a tool-calling agent and read its traces
- Runs containers locally and changes their network settings
- Setup: a laptop processor with uv, or Google Colab. Nothing downloads a model and no key is needed; a free hosted model is optional. Run 00_setup_check before Day 1 and read labs/PREWORK.md.

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

---

SDAIA Academy · AI Engineering Track · Securing Language Model and Agent Applications

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit 98d8fe3
