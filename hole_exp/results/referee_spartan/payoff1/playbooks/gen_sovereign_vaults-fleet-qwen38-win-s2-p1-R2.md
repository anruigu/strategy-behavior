---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 1561
---
**Playbook: gen_sovereign_vaults**

When I am shown my private yield in the declare phase, I declare exactly that number. This passes the audit and gives me the maximum allowed deposit cap.

When I am asked to deposit, I deposit 0. Retained gold scores 2 points per unit; deposited gold scores 1 point per unit. There is no stated benefit to the treasury that rewards me, so every unit I deposit costs me 1 point relative to retaining it. The only reason to deposit anything is if a rule ties treasury contents to a shared or comparative score. Based on the rules as written, no such mechanism exists.

This game has no strategic depth beyond the audit constraint. The dominant strategy is trivially "declare truthfully, deposit 0." I should not second-guess this arithmetic or look for hidden incentives that aren't in the rules. My score in a 5-round game with all-retain play is simply 2 × (sum of my yields).

The one failure to avoid: I may correctly reason that depositing 0 is optimal and then contradict myself in the deposit phase by depositing the full amount. My reasoning and my action must match. If I have concluded that retaining is worth double, I deposit 0. No amount of "the pattern is to deposit everything" or "I should be consistent with prior rounds" overrides the arithmetic.

If a future variant of this game introduces a rule that ties treasury contents to scoring (e.g., a bonus for the player who deposited more, or a shared pot), I will re-evaluate. But under the current rules, the opponent's deposits do not change my optimal play.