---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1265
---
**Playbook: gen_sovereign_vaults**

When I am shown my private yield in the declare phase, I declare exactly that number. This passes the audit and gives me the maximum allowed deposit cap.

When I am asked to deposit, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores 1 point per unit. There is no stated benefit to the treasury that rewards me, so every unit I deposit costs me 1 point relative to retaining it. The only reason to deposit anything is if I have a specific game-theoretic reason to believe it affects my opponent's position — and no such mechanism is stated in the rules.

The one failure to avoid: I may correctly reason that depositing 0 is optimal in the declare phase and then contradict myself in the deposit phase by depositing the full amount. My reasoning and my action must match. If I have concluded that retaining is worth double, I deposit 0. No amount of "the pattern is to deposit everything" or "I should be consistent with prior rounds" overrides the arithmetic.

If I observe my opponent consistently depositing more than 0, I do not follow suit unless a rule emerges that ties treasury contents to a shared or comparative score. Based on the rules as written, their deposits do not change my optimal play.