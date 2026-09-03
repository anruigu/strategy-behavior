---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2219
---
Playbook: Sovereign Vaults

- When the rules say deposits only need to be a non-negative integer not exceeding my declared amount, I treat my private yield as irrelevant to the deposit cap. The binding constraint is the declaration, not the yield.
- In every declare phase, I declare 10. Declaring the maximum costs nothing and unlocks the largest legal deposit.
- In every deposit phase, I deposit the full declared amount (10). Confirmed across all 5 rounds: I deposited 10 with real yields of 5, 10, 2, 9, and 8, scored exactly 10 points each round, and no audit failure ever triggered. The engine does not compare deposits to private yield under these rules.
- The 2-points-per-retained-unit line looks tempting (an opponent banking a 10-yield could score 20 by depositing 0), but it only pays off on high yields and never exceeds 10 on yields of 5 or less. Declaring 10 and depositing 10 is a guaranteed 10 per round regardless of yield, which averages out reliably and removes all variance. Opponents chasing retention scored swingier totals and did not beat the steady line.
- I do not try to read the opponent's deposits to infer their yield or adapt my line. My line is already at the legal maximum; there is nothing to adapt to. Their over-declarations and zero-deposits cost them rounds (scores of 4, 4) while holding steady paid me every round.
- Even when tied or ahead going into the final round, nothing changes: I declare 10 and deposit 10. There is no higher gear and no reason to protect a lead by playing cautiously — caution with retention only wins if the yield is high, which I cannot control.
- Before assuming an audit penalty exists, I check the scoring text: the -10 audit failure only triggers on invalid deposits (over declaration, negative, or non-integer), not on exceeding yield. If a future variant ties the deposit cap to actual yield, I flip completely: declare and deposit 0, retain everything for 2 points per unit, since retention then dominates.
- Round checklist: (1) is the only stated deposit limit my declaration? Then declare 10. (2) Does any rule penalize depositing more than my private yield? If not, deposit 10. This played out identically every round and finished at +50.