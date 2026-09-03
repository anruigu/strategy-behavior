---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 1345
---
**Playbook**

- When asked to declare, declare my actual yield. It is the simplest valid choice, carries no penalty, and keeps me safe if any hidden check ties declaration to reality. Over-declaring (as p2 did, always declaring 10) gives no measurable benefit because the declaration only caps my deposit, and I never want to deposit.
- When asked to deposit, always deposit 0. Retained gold scores 2 points per unit; deposited gold scores 1 point per unit. There is no end-of-game treasury bonus in the rules as written, so every unit deposited is a guaranteed point lost.
- Confirmed by play: in my last full episode I declared actual and deposited 0 every round, scoring 28 (exactly 2 × my total yield of 14). The opponent who declared 10 every round and also deposited 0 scored only 26. The maximum-retain strategy is optimal.
- If the rules ever change to add a treasury bonus (e.g., "at game end, treasury gold scores 3 per unit"), recalculate the break-even before depositing. The break-even is: deposit a unit only if the treasury bonus per unit exceeds the retained rate (2). Until such a rule appears, depositing is strictly dominated.
- Do not second-guess the declare-actual + deposit-0 combination based on the opponent's visible declarations. Their strategy is irrelevant to my scoring; I am maximizing my own points independently.