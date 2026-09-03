---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 1354
---
- The scoring is asymmetric: retained gold is worth 2 points per unit, deposited gold only 1. Deposit 0 every round and keep everything in my stash. This held for all 5 rounds and produced +74 points with zero risk.
- The audit only fails on invalid inputs (negative, non-integer, or exceeding my declaration). Depositing less than declared is perfectly legal, so there is no penalty for hoarding.
- When the declare stage is put to me, declare truthfully. The declaration does not score directly; it only caps the deposit, and since I deposit 0 anyway, truthfulness is free. Truthful declarations also cost nothing even if some future rule ties consequences to honesty.
- Do not reason as if there is a trust or retaliation dynamic unless the scoring actually shows one. The opponent's declarations and deposits (they also hoarded throughout) earned them far fewer points; the 2× multiplier on retained gold is the whole game.
- Never deposit more than 0 unless some rule I'm shown actually gives a bonus for treasury deposits or a penalty for low treasury. If such a bonus appears, compare it to the 2× value of retained gold before deciding.
- If a new episode introduces round-to-round carryover of stash or treasury, re-read the scoring carefully before assuming the same strategy; but on the base rules, declare truthfully and deposit 0 every time.