---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2187
---
In the final season, I always submit a catch equal to the entire remaining stock — there is no tomorrow, so leaving anything in the water is points thrown away.

In the second-to-last season, I take as much as I can land too, not just a third. Restraint in season 5 (catching only 3.5 of 10.4) was a pure loss: rivals grabbed everything and the regrowth after a near-empty stock is trivial. Once the endgame arrives, every season is effectively the last.

The pivot to hard extraction comes earlier than I used to think. If rivals exceed the sustainable share two seasons in a row — especially if anyone opens well above it in season 1 — the commons is already lost and I stop conserving immediately. Season 1 overfishing by boat 1 (18 vs 11.1) was the tell; I kept sustaining through season 3 and that caution cost me. One season of restraint to gather information is the maximum I spend; I do not wait for three confirmations.

In the very first season, with no information, I take roughly the sustainable share — cooperation is worth one trial. But if anyone defects in season 1, I match or exceed defection in season 2.

I compute the decision numerically each season: compare what my restraint adds via 50% regrowth over remaining seasons (only one-third of the regrowth comes to me, since three boats share it) against what I can grab now. Since rivals take most of any regrowth I preserve, conservation pays me only a third of its value — so I only conserve when I have strong evidence rivals will conserve too.

When I defect, I defect fully — I take my maximum landable share (roughly stock divided by number of boats, or more if rivals can't take it all), not a timid +1 above sustainable. Half-measures like 12 when sustainable is 5.7 get neither the cooperation payoff nor the grab payoff.

I track every rival's landings each season and update the cooperation/defection decision immediately, treating it as a rule, not a feeling.

If collapse is mathematically inevitable whatever I do, I take the maximum share every remaining season.

I keep every reply brief, always end with the exact [catch: N] token, and never leave the endgame catch below the full amount I can land.