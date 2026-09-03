---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1615
---
**Playbook for gen_sovereign_vaults**

- The scoring I observed: retained gold scores 2/unit but ONLY up to my declared amount — gold retained above my declaration earned nothing (I kept 9 gold after declaring 1 and scored only 2). Deposits score a flat 1/unit. So the payoff-maximizing line is: **declare my true yield, deposit 0**. That yields 2 × yield per round with no audit risk.

- When the declare stage is put to me, I declare my actual private yield. Underdeclaring is the trap: it doesn't let me secretly keep more (undeclared retained gold scores zero), it just caps my retained-gold scoring. Overdeclaring is pointless since I'd just have to deposit at 1× or fail the audit.

- When the deposit stage is put to me, I deposit 0 whenever I declared truthfully — retained gold beats deposits 2:1 and deposits appear to help the shared/opponent pool more than me. Only deposit if some revealed rule (a multiplier, a bonus threshold, a shared-pool payoff I can actually verify from the scoreboard deltas) makes a deposit worth more than 2/unit to me.

- Track the scoreboard deltas each round to verify the scoring rule. If I ever see retained gold scoring above 2/unit or deposits scoring above 1/unit, adjust; but never assume a shared pool is generous without evidence — in my play the opponent pulled ahead by depositing while I gave up points by capping myself with low declarations.

- Never declare below my yield "for safety" — there is no penalty for a truthful declaration, only for a deposit exceeding it. The only real audit risk is overdeclaring and then being unable to cover a forced deposit.