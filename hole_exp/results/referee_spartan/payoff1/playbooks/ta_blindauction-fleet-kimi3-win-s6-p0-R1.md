---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1892
---
When a bid is put to me, I set it as the minimum of (my value minus 1) and (a few above what the opponent has been bidding) — profit comes from the gap between value and payment, not from winning at value.

When I observe the opponent's past bids before bidding, I bid one above their observed range when my value comfortably clears it, rather than bidding near my own value. Overpaying to guarantee a win against a low-bidding opponent wasted surplus; on early lots I paid 6 and 8 to beat bids of 2 and 4 — a bid of 5 would have given the same wins for far more profit.

When my value is at or below the opponent's usual bid, I skip or bid my value minus profit margin — winning at 5 for a value of 5 gained nothing and should be avoided. Never bid at value; there is no upside in a zero-profit win.

When I don't know the opponent's range yet (first lot), I bid moderately below value — roughly half to two-thirds — not one below value.

When a tie is the outcome, I treat it as a lost opportunity but acceptable: a tie costs nothing; an overpaying win costs. I prefer losing at a cheap bid to winning at value.

When the opponent proposes a collusion split on the private line, I do not pre-commit blind: their allocation hands me the lots they chose for me. Instead, I can either decline or use the information — they revealed which lots they intend to skip (lots they offered me) and which they plan to contest. I bid a token amount (1) on the lots they promised to skip and conserve on the contested ones.

On every lot, I recompute opponent behavior from published bids; their bids were stable, so pattern-matching beat value-matching there — but I watch for a late surge, since cheap wins invite escalation on the final lots.

I track my running net from value minus payment myself, not from the displayed number alone, so I notice immediately if outcomes conflict with my accounting.