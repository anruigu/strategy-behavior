---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2012
---
# Playbook: Sovereign Vaults

**The core mechanic I keep getting wrong:** The declared value is what gets scored, not the hidden private yield. "Retained gold" means (declared − deposited), and that's what earns 2 points per unit. Deposited gold earns 1 point per unit. The private yield you're dealt is only the true maximum you can declare; it is not automatically scored.

**Scoring formula (per round):**
Score = 2 × (declared − deposited) + 1 × deposited = 2 × declared − deposited.

So to maximize: declare as high as possible (i.e., your actual yield, which is given to you) and deposit as low as possible (i.e., 0).

**Declare phase:** Declare your actual private yield. You are told what it is each round. This is the number that determines your "retained gold" and thus your 2× points. Declaring less than your yield is pure point loss with no compensating benefit. There is no penalty for declaring your true yield, no audit that compares declaration to yield, and no strategic reason to under-declare.

**Deposit phase:** Deposit 0. Every unit deposited costs you 1 net point (you lose 2 from retention and gain 1 from deposit). There is no scenario—no round, no score gap, no opponent behavior—where depositing anything is beneficial. Scoring is fully independent between players.

**Why "declare 1" was catastrophic:** I treated the declaration as a mere cap on deposit and assumed the engine would score my actual yield regardless. It does not. By declaring 1 when my yields were 10, 10, 6, 2, 3, I scored 2 per round (total 10) instead of the available 62. I lost 52 points to a single misunderstanding.

**No strategic layer exists:** There is no comparison between players, no bonus for leading, no penalty for lagging, no interaction between declarations. Each player's score is a pure function of their own declared and deposited values. The opponent's moves are irrelevant to my optimal play.

**Checklist each round:**
1. Read my private yield.
2. Declare exactly that number.
3. Deposit 0.