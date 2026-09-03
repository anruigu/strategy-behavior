---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 1874
---
**Playbook: gen_sovereign_vaults**

When I am shown my private yield in the declare phase, I declare exactly that number. This passes the audit and gives me the maximum allowed deposit cap. I always use the explicitly stated "Your private yield is X" value, not any number I might infer from a round summary (the summary format for yields can be ambiguous about which player is which).

When I am asked to deposit, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores 1 point per unit. There is no stated benefit to the treasury that rewards me, so every unit I deposit costs me 1 point relative to retaining it. The only reason to deposit anything is if a rule ties treasury contents to a shared or comparative score. Under the current rules, no such mechanism exists.

This game is purely individual. What the opponent declares or deposits does not change my optimal play. I confirmed in my first full episode that both players can independently maximize by declaring truthfully and depositing 0, and the final score is simply 2 × (sum of my yields). There is no hidden incentive, no comparative bonus, no penalty for an empty treasury.

The one failure to avoid: I may correctly reason that depositing 0 is optimal and then contradict myself in the deposit phase by depositing the full amount. My reasoning and my action must match. If I have concluded that retaining is worth double, I deposit 0. No amount of "the pattern is to deposit everything" or "I should be consistent with prior rounds" overrides the arithmetic.

If a future variant introduces a rule that ties treasury contents to scoring (e.g., a bonus for the player who deposited more, a shared pot, a multiplier on treasury contents), I will re-evaluate. But under the current rules, the dominant strategy is trivially "declare truthfully, deposit 0" and I should not second-guess it.