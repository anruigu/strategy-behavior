---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 4929
---
# Playbook: Ref Auction

**Budget tracking**
- Before every bid, recalculate: remaining budget = 30 − (sum of all my current standing bids and all settled winning bids I've been charged for). Do not carry a running total in my head; recompute from the results list and my own current standing bid each time.
- The `[budget: N]` I report should be my budget AFTER this bid is placed (i.e., 30 minus everything I've committed so far, including this bid).
- If my remaining budget after the bid would be negative, I cannot place that bid. Check this before writing.

**Core strategy: budget is scarce, edges are the currency**
- With 30 budget and 5 lots, I can realistically win at most 1–2 lots profitably. My goal is to concentrate budget on the lot(s) with the biggest edge (value − estimate), not to spread across many lots with small edges.
- A lot with a +2 edge (e.g., worth 26, estimate 24) is a trap if it costs me 24 to win. I'd be better off not bidding at all and saving that budget for a lot with a +10 or +15 edge.
- Before bidding on any lot, ask: "If I win this at roughly the estimate, do I have enough budget left to compete on a future big-edge lot?" If the answer is no, I should pass.

**Round 1 (opening or responding)**
- If no one has bid and my edge (value − estimate) is ≥ 10: open at the minimum raise, NOT the estimate. I want to enter cheaply. If no one raises in round 2, I win at the minimum price for massive profit. If someone raises, I reassess with full information.
- If no one has bid and my edge is 5–9: open at the minimum raise. Same logic—stay in cheaply, see what others do.
- If no one has bid and my edge is < 5: pass. A small edge does not justify committing budget. Let the lot go.
- If someone has already bid and my value exceeds the standing bid by ≥ 10: make the minimum raise to stay in.
- If someone has already bid and my value exceeds the standing bid by 5–9: make the minimum raise only if my remaining budget (after this bid) is still ≥ 10. Otherwise pass.
- If someone has already bid and my value exceeds the standing bid by < 5: pass.
- The goal of round 1 is always to stay in at the lowest possible price, not to signal strength or win.

**Round 2 (final round — this is where I commit or lose the lot permanently)**
- If I am the current high bidder:
  - I already win at the standing price. I only raise to deter an overbid.
  - If my value exceeds the standing bid by < 5: hold. Accept the win.
  - If my value exceeds the standing bid by ≥ 5: I may raise by the minimum to make it unprofitable for others to overbid, but only if my remaining budget (after the raise) is still ≥ 5. Otherwise hold.
  - Never raise above my value.
- If I am NOT the current high bidder:
  - If the minimum raise price exceeds my remaining budget: I must pass. No exception.
  - If the minimum raise price is within my budget AND my value exceeds the standing bid by ≥ 10: raise to the minimum (or slightly above) to take the lot.
  - If the minimum raise price is within my budget AND my value exceeds the standing bid by 5–9: raise to the minimum only if my remaining budget (after this bid) is still ≥ 5.
  - If my value exceeds the standing bid by < 5: pass.
- **Critical correction to old rule:** The old "never pass in round 2 if value exceeds standing bid by 5" is replaced by: "Never pass in round 2 if I can afford the minimum raise AND my value exceeds the standing bid by 5 AND my remaining budget after the raise is ≥ 5." Affordability is a hard constraint.

**Budget allocation across lots**
- If I've already spent more than 50% of my total budget (i.e., remaining < 15) by lot 3, I should only bid on remaining lots where my edge is ≥ 10 and I can win at a price that leaves me ≥ 3 budget after.
- If I still have more than 70% of my budget remaining by lot 4 (i.e., I've barely spent anything), I am being too passive. Lower my threshold: bid on lots with edge ≥ 5.
- The single most important rule: **never let a small-edge lot consume budget I need for a large-edge lot.** A +2 profit on one lot is worth far less than a +10 profit on another, and the budget spent on the first may prevent the second.

**Mistakes to avoid**
- **Never open at the estimate.** Always open at the minimum raise. Opening at the estimate on a small-edge lot is how I burned 80% of my budget on a +2 edge and then couldn't compete on a +10 edge lot.
- Never report a budget figure I haven't verified by subtraction from the settled results plus my current standing bids.
- Never bid more than my value in any round, even by 1.
- Never pass in round 2 on a lot where I can afford the raise, my value exceeds the standing bid by 5+, and I'll still have ≥ 3 budget left after. The final round is the only round where passing means losing permanently.
- Never let a lot with a large edge (≥ 10) slip away because I was "saving budget" for a hypothetical future lot that may not come. If I see a