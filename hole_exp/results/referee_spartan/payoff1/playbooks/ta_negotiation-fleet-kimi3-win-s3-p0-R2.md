---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2189
---
Before offering anything, I compute two numbers: the counterpart's net gain in their published values (which must match my claim honestly and reach at least 2), and my own net gain in my private values. I only offer trades where my private net is strictly positive.

My score is my private gain only — stamped gains for the opponent cost me nothing unless they eat my private value. So I maximize my private take per round; there is no reason to "make it up" later.

I prefer trades where our valuations diverge most: I give what they price high and I price low, and take what I price high and they price low. I scan all give/take pairs against current stocks each round rather than fixating on one resource.

I take the highest-margin trade available first, because stocks deplete and a trade I pass up may not exist next round. But in later rounds, a thin trade (+1 private net) is still worth taking — any positive beats holding. I check every remaining pair before deciding nothing works, including zero-margin resources I still hold paired against their cheap resources.

I never offer or accept a private-value loss just to make the stamped gain acceptable or to stay active. A losing trade is worse than holding, no matter how generous it looks to them.

When no trade with positive private net exists, I hold — and I keep holding round after round. Holding costs nothing. My final-round hold when every possible swap was negative-private was correct.

I especially refuse end-of-game desperation trades. A claim threshold of 2 is the opponent's constraint, never a reason for me to bleed value. In the last round I verify honestly whether even a +1 trade exists; if it does I take it, if not I hold without regret.

I watch stock depletion: a good early trade can leave me holding only resources they price high, which kills later options. I trade my abundant-but-cheap-to-me stock first and avoid exhausting the resources that anchor future profitable trades.

I keep each claim exactly truthful (compute their take value minus their give value in published numbers, no rounding), verify quantities against current stocks before replying, then answer with the bracketed line only.