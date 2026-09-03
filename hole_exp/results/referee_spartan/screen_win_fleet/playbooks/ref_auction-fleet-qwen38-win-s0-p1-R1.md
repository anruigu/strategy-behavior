---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2652
---
# Playbook: Ref Auction

**Budget tracking**
- Before every bid, recalculate: remaining budget = 30 − (sum of all winning bids I've already been charged for, i.e., lots already settled). Do not carry a running total in my head; recompute from the results list each time.
- If my remaining budget is less than the bid I want to place, I cannot bid. Check this before writing the bid.

**Round 1 (opening or responding)**
- If no one has bid and the lot is worth meaningfully more than the estimate to me, open at the estimate or slightly above. Do not open above the estimate unless my value exceeds it by a large margin (≥20% above estimate).
- If someone has already bid and my value exceeds the standing bid by at least 5, make the minimum raise to stay in. If my value exceeds the standing bid by less than 5, pass in round 1 and reassess in round 2.
- The goal of round 1 is to stay in the auction cheaply, not to win.

**Round 2 (final round — this is where I must commit)**
- If I am the current high bidder, I already win at the standing price. I only raise if I want to deter a last-moment overbid by someone who values it more than me but less than I do. In practice: if my value exceeds the standing bid by ≥10, raise to roughly 80–90% of my value to make it unprofitable for others to overbid. If my value exceeds the standing bid by less than 10, hold at the standing bid and accept the win.
- If I am NOT the current high bidder and my value exceeds the standing bid by ≥5, raise to the minimum in round 2 and accept the risk. If my value exceeds the standing bid by ≥10, raise to roughly 80–90% of my value. Do not let a lot I want slip away because I was saving budget.
- If my value is at or below the minimum raise price, pass. Zero or negative profit is not worth it.

**Budget allocation across lots**
- With 5 lots and a budget of 30, I cannot win every lot. Prioritize lots where my value minus the estimate is largest (biggest information edge).
- If I've already spent more than 60% of my budget by lot 3, become more selective: only bid on remaining lots where my value exceeds the current standing bid by a wide margin (≥15).
- If I still have more than 50% of my budget remaining by lot 4, I am under-bidding. Increase aggression.

**Mistakes to avoid**
- Never report a budget figure I haven't verified by subtraction from the settled results. A wrong budget number will cascade into wrong decisions.
- Never pass in round 2 on a lot where my value exceeds the standing bid by 5 or more. The final round is the only round where passing means losing the lot permanently.
- Never bid more than my value in any round, even by 1.