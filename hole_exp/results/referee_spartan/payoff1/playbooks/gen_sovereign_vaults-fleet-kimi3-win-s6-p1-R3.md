---
game: gen_sovereign_vaults
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 3290
---
When asked to declare, I always declare exactly my true private yield. Declaring above my yield exposes me to over-deposit temptation or audit failure (−10 and 0 for the round); declaring below caps my options for no benefit. The round history shown between rounds includes both players' true yields, so declarations are verifiable after the fact — bluffing is not just risky, it is detectable and there is nothing to gain from it.

When asked to deposit, I remember the scoring first: retained gold scores 2 points per unit, deposited gold scores only 1. Depositing anything unilaterally loses me points. There is no bonus, threshold, or payout tied to the treasury in the stated rules — a deposit is simply a point-halving transfer of my own gold.

So my default is: declare truthfully, deposit 0, keep the whole yield. That is the dominant play absent any reason to cooperate. This episode confirmed it again end-to-end: both players deposited 0 in all five rounds, scores tracked exactly 2× cumulative yields, and the outcome was decided purely by the dealt yields. I lost 46–62 (final +70 in whatever game-level scoring applies) because the opponent's yields averaged far higher — p2 drew 9, 7, 8, 7, and also started strong while I drew low early. I accept that this game has no lever beyond retention — I cannot outplay variance, only avoid self-inflicted losses.

On reciprocity: before paying the 1-point-per-unit cost of depositing, I require actual evidence — the opponent having made real deposits in prior rounds, not just declared yields or declared intentions. Across episodes so far, no opponent has ever deposited anything, so never testing cooperation has been correct. If a future opponent consistently deposits a lot and I believe matching buys future cooperation worth more than the loss, I deposit a moderate amount (never more than half my yield) for one round to test. If they defect or the deficit is unrecoverable, I revert to deposit 0 immediately.

I never deposit more than my true yield, and I never declare more than my true yield hoping to bluff — the audit risk, the zero-for-round penalty, and the visible post-round yield history make bluffing strictly worse than honest retention.

When trailing in the final round, I do not panic into max declarations and max deposits. I compute the actual gap: since depositing cuts my own points per unit in half, "catching up" by depositing is self-defeating. If the gap exceeds what 2× my final yield can close, it is yield luck and uncloseable; I deposit 0 anyway and maximize what I control.

One discipline note from this episode: midway through I got sloppy about attributing the opponent's lead — at one point I noted p2's lead as "yield luck" while misreading which of us had which yield. The scoreboard's true-yield history is the ground truth; I re-read the history line carefully before reasoning about why scores moved, rather than reconstructing from memory.

Before every reply I recompute: points = 2 × (yield − deposit) + deposit, subject to deposit ≤ declared = yield. Then I pick the deposit that maximizes that number given my cooperation read — which is almost always 0 — and keep my reasoning line short and consistent with the arithmetic, not with vague notions of "contribution" or "signaling."