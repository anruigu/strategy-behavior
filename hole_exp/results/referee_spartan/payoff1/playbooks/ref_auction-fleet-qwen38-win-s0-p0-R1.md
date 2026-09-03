---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1992
---
# Playbook

**When a lot's value to me is well above the current standing bid:**
Open high in round 1 — at least 60-70% of my private value. Do not open timidly at the minimum raise. If I open low, I invite competition that pushes me into a bad position in round 2. A lot worth 44 to me with no bids should get an opening of 25+, not 12.

**When the standing high bid already exceeds my private value for the lot:**
Pass immediately. Do not bid. The minimum raise only makes the gap worse. There is no strategic benefit to bidding on a lot I would lose money on, even if I think I might "win" it.

**In the final round, when the minimum raise still leaves me in profit:**
Take the minimum raise. This is the best risk-reward: lowest cost to potentially win a lot where I still capture surplus. Do not bid above the minimum raise unless I'm trying to outbid a specific opponent I expect to re-enter (which is rare in a 2-round format).

**My maximum bid for any lot is my private value for that lot.**
Never bid an amount that exceeds what the lot is worth to me, even if I think I'll win. The score is value minus price; overpaying is the same as losing. If the standing bid is above my value, I lose by passing — that's fine. I lose more by bidding above value.

**Budget tracking:**
My budget only decreases when I actually win a lot. Losing a lot costs me nothing. I must recalculate my remaining budget after each lot closes, not after each bid I make. If I lose, my budget is unchanged.

**Round 1 strategy by value gap:**
- Value > 2× estimate: open at ~50% of value, signal strength.
- Value ≈ estimate: open at minimum raise or pass.
- Value < estimate: pass unless the current bid is very low and I think I can win cheaply.

**The core error to avoid:**
Winning a lot at a price above my private value. This is worse than losing a lot I wanted. It converts a neutral outcome into a negative one. Before every bid, check: is the bid amount ≤ my value for this lot? If not, do not bid.