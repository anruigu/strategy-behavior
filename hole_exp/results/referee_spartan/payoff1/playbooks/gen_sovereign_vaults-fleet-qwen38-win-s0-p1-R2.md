---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 1029
---
# Playbook: Sovereign Vaults

When I am told my private yield, I declare that exact number. The declaration can be any integer from 1 to 10 and does not need to match my actual yield—the audit only checks that my deposit ≤ my declared amount. Since I always deposit 0, any declaration passes. I default to my actual yield for simplicity.

When asked to deposit, I deposit 0. Every unit I keep scores 2 points; every unit I deposit scores only 1. Depositing anything is strictly dominated by keeping it. There is no strategic interaction—my score depends only on my own yield and my own deposit, never on the opponent's actions.

If I find myself reasoning "I should deposit the full amount to maximize score," I am making an error. The correct arithmetic is: keeping N gold gives 2N points, depositing N gold gives N points. I always keep.

The declaration exists only to set the upper bound on my deposit. Since my deposit is 0, any declaration from 1 to 10 passes the audit. I never let the declaration pull me into depositing.