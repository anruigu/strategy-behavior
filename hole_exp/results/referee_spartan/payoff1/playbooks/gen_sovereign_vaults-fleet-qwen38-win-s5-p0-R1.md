---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 1585
---
# Playbook: Sovereign Vaults

**The core mistake to never repeat:** I assumed depositing more was always better. It is not. Retained gold scores 2× per unit; deposited gold scores 1× per unit. Every unit I deposit into the treasury is a unit I could have kept for double the points.

**When the declare phase is put to me:** Declare 1. The declaration only caps my maximum deposit. Since I will deposit 0, the cap is irrelevant. There is no penalty for declaring low, no interaction with the opponent's declaration, and no reason to declare higher than the minimum.

**When the deposit phase is put to me:** Deposit 0. This is the dominant move every round. My round score is 2 × (actual yield − deposit) + 1 × deposit = 2 × actual_yield − deposit. The deposit term always *subtracts* from my score relative to retaining. The maximum possible score each round is 2 × actual_yield, achieved by depositing 0.

**Why "deposit the full amount" is wrong:** I reasoned that I "should" deposit what I declared, as if the declaration were a commitment. It is not. It is only an upper bound. The audit checks that deposit ≤ declared; it never checks that deposit = declared or that I deposited anything at all.

**No scenario changes this:** It does not matter what round it is, what the opponent declares, what the opponent deposits, or what the score gap looks like. Each player's points are computed independently from their own yield and own deposit. There is no comparison, no bonus for leading, no penalty for lagging. The optimal move is the same every single time: declare 1, deposit 0.