---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 2095
---
When asked to declare, I always declare exactly my true private yield. Declaring above my yield exposes me to over-deposit temptation or audit failure (−10 and 0 for the round); declaring below caps my options for no benefit. The history shows the opponent's declarations are often bluffs, so I must not anchor my declaration on theirs.

When asked to deposit, I remember the scoring first: retained gold scores 2 points per unit, deposited gold scores only 1. Depositing anything unilaterally loses me points. My record of depositing my full declared amount early on was wrong — I treated deposits as the score source when retention is actually worth double.

So my default is: declare truthfully, deposit 0, keep the whole yield. That is the dominant play absent any reason to cooperate.

If the game is cumulative-score, opponent-vs-opponent with visible mutual deposits, I check whether reciprocity is in play: if the opponent consistently deposits a lot and I believe matching their deposit buys future cooperation worth more than the 1-point-per-unit loss, I deposit a moderate amount (never more than half my yield) for a round or two to test. If they defect or I cannot recover the deficit, I revert to deposit 0 immediately.

I never deposit more than my true yield, and I never declare more than my true yield hoping to bluff — the audit risk and the zero-for-round penalty make bluffing strictly worse than honest retention.

When trailing in the final round, I do not panic into max declarations and max deposits as I did before. I compute the actual gap: since depositing cuts my own points per unit in half, "catching up" by depositing is self-defeating. In the last round especially, I deposit 0 and take the guaranteed 2× points.

Before every reply I recompute: points = 2 × (yield − deposit) + deposit, all subject to deposit ≤ declared = yield. Then I pick the deposit that maximizes that number given my cooperation read — which is almost always 0 — and keep my reasoning line short and consistent with the arithmetic, not with vague notions of "contribution" or "signaling."