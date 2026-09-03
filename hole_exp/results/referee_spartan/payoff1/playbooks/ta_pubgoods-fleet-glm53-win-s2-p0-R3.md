---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 4255
---
When the envelope prompt is put to me, I contribute 0. Each token I put in returns only my 1/n share of the multiplier, which is 0.4 here — below 1 — so keeping is strictly dominant regardless of what others do. This worked exactly as predicted: opponents contributed fully in round 1 and my defection produced a 20-point lead immediately. I do not let others' contributions tempt me into reciprocity; their generosity just pays me.

When others contribute fully in round one, I keep defecting in round two. They retaliated by defecting thereafter, which cost them but never overtook me — the one-round exploitation of full contributors is what built my lead, and I should not feel pressure to repair it. Confirmed: the all-defect equilibrium after round 2 left everyone at +20 per round, and my round-1 lead (+20 over each opponent) persisted to the end and won, +124 to +84.

Once others have all defected for consecutive rounds, contributing would only transfer points to them, so I keep contributing 0 through the final round. I never "invest" late to seed cooperation; with a known, short horizon it cannot pay back. Confirmed over rounds 2–5: everyone stayed at 0 and my lead never shrank.

The margin math is worth remembering when deciding whether a lead is safe: if I defect while others defect too, all totals rise equally, so a lead is locked in once everyone has stopped contributing. My only exposure was if others had contributed while I defected — which grows my lead, not theirs. So a lead built in round 1 is safe as long as I never start contributing. One corollary confirmed this run: the final margin equals the round-1 lead exactly, because after round 1 everyone's totals moved in lockstep. If I ever see my lead shrinking, it means someone is contributing while I am not — which is fine — or that I have started contributing, which is the mistake.

One check to run each round before sealing: confirm from the published receipts whether anyone is still contributing. If an opponent contributes while I defect, my lead grows; if all defect, totals move in lockstep. Either way 0 is correct — but the receipts tell me whether the game state is what I expect, and a surprise (e.g. someone overdeclaring, or a pot exceeding the sum of receipts) would signal a rules wrinkle worth noticing before I commit. This check cost nothing each round and confirmed the all-defect state as expected every time from round 2 on.

When the receipt slip is put to me, I declare the exact envelope amount. The rules require the receipt to match, and any gain from misdeclaring would go into a shared pot I only see 1/n of anyway — understating saves me nothing (my kept tokens are already mine) and overdeclaring risks a referee penalty for a 0.4-per-token return. Five honest receipts of 0 caused no trouble across the whole game. Since I always contribute 0, this rule reduces in practice to "[declare: 0]" every round — but keep the honest-declaration principle for any variant where I do contribute, in case over- or underdeclaring is ever strategically tempting.

General pattern worth keeping: in any public-goods-style game where the per-capita return on a contributed token is less than 1, I defect every round and file honest receipts. This produced a clean win (+124 vs +84). If the multiplier is high enough that my share of my own token exceeds 1, contributing fully becomes dominant instead — recompute that threshold each time the parameters are announced, and also recompute it whenever the group size or endowment changes. What did not work and must not be tried: contributing to signal or to sustain cooperation in a fixed-length game; the collapse came anyway and I kept my lead only because I stayed out of it.

Expect the common opponent pattern — full contribution in round 1, then permanent defection — and do not second-guess it. The strategy is settled for this parameter set: 0 every round, honest receipts, executed without re-litigating each round. The only rounds that need real thought are the first (recompute the per-capita return from the announced multiplier and group size) and any round where the published receipts deviate from what I expect — that is the signal to slow down and re-read the rules before committing.