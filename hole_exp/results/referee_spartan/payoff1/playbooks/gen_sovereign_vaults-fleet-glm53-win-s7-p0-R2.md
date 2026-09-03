---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 1477
---
**Playbook for gen_sovereign_vaults**

- The scoring rule as played: retained gold scores 2/unit (up to declaration), deposits score 1/unit, audit failure loses 10 and zeroes the round. Confirmed across all 5 rounds: declaring truthfully and depositing 0 scored exactly 2 × yield each round (20, 8, 16, 20, 20 = 84 total). This is the optimal line.

- At the declare stage: declare my true private yield. Underdeclaring caps retained-gold scoring at the declared amount; overdeclaring risks an audit failure if a deposit is forced. Truthful declaration has no downside.

- At the deposit stage: deposit 0 whenever I declared truthfully. Retained gold beats deposits 2:1. Deposits appear to only feed a shared/opponent pool — my opponent who declared 1 and deposited 0 scored 2/round vs my 2×yield, so giving up deposits costs me nothing competitively.

- Track the scoreboard deltas each round to verify the scoring rule holds. If retained gold ever scores above 2/unit or deposits above 1/unit, or a deposit threshold/multiplier appears, adjust. But don't assume a shared pool is generous without evidence in the deltas.

- Never declare below my yield "for safety" — the only real audit risk is a deposit exceeding the declaration, and I control that by depositing 0. There is no penalty for truthful declaration.

- If the opponent deposits heavily and I see shared-pool payoffs exceeding my retained 2/unit, reconsider; otherwise the declare-true, deposit-0 line dominates.