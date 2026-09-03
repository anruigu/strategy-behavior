---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 3142
---
# Playbook: Ref Auction

**Budget tracking.** My budget starts at the stated amount (e.g., 30). It decreases only when I win a lot, by the exact amount I paid. While bidding in any round, my cash is unchanged. Before I write [budget: N], I must compute: starting_budget − (sum of prices I paid for lots already won). If I have won nothing, my budget is the full starting amount. I have previously stated absurd numbers (0, 100, 73) when the true answer was simple arithmetic. This error is the single most expensive mistake I can make.

**Round 1 (information round).**
- If no bids exist and my value ≥ estimate: open at the minimum raise.
- If a bid exists and my value ≥ estimate: raise by the minimum.
- If my value < estimate: pass. A lot worth less to me than the market expects is unlikely to yield surplus, and bidding only invites competition I don't want.
- I never commit more than the minimum in round 1.

**Round 2 (final round) — the real decision.**
- If the standing high is at or above my value: pass. Paying more than the lot is worth is a guaranteed loss.
- If the standing high is below my value, I do NOT bid my full value. This is a first-price auction: I pay exactly what I bid. Bidding my value guarantees zero surplus if I win.
- **If I am the only bidder** (no one else has bid, or the standing high is my own round-1 bid): bid the minimum raise above the standing high. I want to win cheaply. If someone appears and outbids me, I lose — the same outcome as if I had bid high and they outbid me. Bidding low strictly dominates when I am alone.
- **If there is one or more competitors**: bid approximately the estimate. The estimate is a reasonable proxy for what other bidders expect the lot to be worth. If my value exceeds the estimate, bidding near the estimate captures most of my expected surplus. If my value is only slightly above the estimate, I bid just above the current high or pass.
- **Cap**: my round-2 bid never exceeds min(my_value, estimate + a small margin). In practice, I bid the estimate (or slightly below) when there is competition, and the minimum raise when I am alone.

**Why not bid my full value.** In the episode I just played, I bid 27 (my exact value) on a lot where I was the only bidder and the standing high was 2. I won at 27 and captured zero surplus. If I had bid 4 (the minimum raise), I would have won at 4 and captured 23 in surplus. The lesson: in a first-price auction with no competition, the winning price is set by you, so set it low.

**When my value is below the estimate.** I should not have bid on lot 4 (value 35, estimate 37) or been aggressive on lot 5 (value 25, estimate 29). These lots are overpriced relative to my valuation. The other bidders probably want them more than I do. I should pass in round 1 and conserve budget for lots where my value clearly exceeds the estimate.

**Prioritizing across lots.** When budget is tight, I allocate to lots where (my_value − estimate) is largest. A lot worth 35 with estimate 29 (surplus potential 6) is a better target than one worth 25 with estimate 29 (surplus potential −4). I skip negative-surplus lots entirely.