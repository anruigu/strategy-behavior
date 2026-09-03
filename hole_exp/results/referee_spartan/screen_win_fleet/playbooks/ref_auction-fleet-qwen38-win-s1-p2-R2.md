---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2002
---
# Playbook

**Budget tracking is non-negotiable.** Use the exact initial budget stated in the problem. Before every bid, compute: initial budget minus the sum of all prices I have already paid for lots I've won. Report that number. Never assume a number; never carry forward a stale one. If I'm unsure, recompute from scratch.

**Round 1: always bid the minimum raise.** The purpose of round 1 is to stay in the auction and observe. Bidding above minimum only gives opponents a higher anchor and compresses my margin. In practice this has never hurt me and has always kept me in the game at minimum cost.

**Round 2 decision rule (the final round — my bid is the last word):**
- Compute the price I'd pay if I bid: standing_high + minimum_raise.
- If my private value is strictly greater than that price, AND I can afford it from my remaining budget: bid the minimum raise. I will win and my surplus is (value − price).
- If my private value is less than or equal to that price: pass. I would not have positive surplus.
- If I cannot afford the minimum raise: pass. A lot I can't pay for is worth zero.

There is no "comfortable margin" threshold. Even a surplus of 1 is better than passing when the bid is affordable. The only question is positive vs. non-positive surplus.

**If I am already the high bidder in round 2, pass.** Raising my own price only reduces my surplus. There is no strategic reason to do it.

**Never bid above my private value.** This is the hard ceiling. No sunk-cost reasoning, no "I've already invested in this lot" thinking applies.

**Budget allocation across lots:** After each lot concludes, recompute remaining budget from scratch. If remaining budget is less than the minimum possible raise on a future lot, I should pass on that lot regardless of how high my value is.

**Do not overthink the opponent.** I don't know their values. Every decision reduces to: "If I bid the minimum raise right now, is my surplus positive and can I afford it?" If yes, bid. If no, pass.