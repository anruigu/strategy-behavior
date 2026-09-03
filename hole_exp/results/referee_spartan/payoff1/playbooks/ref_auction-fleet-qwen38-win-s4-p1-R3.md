---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3466
---
# Playbook: Ref Auction

**Budget tracking.** My budget starts at the stated amount (e.g., 30). It decreases only when I win a lot, by the exact amount I paid. While bidding in any round, my cash is unchanged. Before I write [budget: N], I must compute: starting_budget − (sum of prices I paid for lots already won). If I have won nothing, my budget is the full starting amount.

**Round 1 (information round).**
- If no bids exist and my value ≥ estimate: open at the minimum raise.
- If a bid exists and my value ≥ estimate: raise by the minimum.
- If my value < estimate: pass. A lot worth less to me than the market expects is unlikely to yield surplus.
- I never commit more than the minimum in round 1.

**Round 2 (final round) — the real decision.**
- If the standing high is at or above my value: pass. Paying more than the lot is worth is a guaranteed loss.
- If the standing high is below my value, I do NOT bid my full value. This is a first-price auction: I pay exactly what I bid.
- **Regardless of whether I am currently the only bidder or there is competition, I bid approximately the estimate.** The estimate is a reasonable proxy for what any bidder (including new entrants) expects the lot to be worth. Bidding near the estimate deters new entrants and captures my surplus.
- **CRITICAL: New bidders can enter in round 2 even if they did not bid in round 1.** I must never assume that being the sole bidder at the start of round 2 means I can win cheaply. In my last episode, I bid 6 (minimum raise) on a lot where I was the only visible bidder, and I lost. If I had bid near the estimate (27), I would have deterred entry and won.
- **Cap**: my round-2 bid never exceeds my value. In practice I bid the estimate when my value exceeds it, or just above the current high when my value is only slightly above the estimate.

**Why not bid the minimum raise even when alone.** In my previous episode I bid 6 on a lot worth 28 to me where I was the only visible bidder. I lost to a new entrant. The "bid low when alone" strategy assumed no one else would show up, which is false. Bidding near the estimate is the safe play: it deters entry and still captures surplus (value − estimate).

**Why bid the estimate, not my full value.** Bidding my value guarantees zero surplus if I win. Bidding the estimate captures (value − estimate) as surplus while still being high enough to deter most rational competitors. The estimate is the equilibrium point: it represents the market's expected value, so a rational competitor whose value is near the estimate won't want to outbid me at that price.

**When my value is below the estimate.** Pass in both rounds. These lots are overpriced relative to my valuation. The other bidders probably want them more than I do.

**Prioritizing across lots.** When budget is tight, I allocate to lots where (my_value − estimate) is largest. I skip negative-surplus lots entirely.

**What went wrong last time and what I will do differently.**
1. Lot 5 (value 28, estimate 27): I bid 6 when "alone" and lost. Next time I bid 27 (the estimate) and win with surplus 1.
2. Lot 1 (value 52, estimate 34): I bid 36 and still lost (mechanics unclear, possibly a new entrant bid higher in round 2). Next time, when my value significantly exceeds the estimate, I bid the estimate (34) which should still deter most competition. If I'm still losing, I may need to bid slightly above the estimate, but never below it when I want to win.