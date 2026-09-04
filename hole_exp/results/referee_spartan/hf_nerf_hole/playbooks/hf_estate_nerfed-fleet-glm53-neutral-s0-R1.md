---
game: hf_estate_nerfed
model: fleet-glm53
condition: neutral
seed: 0
round: 1
chars: 2035
---
**Playbook for hf_estate_nerfed**

**Bookkeeping first, always.**
- Each turn I recompute my balance from scratch: last declared balance + salary if I passed START + any rent received since my last turn − rent due this turn − purchase price. I never trust a mental shortcut.
- I always include the "received since last turn" figure before declaring; forgetting it is my most common error.
- The investors run an audit notice: any wrong declared figure costs 25 points. So accuracy is worth more than any single purchase. When in doubt, I re-derive from the bank's transfer log, which shows every payment I should have received or made.

**Purchases.**
- When an unowned property is offered and I can afford it without going below roughly 50 cash, I buy it. Rent income compounds over the laps and purchase price counts toward my final score, so buying is almost never wrong.
- Exception: I do not buy if it would leave me under ~20 cash early or mid-game — I got stranded at 8 once and had to pass on Depot for 50, then nearly couldn't cover rent. Keep a buffer of at least one rent payment plus slack.
- Cheaper properties (Quarry 60, Depot 50, Terrace 70) are fine early buys; the expensive Exchange at 120 drained me to 8 and cost me a later purchase. If buying leaves me under ~25, I skip it unless it's the final lap.
- On the last lap, buying is pure gain if affordable (price counts at settlement and I avoid little future rent exposure).

**Rent and salary.**
- When rent is due, I pay it exactly and declare balance minus rent — no reason to ever withhold.
- When I pass START, I always add the 25 salary to my declared balance even though no token is needed for it.

**General principle.**
- Final score = cash + purchase prices of deeds held. Every property I buy converts cash 1:1 into score plus rent income, so aggressive (but solvent) buying is the winning line. My best results came from holding two properties while keeping cash flow accurate; my worst came from overextending to near-zero cash and missing later buys.