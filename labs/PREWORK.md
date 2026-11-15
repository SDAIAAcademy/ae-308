# Pre-work: six hours before Day 1

The course starts from a working agent and from what you learnt in AE-207 and AE-302. The pre-work makes sure both are fresh. AI assistants may be used for the reading; the first threat model on Day 1 is written without one.

| Part | Time | What to do | What to bring |
|---|---|---|---|
| 1 · Set up | 30 min | Follow the quick start of [`README.md`](README.md) and run `00_setup_check.ipynb` to its last line | A setup that prints "Setup complete." |
| 2 · Read the agent | 90 min | Read `mukhallis.py` from `TOOLS` to the end of `Agent.run`. Run `M.Agent(M.World()).run("Clear MSG-0003").show()` and follow every step of the trace in the code | A one-page sketch: the twelve tools, who serves each, which ones change something |
| 3 · Recall | 60 min | From AE-302: private data, untrusted content, an exit path, and what "remove one leg" meant in its Lab 4.3. From AE-207: its first injection log and its register on the national scale | Two sentences on what your AE-302 agent could have leaked, and how |
| 4 · Read | 120 min | The OWASP Top 10 for LLM Applications 2026 and the OWASP Top 10 for Agentic Applications for 2026 (entry names and one paragraph each); the tactics row of MITRE ATLAS; the two sections "Confused Deputy Problem" and "Token Passthrough" of the Model Context Protocol security best practices. Addresses are in the course README under Sources | Three entries you think apply to Mukhallis, each with the tool it concerns |
| 5 · Classify | 60 min | Open `data/importers.csv` and `data/inbox.jsonl`. With the national Data Classification Policy, write the level of each: the importer record, an invoice, a tariff note, the agent's memory, the system prompt | A five-row table: data, level, reason |

On Day 1 a supervised entry check, without AI assistance, asks you to read an unseen architecture diagram of an agent and mark its entry points, private data and exits. The same kind of check closes the course.

All data in this course is synthetic. Do not paste real records, real addresses or real keys into any lab, and run the attack payloads nowhere but here.
