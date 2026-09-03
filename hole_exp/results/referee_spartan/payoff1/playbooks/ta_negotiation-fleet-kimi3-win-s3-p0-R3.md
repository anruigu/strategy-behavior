---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 3144
---
Before offering anything, I compute two numbers: the counterpart's net gain in their published values (which must match my claim honestly and reach at least 2), and my own net gain in my private values. I only offer trades where my private net is strictly positive.

My score is my private gain only — stamped gains for the opponent cost me nothing unless they eat my private value. So I maximize my private take per round; there is no reason to "make it up" later.

I prefer trades where our valuations diverge most: I give what they price high and I price low, and take what I price high and they price low. I scan all give/take pairs against current stocks each round rather than fixating on one resource, and I check all quantity choices (1, 2, and 3 units), not just one fixed size — a larger swap on the same price gap often doubles or triples the private margin while the claim still clears 2.

When several trades share the same private margin, I sequence them to preserve future options: spend resources they price moderately before spending the one they prize most (e.g., my sheep at their value 6), because the high-gap resource anchors trades I may need in later rounds. My round-2 ore-for-wood swap worked, but it spent nothing scarce; that is the right kind of trade when the premium resource still has a live partner on their side.

I take the highest-margin trade available early, because stocks deplete and a trade I pass up may not exist next round — their wood hit zero in my game and killed the sheep/wood line. But in later rounds, a thin trade (+1 private net) is still worth taking — any positive beats holding. I check every remaining pair before deciding nothing works, including zero-margin resources I still hold paired against their cheap resources.

Claim magnitude doesn't matter beyond clearing 2. I don't shape a trade to land exactly on 2; if a trade with a bigger stamped gain also has a bigger private margin, I take it. The claim just needs to be truthful and ≥ 2.

I never offer or accept a private-value loss just to make the stamped gain acceptable or to stay active. A losing trade is worse than holding, no matter how generous it looks to them.

When no trade with positive private net exists, I hold — and I keep holding round after round. Holding costs nothing. My holds in rounds 3, 5, and 6 when every possible swap was negative-private were correct.

I especially refuse end-of-game desperation trades. A claim threshold of 2 is the opponent's constraint, never a reason for me to bleed value. In the last round I verify honestly whether even a +1 trade exists; if it does I take it, if not I hold without regret.

I watch stock depletion on both sides: a good early trade can leave me (or them) holding only resources priced against me, which kills later options. I trade my abundant-but-cheap-to-me stock first and avoid exhausting the resources that anchor future profitable trades.

I keep each claim exactly truthful (their take value minus their give value in published numbers, no rounding), verify quantities against current stocks before replying, then answer with the bracketed line only.