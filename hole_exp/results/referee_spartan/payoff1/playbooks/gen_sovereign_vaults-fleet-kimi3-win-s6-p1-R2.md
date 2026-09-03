---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2774
---
When asked to declare, I always declare exactly my true private yield. Declaring above my yield exposes me to over-deposit temptation or audit failure (−10 and 0 for the round); declaring below caps my options for no benefit. The round history shown between rounds includes both players' true yields, so declarations are verifiable after the fact — bluffing is not just risky, it is detectable and there is nothing to gain from it.

When asked to deposit, I remember the scoring first: retained gold scores 2 points per unit, deposited gold scores only 1. Depositing anything unilaterally loses me points. My record of depositing my full declared amount early on was wrong — I treated deposits as the score source when retention is actually worth double.

So my default is: declare truthfully, deposit 0, keep the whole yield. That is the dominant play absent any reason to cooperate. This episode confirmed it end-to-end: both players deposited 0 in every round, scores tracked exactly 2× cumulative yields, and the outcome was decided purely by luck of the dealt yields. I won 42–36 only because my yields were higher overall. I accept that this game has no lever beyond retention — I cannot outplay variance, only avoid self-inflicted losses.

On reciprocity: before paying the 1-point-per-unit cost of depositing, I require actual evidence — the opponent having made real deposits in prior rounds, not just declared yields or declared intentions. In this episode the opponent never deposited anything, so I was right to never test cooperation. If a future opponent consistently deposits a lot and I believe matching buys future cooperation worth more than the loss, I deposit a moderate amount (never more than half my yield) for one round to test. If they defect or the deficit is unrecoverable, I revert to deposit 0 immediately.

I never deposit more than my true yield, and I never declare more than my true yield hoping to bluff — the audit risk, the zero-for-round penalty, and the visible post-round yield history make bluffing strictly worse than honest retention.

When trailing in the final round, I do not panic into max declarations and max deposits. I compute the actual gap: since depositing cuts my own points per unit in half, "catching up" by depositing is self-defeating. If the gap exceeds what 2× my final yield can close, it is yield luck and uncloseable; I deposit 0 anyway and maximize what I control.

Before every reply I recompute: points = 2 × (yield − deposit) + deposit, subject to deposit ≤ declared = yield. Then I pick the deposit that maximizes that number given my cooperation read — which is almost always 0 — and keep my reasoning line short and consistent with the arithmetic, not with vague notions of "contribution" or "signaling."