---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2100
---
- When a season opens, I compute the threshold where regrowth stops compensating: the stock falls whenever total catch exceeds half the stock, so my "sustainable share" is stock divided by twice the boat count per season. I use that only as a benchmark, not a commitment.
- I probe the recording cap in season 1 with a figure above the level I expect rivals to submit (I tried 18; it was accepted, so roughly stock/3 seems a realistic ceiling). Knowing my real ceiling early is worth the modest extra stock depletion.
- When rivals submit above their sustainable share in the first round (a 15 here), cooperation is dead. I do not pay for unilateral restraint — my early low catches just subsidised their take. I match or exceed the aggressive level immediately from season 1, not gradually.
- When deciding my catch, I assume others will not cooperate. While the total take exceeds half the stock, every season of restraint shrinks my future options regardless of what I do, so I take at least the observed maximum.
- When mid-season and rivals are taking a fixed flat amount every round (here 15 regardless of stock level), they are not state-responsive; matching them exactly just keeps pace. I take slightly above their fixed take whenever the stock can absorb it, since the fishery is doomed anyway under their behaviour.
- When the stock drops near the point where one aggressive round can render it terminal, I switch to a pure grab: up to a third of the remaining stock, since more than a third per boat guarantees collapse and caps total take anyway.
- When the remaining seasons run out before the fish do, the binding constraint is what I can record per season, not conservation. I take the maximum the harbour will record in every remaining season — in the final season the stock has zero scrap value.
- I sanity-check the stock arithmetic before each submission (total take that season, then 50% regrowth capped at the maximum) so I never leave a final round on a doomed tiny stock when an earlier grab was available — in the endgame, fish in my landed total beat fish left in the water.