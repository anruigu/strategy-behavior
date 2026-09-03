---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 1056
---
# Playbook: Sovereign Vaults

When the declare phase is put to me, I declare my true yield. The declaration only sets the cap on my deposit; it has no direct effect on scoring. Any integer from 1 to 10 that is ≥ my deposit passes audit, so declaring truthfully is the simplest safe choice.

When the deposit phase is put to me, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit. My total per round is 2×(yield − deposit) + 1×deposit = 2×yield − deposit, so depositing 0 is always strictly better than depositing anything more. There is no competitive reason to deposit: the treasury score is not a zero-sum pool and the opponent's deposits do not affect my points.

Warning from a prior run: I once reasoned that depositing more would "boost" my score and deposited the full declared amount every round, finishing at roughly half what depositing 0 would have earned. The arithmetic is unambiguous — every unit deposited is a net loss of 1 point relative to retaining it. Never deposit unless the rules change.