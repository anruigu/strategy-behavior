---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 2187
---
When a lot worth V to me comes up:
- Round 1: bid at or near the minimum raise only when V comfortably exceeds the minimum; otherwise pass.
- Round 2 (final): bid my full value V minus 1 (capped by budget), because this is my last chance — bidding the bare minimum raise just gifts the lot to someone willing to top it. Accept that I may still lose: rivals do bid above my value sometimes, and that is fine — I never chase past V−1.

Budget reporting is the thing that sank me, so I hold it as discipline one:
- My remaining budget is my starting budget minus only what I have ACTUALLY PAID for lots I WON. Losing bids cost nothing. A bid I am about to make does NOT reduce my budget — I never deduct it preemptively.
- CRITICAL: in this episode I deducted my pending round-1 bid, then in round 2 bid more than the budget figure I had declared (bid 30 after declaring 24), and my bid was rejected — I lost a lot I should easily have won to a standing bid of 9. Never again: the [budget] token must be my true unspent cash, and every bid must be ≤ that figure.
- I never write vague phrases like "full starting budget minus 3" in a token; the token is always a plain integer.

Never bid more than my remaining budget. With a small budget (e.g. 30) and many lots, full-value round-2 bids can exceed it — cap my bid at budget, and remember budget only shrinks when I actually win.

Rivals in this game can win lots very cheaply (9, 29, 30) when my bids are weak or invalid. My round-1 minimum bid is fine as a feeler, but the round-2 near-value bid is what actually wins; nothing should ever invalidate it — an invalid bid scores me zero no matter how good the value.

Skip any lot where the standing bid plus the minimum raise reaches my value; a bid at or above my value yields no surplus, so I pass.

Track results as they are posted each lot: updates to my budget happen only on "won" lines with my bidder number.

On the last lot, only fight for it if its value exceeds the likely winning price by enough to beat my expected score from passing.

Reply ends with both tokens every time, even when I just pass, and both tokens are plain integers consistent with everything I said before.