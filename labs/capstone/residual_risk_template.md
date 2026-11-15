# Residual-risk statement: Mukhallis, team <name>

For Siham Al-Nuwaiser, director of clearance services, who accepts or refuses the risk.

## 1. What we claim

- Every exfiltration path in our attack log fails on this build, over <n> trials each, and <x>% of the 50 benign tasks pass.
- Which claims are exact (a deterministic control: name it) and which are rates (a guardrail or a model's behaviour: give the interval).

## 2. What the other team found, and what we did

| Finding | Confirmed? | Fix | Regression test | Before | After |
|---|---|---|---|---|---|

## 3. What remains

| Risk | Why it remains | Likelihood | Impact | Level and band | Treatment (avoid, mitigate, transfer, accept) | Owner |
|---|---|---|---|---|---|---|

Include what the design costs users: legitimate requests the guardrail blocks, by language; free-text requests the split drops; tasks that wait for an approval.

## 4. What would change this statement

A model change, a new tool, a new server, a new language of traffic. The suite to re-run and who runs it.
