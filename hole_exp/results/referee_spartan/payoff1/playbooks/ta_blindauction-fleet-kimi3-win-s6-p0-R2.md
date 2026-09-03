---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2373
---
When a bid is put to me, I set it as the minimum of (my value minus 1) and (a few above what the opponent has been bidding) — profit comes from the gap between value and payment, not from winning at value.

When I observe the opponent's past bids before bidding, I bid one above their observed range when my value comfortably clears it, rather than bidding near my own value. Overpaying to guarantee a win against a low-bidding opponent wasted surplus.

When my value is at or below the opponent's usual bid, I skip with a token bid (1) or bid at most value minus 1 — winning at full value gains nothing and overpaying loses. Never bid at value; there is no upside in a zero-profit win.

When my value only just clears none of the opponent's range, I still take cheap shots: bidding just under value (e.g., 3 at value 4) won a lot when the opponent dipped low, and losing to a high bid cost nothing. Cheap shots below the opponent's high bid, above their low bid, paid off twice this episode.

When I don't know the opponent's range yet (first lot), I bid moderately below value — roughly half to two-thirds — not one below value, and proportionally low on low-value lots (1 at value 2 worked as a probe).

I look for alternation or simple patterns, not just a range: Vega cycled 4/2/4, then settled at 4, then crashed to 1. Pattern-matching to the recent tail (1 on lot 5 justified a cheap 3 on lot 6) beat assuming stability. Recency matters late.

When the opponent proposes a collusion split on the private line, I do not pre-commit blind: their allocation hands me the lots they chose, and the offer may be bait. I declined and instead inferred their plan from published bids. If I ever accept anything there, I still re-derive the bid from my own values, never from their script — and I treat their promised skips as unverifiable until a cheap probe confirms them.

When a tie is the outcome, I treat it as a lost opportunity but acceptable: a tie costs nothing; an overpaying win costs. I prefer losing at a cheap bid to winning at value.

On every lot, I recompute opponent behavior from published bids and watch for a late surge or crash, since cheap early wins invite escalation or desertion on the final lots.

I track my running net from value minus payment myself, not just the displayed number, so I notice immediately if outcomes conflict with my accounting.