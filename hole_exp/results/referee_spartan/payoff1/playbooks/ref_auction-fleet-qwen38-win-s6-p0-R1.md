---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 2979
---
# Playbook

**Budget tracking.** After every bid I make, my remaining budget is (previous remaining budget − amount I paid for any lot I won so far). I do not subtract bids I lose. Before I write a [budget: N] token, I recount from the start: 30 minus the sum of prices I actually paid to win lots. I never guess or carry forward a number I didn't derive.

**Opening a lot (no standing bid, round 1).** I bid roughly 40–50% of my value. This signals interest, anchors the auction below my value, and leaves room to raise in round 2 without immediately hitting my ceiling.

**Responding to a standing bid in round 1.** I bid the minimum raise. This keeps me in the auction at the lowest possible cost while I gather information about how aggressively others are bidding. I only bid above the minimum raise in round 1 if my value exceeds the minimum-raise price by more than 30%, in which case I bid the minimum raise plus a small increment.

**Final round (round 2) when I want to win.** I do NOT bid my full value. I do NOT bid only the minimum raise (other bidders can still counter after me). I bid the minimum raise plus enough to create a gap that makes it unattractive for others to continue, capped at 90% of my value. Concretely: I bid min(value × 0.9, standing_bid + 2 × minimum_raise). This gives me a fighting chance to win while preserving at least 10% profit margin.

**Final round when I am uncertain whether to win.** If my value minus the minimum-raise price is less than 20% of my value (i.e., thin margin), I pass unless the lot is the only high-value one left to me. Thin-margin wins erode my score through accumulated small losses or zero-profit wins.

**Passing.** When the minimum raise price exceeds my value for the lot, I pass immediately. No exception. I do not bid a loss "to keep up appearances" or because I've already committed psychologically.

**Cross-lot budget management.** Before bidding on any lot after the first, I check: if I win this lot at my planned bid price, do I still have enough budget remaining to cover at least one other lot I might want? If not, I lower my bid or pass. I never let a single lot consume more than 50% of my remaining budget unless it is the last lot or my value is exceptional.

**Reading opponents.** If a bidder has been winning lots at prices near my value for those lots, they are likely valuing lots similarly to me and I should be more cautious. If a bidder has been passing on lots I value highly, they may not value them and I can afford to be more aggressive.

**What did not work last time.** I was too passive on a lot worth 52 to me (only bid 18 when the auction was at 14) and lost it at 26 — a missed profit of 26. Conversely, I bid my exact value (25) on a lot worth 25 and won at 25 for zero profit; I should have bid 20–22 and likely still won. The fix: in round 2, commit to a higher bid when my value is well above the current price, but stop short of my full value to lock in positive margin.