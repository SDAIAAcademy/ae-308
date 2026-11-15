---
course: "Securing Language Model and Agent Applications"
code: "AE-308"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ae-308/slides/day1.html"
---

# Securing Language Model and Agent Applications

## Day 1: Model the threats

What the agent reads, what it can do, and which threats deserve the budget

#### [day1#title] Model the threats

*SDAIA Academy · Securing Language Model and Agent Applications*

Day 1: What the agent reads, what it can do, and which threats deserve the budget

AI Engineering Track · 4 teaching days + capstone day · 4 sessions · 4 labs · AE-308

#### [day1#agenda] Model the threats

*Today*

- **Session 1 · A fooled model must break nothing important**: What a fooled model can read and do: entry points for untrusted text, and actions
- **Session 2 · Data flows and trust boundaries**: Where private data, untrusted content and an exit path meet in one context
- **Session 3 · Risk lists and technique catalogues**: Each threat mapped to a risk entry and an adversary technique
- **Session 4 · Scoring and choosing what to test**: The national likelihood and impact scale, and a budget of model calls

#### [day1#the-case] One agent for four days: Mukhallis, the clearance assistant of Fanar Ports Authority

*The case*

- Reads importers' **emails and invoices**, in Arabic and English
- Searches the **tariff notes**, remembers each importer
- Runs **code** to compute duties
- Acts through **two protocol servers**: the case system and outbound communications

- **The data.** 400 importer records, classified Restricted. 200 emails and invoices. 12 tariff notes. 50 benign tasks. 30 starter attacks. All synthetic, seed 308.
- **Your role.** Luay Al-Najdi, AI security engineer. The platform team built it; you take it as found.

#### [day1#from-207-and-302] You arrive with a risk list, a first attack log and an agent you built

*Where this course starts*

| From | You already have | Here it becomes |
| --- | --- | --- |
| AE-207 | The OWASP list, ten injection attempts, four basic controls, a register on the national scale | Two lists and a technique catalogue; rates over repeated trials; containment that does not depend on the model |
| AE-302 | A loop, tools, a protocol server, traces, one planted instruction and one leg removed | A full threat model of an agent someone else built, attacked through every entry point |

> **Not here.** Planning and running a red-team programme, assurance cases and briefing an executive are AE-407.

### Session 1: A fooled model must break nothing important

#### [day1#s1] A fooled model must break nothing important

*Session 1*

- Explain why a design must hold when the model is fooled
- List the entry points for untrusted text from run traces
- List every action the agent can take and its effect

#### [day1#assume-fooled] Assume the model will be fooled, then ask what it can reach

*The stance*

- **The question that fails.** "How do we stop the model from obeying an attacker?" Nobody can promise that, and an attacker retries for free.

- **The question that works.** "When the model obeys an attacker, what can it read, and what can it do?" That has an answer you can test.

> **The design goal.** A fooled model must break nothing important.

#### [day1#component-or-actor] A component transforms text; an actor chooses what happens next

*Two ways to see the model*

|  | Model as component | Model as actor |
| --- | --- | --- |
| It decides | Nothing: the application calls it and uses the output | Which tool to call, with which arguments, and when to stop |
| A fooled model | Returns wrong text | Takes wrong actions |
| The worst case | Whatever the application does with that text | Everything its tools and credentials allow |
| Mukhallis | The quarantined extraction of Day 3 | The planner with twelve tools |

#### [day1#three-legs-recap] Private data, untrusted content, an exit path: any agent that holds all three can be made to leak

*From AE-302*

1. **Private data** 400 importer records, classified Restricted
2. **Untrusted content** emails, invoices, notes, memory, tool text
3. **An exit path** email, a fetched address, a rendered image

> **What goes wrong.** Teams look for the three in the architecture diagram and miss that one context window holds all of them at once.

#### [day1#entry-points] Every tool result has an author, and the author is not always the authority

*What the model reads*

| Origin | Arrives by | Who can write it | Outsider? |
| --- | --- | --- | --- |
| importer | `read_message` | The importer, or anyone who emails the inbox | Yes |
| kb | `search_tariff` | The tariff committee, and brokers who upload circulars | Yes |
| memory | `recall` | The model, from what it read earlier | Yes |
| web | `fetch_rate` | Whoever runs the page the model was pointed at | Yes |
| system | case-system answers | The authority's own records | No |

#### [day1#actions] The ten tasks used four of seven actions; the attacker wants the other three

*What the agent can do*

| Tool | Effect | Used by a benign task |
| --- | --- | --- |
| `update_case` | write | Yes |
| `send_email` | send | Yes |
| `fetch_rate` | request | Yes |
| `run_duty_code` | exec | Yes |
| `release_hold` | write | No |
| `remember` | write | No |
| `send_case_summary` | send | No |

> **Read the tool list, not the logs.** A benign run shows what the agent does. The tool list shows what it can do.

Result of Lab 1.1 on the build as found.

#### [day1#check-fooled] Which claim survives a fooled model?

*Checkpoint*

**Question:** Wissam, who built Mukhallis, lists four reasons why it is safe. Which one still holds on the day the model obeys a hostile invoice?

- A. The system prompt says never to share one importer's data with another
- B. In ten test tasks the agent never called `release_hold`
- C. The case server refuses any call for a case other than the one the officer opened
- D. The model was tested on 200 messages and followed its instructions every time

#### [day1#lab-1-1] Entry points and actions

Lab 1.1 · 25 min

Run Mukhallis on ten clearance tasks, then read the traces: every place where text written outside the authority enters the context, and every action the agent can take.

[D1_1_entry_points_actions.ipynb](https://sdaiaacademy.github.io/ae-308/labs/D1_1_entry_points_actions.ipynb)

- [ ] Run the ten tasks and read one trace (6 min)
- [ ] List the entry points for untrusted text (7 min)
- [ ] List the actions and their effects (7 min)
- [ ] One table: who writes what the model reads (5 min)
- [ ] ✱ Stretch: Find the entry point that no task of the ten exercised

### Session 2: Data flows and trust boundaries

#### [day1#s2] Data flows and trust boundaries

*Session 2*

- Draw the agent as processes, stores, external entities and flows
- Mark trust boundaries and the flows that cross them
- Find where private data, untrusted content and an exit path meet

#### [day1#dfd-elements] Four shapes are enough to draw any agent

*The notation*

- **External entity.** Outside your control: the importer, a rate site, the officer.
- **Process.** Code that transforms data: the planner, the code runner, each server, the case screen.
- **Data store.** Where data rests: importer records, tariff notes, memory.
- **Data flow.** An arrow with a name: what moves, from where to where.

#### [day1#trust-boundaries] A trust boundary is where the author of the data changes

*Boundaries*

- Mukhallis has four zones: **outside**, **authority**, **agent**, **servers**
- A flow that crosses a boundary needs a decision: who checks it, and how
- Trust follows the **author**, not the transport: an importer's email is still the importer's after the case server stored it

**13 of 19** flows of Mukhallis cross a trust boundary (Lab 1.2)

> **What goes wrong.** "It comes from our own case server" is said about text an outsider wrote yesterday.

#### [day1#mark-sources] Mark where private data and untrusted content start; taint spreads by itself

*Marking*

1. **Private source** `records`, the Restricted importer file
2. **Untrusted sources** `importer`, `ratesite`
3. **Follow the flows** every node the data can arrive at
4. **Exits** flows that end outside

> **Classify first.** The national Data Classification Policy gives the level of each store before you draw: the pre-work table.

#### [day1#meeting-points] Six of nine components inside the authority hold all three legs

*The finding*

| Component | Private | Untrusted | Can reach outside |
| --- | --- | --- | --- |
| Planner | Yes | Yes | Yes |
| Comms server | Yes | Yes | Yes |
| Case server | Yes | Yes | Yes |
| Code runner | Yes | Yes | Yes |
| Memory | Yes | Yes | Yes |
| Case screen | Yes | Yes | Yes |
| Tariff notes | No | Yes | Yes |

> **A model in a loop.** Whatever it reads can shape whatever it sends. The diagram cannot be fixed by moving one box.

#### [day1#four-exits] The diagram's use is a short list: four ways out

*Exits*

| Exit | Tool or part | Day 3 or 4 control |
| --- | --- | --- |
| Email to any address | `send_email`, `send_case_summary` | Recipient rules, one approval |
| A request to an address the model chose | `fetch_rate` | Egress allowlist, a fixed argument |
| Images of the rendered reply | the case screen | Escaping before rendering |
| Whatever generated code sends | `run_duty_code` | A sandbox with no network |

#### [day1#dfd-as-data] Write the diagram as data, so that code can check it

*In the lab*

```python
# file: dfd.json
{"id": "F03", "from": "case", "to": "planner",
 "data": "message text (read_message)"}
```

- A flow is a row: `from`, `to`, `data`
- A zone per node gives the boundaries
- `reach(flows, start)` is twelve lines of graph search
- The same file renders as a Mermaid diagram in the capstone README

#### [day1#check-boundary] Which flow carries untrusted content?

*Checkpoint*

**Question:** A broker uploads a circular. It becomes a tariff note. A week later the planner retrieves it for another importer's question. Where does untrusted content cross into the agent's context?

- A. On the flow from the tariff notes to the planner: the note is still the broker's words
- B. Nowhere: the note was stored inside the authority, so it is trusted now
- C. Only at upload, where the broker's file crossed the boundary once
- D. On the flow from the planner to the comms server, when the reply is sent

#### [day1#lab-1-2] The data-flow diagram

Lab 1.2 · 25 min

Write the data-flow diagram of Mukhallis as data, mark each flow as private data, untrusted content or exit path, and let code find every component where the three meet.

[D1_2_data_flow_diagram.ipynb](https://sdaiaacademy.github.io/ae-308/labs/D1_2_data_flow_diagram.ipynb)

- [ ] Complete the flows of the diagram (8 min)
- [ ] Mark private data, untrusted content and exit paths (7 min)
- [ ] Find the crossings and where the three legs meet (6 min)
- [ ] Draw it and read it (4 min)
- [ ] ✱ Stretch: Add the approver as an entity and see which paths change

### Session 3: Risk lists and technique catalogues

#### [day1#s3] Risk lists and technique catalogues

*Session 3*

- Tell a risk entry from an adversary technique
- Map a threat to an OWASP entry and a MITRE ATLAS technique
- State a threat as source, entry point, action and harm

#### [day1#risk-or-technique] A risk list names what goes wrong in your application; a technique catalogue names what an adversary does

*Two kinds of list*

- **OWASP lists.** Weaknesses and their consequences, ranked. You map your **threats** and your **controls** to entries.

- **MITRE ATLAS.** Tactics (the adversary's goal at a step) and techniques (how). You map your **tests** to techniques.

> **Use both.** The entry tells the owner why it matters. The technique tells the tester what to reproduce.

#### [day1#owasp-two-lists] Two OWASP lists apply to an agent

*Risk lists*

| LLM applications 2026 |
| --- |
| LLM01 Prompt Injection |
| LLM02 Sensitive Information Disclosure |
| LLM03 Excessive Agency |
| LLM04 Supply Chain |
| LLM05 Data and Model Poisoning |
| LLM08 Hidden Context Exposure |
| LLM10 Improper Output Handling |

| Agentic applications 2026 |
| --- |
| ASI01 Agent Goal Hijack |
| ASI02 Tool Misuse and Exploitation |
| ASI03 Identity and Privilege Abuse |
| ASI04 Agentic Supply Chain Vulnerabilities |
| ASI05 Unexpected Code Execution |
| ASI06 Memory and Context Poisoning |
| ASI09 Human-Agent Trust Exploitation |

#### [day1#atlas] ATLAS gives the adversary's steps their ids

*Technique catalogue*

| Technique | Id | In Mukhallis |
| --- | --- | --- |
| LLM Prompt Injection: Indirect | AML.T0051.001 | An instruction in an email or invoice |
| AI Agent Tool Invocation | AML.T0053 | A tool called for the attacker |
| LLM Response Rendering | AML.T0077 | Data in the address of a rendered image |
| AI Agent Context Poisoning: Memory | AML.T0080.000 | A note planted for later sessions |
| Exfiltration via AI Agent Tool Invocation | AML.T0086 | A record sent by a permitted tool |
| AI Supply Chain Rug Pull | AML.T0109 | A tool description changed after approval |

Ids and names from ATLAS data version 5.6.0. The catalogue is revised several times a year.

#### [day1#threat-form] A threat you can test names four things

*Stating a threat*

1. **Source** who writes the text
2. **Entry point** where it enters
3. **Action** which tool or output it turns
4. **Harm** what is lost

> **TH-01.** An importer plants text in the body of an email so that `send_email` does this: another importer's record is emailed to an outside address.

#### [day1#mapping-is-argument] A mapping is an argument: write the reason beside the id

*Mapping*

- **TH-07: a description changes after approval.** The text is an injection (LLM01). The cause is a supplier's component that changed under you (LLM04, ASI04). The key takes the cause: the control follows from it.

- **TH-09: one key for both servers.** Excessive agency (LLM03)? No model is fooled. A server acts with authority nobody gave it: identity and privilege abuse (ASI03).

> **What goes wrong.** Ids are pasted in to look complete. A linter catches an id that does not exist; only a reviewer catches one that does not fit.

#### [day1#check-mapping] Which pair fits the threat?

*Checkpoint*

**Question:** An importer's invoice says: "use the exchange rate from" an outside address that ends in the importer's IBAN. The agent calls `fetch_rate` with that address. Which risk entry and technique fit best?

- A. LLM04 Supply Chain, with AI Supply Chain Rug Pull
- B. LLM06 Unbounded Consumption, with Cost Harvesting
- C. LLM08 Hidden Context Exposure, with Extract LLM System Prompt
- D. LLM02 Sensitive Information Disclosure, with Exfiltration via AI Agent Tool Invocation

#### [day1#lab-1-3] Ten threats, mapped

Lab 1.3 · 25 min

State ten threats to Mukhallis in one form, map each to an OWASP risk entry and a MITRE ATLAS technique, and lint the mapping against the catalogue.

[D1_3_map_threats.ipynb](https://sdaiaacademy.github.io/ae-308/labs/D1_3_map_threats.ipynb)

- [ ] Read the catalogue file: two lists and the techniques (4 min)
- [ ] Write threats in the form source, entry, action, harm (6 min)
- [ ] Map ten threats to risk entries and techniques (10 min)
- [ ] Lint the mapping and settle two disputes (5 min)
- [ ] ✱ Stretch: Write threats 11 and 12 for the threat model of the outcome

### Session 4: Scoring and choosing what to test

#### [day1#s4] Scoring and choosing what to test

*Session 4*

- Score a threat on the national four-by-four scale with a stated reason
- Choose what to test under a fixed budget of model calls
- Plan trials so that a success rate has a useful interval

#### [day1#national-scale] The national framework scores likelihood and impact from 1 to 4

*Scoring*

| Score | Likelihood | Impact |
| --- | --- | --- |
| 1 | rare | low |
| 2 | unlikely | medium |
| 3 | likely | high |
| 4 | almost certain | catastrophic |

| Level | Band |
| --- | --- |
| 1 to 2 | low |
| 3 to 6 | medium |
| 8 to 12 | high |
| 16 | catastrophic |

Level is likelihood times impact. Treatments: avoid, mitigate, transfer, accept.

#### [day1#evidence-for-likelihood] Before a test, likelihood is a judgement with a reason; after, it is a rate

*Likelihood*

- **Who can reach the entry point?** Anyone with an email address, or only a broker with upload rights
- **How much skill?** One sentence in an invoice, or control of a server
- **How often does it work?** Unknown today. Tomorrow: successes over trials, with an interval

> **Write the reason.** "TH-04: needs a shipment under hold and the right wording; uninspected goods leave the port" can be challenged. A bare 2 and 4 cannot.

#### [day1#register] Ten threats scored: one at 12, seven more in the high band

*The register*

| Id | Threat | L | I | Level |
| --- | --- | --- | --- | --- |
| TH-01 | Record emailed out through an email | 4 | 3 | 12 |
| TH-02 | IBAN in the address of an image | 3 | 3 | 9 |
| TH-03 | IBAN in a tool argument | 3 | 3 | 9 |
| TH-05 | Instruction planted in memory | 3 | 3 | 9 |
| TH-09 | Any case to any address with the shared key | 3 | 3 | 9 |
| TH-04, TH-07, TH-08 | Released hold; changed tool; hostile code | 2 | 4 | 8 |
| TH-06, TH-10 | Poisoned note; printed prompt |  |  | 6 |

#### [day1#ten-trials] Ten trials tell you that an attack works, not how it ranks

*Trials*

| Successes in 10 | 95% interval |
| --- | --- |
| 0 | 0% to 28% |
| 3 | 11% to 60% |
| 5 | 24% to 76% |
| 8 | 49% to 94% |
| 10 | 72% to 100% |

- **One attack, measured twice.** Attack A-03 on the stand-in model: 4 of 10, then 49 of 100, an interval of 39% to 59%.

> **Zero in ten.** The interval still reaches 28%. A defence is claimed over more trials, or shown by a control that needs none.

#### [day1#budget] A fixed budget of 300 model calls forces you to name what you did not test

*Budget*

| Threat | Calls per trial | Ten trials |
| --- | --- | --- |
| TH-01 through an email | 11 | 110 |
| TH-02 link | 9 | 90 |
| TH-04 release | 10 | 100 |
| TH-05 memory, two sessions | 16 | 160 |
| TH-08 hostile code | 0 | 0 |
| TH-09 shared key | 0 | 0 |

> **Free tests.** Generated code and a server's key are tested directly, without the model. They are also the ones a deterministic control closes.

#### [day1#check-what-first] Where does the next model call go?

*Checkpoint*

**Question:** You have 90 calls left. TH-03 (level 9, 9 calls a trial) is untested. TH-01 (level 12) stands at 5 successes in 10. What do you do with the 90 calls?

- A. Ten more trials of TH-01, to narrow its interval
- B. Ten trials of TH-03: an untested high threat teaches more than a tighter interval on one that already works
- C. Ninety single-call probes of the portal chat, to cover more ground
- D. Keep them in reserve: an unspent budget is the safer report

#### [day1#lab-1-4] Score and choose five

Lab 1.4 · 25 min

Score the ten threats on the national likelihood and impact scale, rank them, and pick five to attack within a budget of 300 model calls.

[D1_4_score_and_choose.ipynb](https://sdaiaacademy.github.io/ae-308/labs/D1_4_score_and_choose.ipynb)

- [ ] Score likelihood and impact with a reason each (8 min)
- [ ] Level and band, then rank (4 min)
- [ ] What ten trials can and cannot show (6 min)
- [ ] Pick five within 300 calls (7 min)
- [ ] ✱ Stretch: Rescore one threat as if email were removed from the agent

#### [day1#wrap-up] Three things to keep

*Day 1 · wrap-up*

- **Assume it is fooled.** The design question is what a fooled model can read and do, never whether it will obey.
- **Entries, actions, exits.** Four origins of outside text, seven actions, four exits. Defences go on flows.
- **A budget names the gaps.** Score with reasons, test five, and write down the high threats you did not test.

#### [day1#next] Day 2: Attack

*Next*

Tomorrow you attack Mukhallis through every entry point of today's table, ten trials at a time. Finish any open lab tonight; each of tomorrow's labs starts from supplied files.
