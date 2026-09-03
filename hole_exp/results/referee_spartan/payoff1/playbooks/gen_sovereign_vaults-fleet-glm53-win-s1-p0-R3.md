---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 1648
---
- The scoring is asymmetric: retained gold is worth 2 points per unit, deposited gold only 1. Deposit 0 every round and keep everything in my stash. This held for all 5 rounds again and produced +40 points with zero risk.
- The audit only fails on invalid inputs (negative, non-integer, or exceeding my declaration). Depositing less than declared is perfectly legal, so there is no penalty for hoarding.
- Declare truthfully every round. The declaration does not score directly; it only caps the deposit, and since I deposit 0 anyway, truthfulness is free. The opponent under-declared in two rounds (4→1, 5→1) and gained nothing from it, which confirms honesty costs nothing here.
- Do not reason as if there is a trust or retaliation dynamic unless the scoring actually shows one. In this episode the opponent deposited small amounts in round 1 and then 0 thereafter; neither behavior changed my payoffs. The 2× multiplier on retained gold is the whole game.
- Never deposit more than 0 unless some rule I'm shown actually gives a bonus for treasury deposits or a penalty for low treasury. If such a bonus appears, compare it to the 2× value of retained gold before deciding.
- Variance comes only from the private yield draws, not from my strategy — my final score is simply 2× the sum of my yields. Play the same regardless of round number or current standings; there is no endgame effect.
- If a new episode introduces round-to-round carryover of stash or treasury, or any penalty tied to total treasury levels, re-read the scoring carefully before assuming the same strategy; but on the base rules, declare truthfully and deposit 0 every time.