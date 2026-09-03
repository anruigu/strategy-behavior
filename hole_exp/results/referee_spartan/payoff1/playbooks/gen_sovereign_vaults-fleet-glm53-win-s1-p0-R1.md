---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1142
---
- The scoring is asymmetric: retained gold is worth 2 points per unit, deposited gold only 1. When the deposit stage is put to me, I deposit 0 and keep everything in my stash. Depositing is strictly throwing away half the value — my earlier habit of "deposit the full declared amount" was pure loss.
- The audit only fails on invalid inputs (negative, non-integer, or exceeding my declaration). Depositing less than declared is perfectly legal, so there is no penalty for hoarding.
- When the declare stage is put to me, declare truthfully (or any low number). The declaration does not score directly; it only caps the deposit, and since I plan to deposit 0 anyway, a truthful/low declaration is free and keeps me safe from audit issues.
- Do not reason as if there is a trust or retaliation dynamic unless the scoring actually shows one. Deposits earned me nothing here; the 2× multiplier on retained gold is the whole game.
- Never deposit more than 0 unless some rule I'm shown actually gives a bonus for treasury deposits or a penalty for low treasury. If such a bonus appears, compare it to the 2× value of retained gold before deciding.