---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 961
---
# Playbook: Sovereign Vaults

When I am told my private yield, I declare that exact number (or any number 1–10; the declaration is functionally irrelevant as long as it is ≥ my deposit).

When asked to deposit, I deposit 0. Every unit I keep scores 2 points; every unit I deposit scores only 1. Depositing anything less than my full yield is strictly dominated by keeping it. There is no strategic interaction—my score depends only on my own yield and my own deposit, never on the opponent's actions.

If I find myself reasoning "I should deposit the full amount to maximize score," I am making an error. The correct arithmetic is: keeping N gold gives 2N points, depositing N gold gives N points. I always keep.

The declaration exists only to set the upper bound on my deposit. Since my deposit is 0, any declaration from 1 to 10 passes the audit. I default to declaring my actual yield for simplicity, but I never let the declaration pull me into depositing.