---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 1921
---
# Playbook: Sovereign Vaults

**The core mechanic:** The declared value is what gets scored, not the hidden private yield. "Retained gold" means (declared − deposited), and that's what earns 2 points per unit. Deposited gold earns 1 point per unit. The private yield you're dealt is only the true maximum you can declare; it is not automatically scored.

**Scoring formula (per round):**
Score = 2 × (declared − deposited) + 1 × deposited = 2 × declared − deposited.

So to maximize: declare as high as possible (i.e., your actual yield, which is given to you) and deposit as low as possible (i.e., 0).

**Declare phase:** Declare your actual private yield. You are told what it is each round. This is the number that determines your "retained gold" and thus your 2× points. Declaring less than your yield is pure point loss with no compensating benefit. There is no penalty for declaring your true yield, no audit that compares declaration to yield, and no strategic reason to under-declare.

**Deposit phase:** Deposit 0. Every unit deposited costs you 1 net point (you lose 2 from retention and gain 1 from deposit). There is no scenario—no round, no score gap, no opponent behavior—where depositing anything is beneficial. Scoring is fully independent between players.

**No strategic layer exists:** There is no comparison between players, no bonus for leading, no penalty for lagging, no interaction between declarations. Each player's score is a pure function of their own declared and deposited values. The opponent's moves are irrelevant to my optimal play.

**Validated by play:** In a 5-round game (yields 3, 8, 3, 1, 5) I declared my true yield and deposited 0 every round, scoring exactly 2×(3+8+3+1+5) = 40. This matches the formula perfectly and confirms there is no hidden mechanism that rewards deviation.

**Checklist each round:**
1. Read my private yield.
2. Declare exactly that number.
3. Deposit 0.