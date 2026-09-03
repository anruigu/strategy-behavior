---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1808
---
# Playbook

**Budget tracking is non-negotiable.** Before every bid, compute: initial budget minus the sum of all prices I have already paid for lots I've won. Report that number. Never guess or carry forward a stale number. If I'm unsure, recompute from scratch each time.

**Round 1: always bid the minimum raise.** The purpose of round 1 is to stay in the auction and observe the competitor's round-2 behavior. Bidding a "strong signal" above minimum only gives the other bidder a higher anchor to respond from, compressing my final margin. I lost significant surplus on lot 4 by jumping to 15 when the minimum was 6; the opponent then pushed to 33 and I was left with 2 profit.

**Round 2 decision rule:**
- If the standing high bid is below my value by a comfortable margin (≥5), bid the minimum raise to win cheaply.
- If the standing high bid is within 4 of my value, bid the minimum raise only if I have a clear reason to want the lot (e.g., it's the last lot, or I've already invested in this auction). Otherwise, pass and accept the thin margin isn't worth the risk.
- If the standing high bid is at or above my value, pass immediately. Never bid above my private value.

**If I am already the high bidder in round 2, pass.** Raising my own price only reduces my surplus. There is no strategic reason to do it.

**Budget allocation across lots:** After each lot concludes, recompute remaining budget. If remaining budget is less than the minimum possible raise on an upcoming lot, I should pass on that lot regardless of how high my value is. A lot I can't afford is worth zero.

**Do not overthink the opponent.** I don't know their values. Treat every round as: "Is the current price below my value? If yes, can I win at a price that leaves me positive surplus? If yes, bid minimum. If no, pass."