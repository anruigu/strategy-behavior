---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 2473
---
- Before anything else: my reply must end with the clean `[catch: N]` token and nothing else — no tool-call scaffolding, no stray markup. A malformed submission risks a lost or misrecorded season, which is worse than any strategic error.
- When a season opens, I compute the threshold where regrowth stops compensating: the stock falls whenever total catch exceeds half the stock, so my "sustainable share" is stock divided by twice the boat count per season. I use that only as a benchmark, not a commitment.
- I probe the recording cap in season 1 with a figure above the level I expect rivals to submit (I tried 18 of 100; it was accepted, so roughly stock/3 seems a realistic ceiling). Knowing my real ceiling early is worth the modest extra stock depletion.
- When rivals submit above their sustainable share in the first round, cooperation is dead. I do not pay for unilateral restraint — early low catches just subsidise their take. I take aggressively from season 1, not gradually.
- When rivals take a fixed flat amount every round regardless of stock level (here ~14–15 at every stock from 100 down to 62), they are not state-responsive and will not slow down even as collapse looms. Doomsday arrives faster than intuition suggests — here the stock went 100 → 85 → 62 → 18 in three seasons. I must take my ceiling from the start, because there will be no "later, when it matters".
- With flat-takers near the cap, the collapse point arrives when stock ≈ (their flat take × other boats) × 2. I track this two seasons ahead: the last season where the stock still supports a full-cap take is my last chance, and I use it fully.
- When the stock drops to the point where one aggressive round renders it terminal, I submit the maximum the harbour will record (up to a third of the stock, or the known cap), even if total submitted take exceeds the stock — my recorded take cannot be hurt by submitting high, and proration can only punish submitting low.
- When the remaining seasons run out before the fish do, the binding constraint is what I can record per season, not conservation. I take the recordable maximum in every remaining season — in the final season the stock has zero scrap value.
- I sanity-check the stock arithmetic before each submission (total take that season, then 50% regrowth capped at the maximum) so I never leave a big take on the table in a season that turns out to be the fishery's last viable one — landed fish beat fish left in the water.