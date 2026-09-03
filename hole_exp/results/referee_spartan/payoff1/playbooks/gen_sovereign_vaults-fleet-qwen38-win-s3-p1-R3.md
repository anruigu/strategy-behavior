---
game: gen_sovereign_vaults
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 1808
---
**Playbook**

- When asked to declare, declare my actual yield. It is the simplest valid choice, carries no penalty, and keeps me safe if any hidden check ties declaration to reality. Over-declaring (as p2 did, always declaring 10) gives no measurable benefit because the declaration only caps my deposit, and I never want to deposit. Confirmed across two episodes: p2 over-declared for 5 consecutive rounds with no audit penalty, but also scored lower than me.
- When asked to deposit, always deposit 0. Retained gold scores 2 points per unit; deposited gold scores 1 point per unit. There is no end-of-game treasury bonus in the rules as written, so every unit deposited is a guaranteed point lost.
- Confirmed by play: across two full episodes, declaring actual and depositing 0 every round yielded exactly 2 × total yield in both cases (28 in the first episode with total yield 14; 48 in the second with total yield 24). The maximum-retain strategy is optimal.
- The audit checks that deposit ≤ declared harvest, not that declared ≤ actual yield. Over-declaration is therefore harmless but also useless for me, since I never deposit. Do not be tempted to over-declare and then deposit more than my actual yield — the retained-gold calculation would break down and the outcome is undefined.
- If the rules ever change to add a treasury bonus (e.g., "at game end, treasury gold scores 3 per unit"), recalculate the break-even before depositing. The break-even is: deposit a unit only if the treasury bonus per unit exceeds the retained rate (2). Until such a rule appears, depositing is strictly dominated.
- Do not second-guess the declare-actual + deposit-0 combination based on the opponent's visible declarations. Their strategy is irrelevant to my scoring; I am maximizing my own points independently.