---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1029
---
# Playbook: Sovereign Vaults

When the declare phase is put to me, I declare my true yield. The declaration only sets the cap on my deposit; it has no direct effect on scoring.

When the deposit phase is put to me, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores only 1 point per unit. Every unit I deposit instead of retain costs me 1 point. My total per round is 2×(yield − deposit) + 1×deposit = 2×yield − deposit, so depositing 0 is always strictly better than depositing anything more.

I made a critical error in my previous run: I reasoned that "maximizing my deposit" would boost my score, when in fact it was halving my score. I deposited the full declared amount every round and finished at 29 when depositing 0 every round would have yielded roughly double.

The declaration is a free choice as long as it is an integer from 1 to 10 and at least as large as my deposit. Since I always deposit 0, any declaration from 1 to 10 passes audit. Declaring my true yield is the simplest safe choice.