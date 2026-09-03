---
game: ref_auction
model: haiku
condition: win
seed: 0
round: 2
chars: 2281
---
# My Auction Playbook

**On valuation and bidding discipline:**
When a lot's value to me exceeds the current bid, I will bid. The margin between my private valuation and the standing bid is what matters, not the estimate.

When I'm in round 1 of 2, I will bid conservatively to preserve capital for round 2 and remaining lots, even when I have strong value. A minimum or near-minimum raise is appropriate.

When I'm in round 2 of 2 (the final round for that lot), I can bid more aggressively since there are no more opportunities to contest that lot.

**On calculating profit potential:**
Before bidding, I will quickly estimate: value to me minus potential bid price. If this margin is positive, the bid is justified. I will not overthink the estimate price—my private valuation is what drives my decisions.

**On budget management:**
I will track my remaining budget carefully after each win. I need to know my actual budget at the start of each episode (it may not be 100—in this episode it was 200000, and I made errors by not recognizing this).

I will not assume standard amounts. Each time I see the game state, I will use the budget shown in the game feedback as ground truth, not my mental math.

When calculating whether to bid, I will base my decision on my actual remaining funds, not theoretical starting amounts. If I've won lots, I should verify my remaining budget by looking at what the game tells me, not by recalculating.

**What worked:**
- Conservative bidding in round 1 preserved capital while securing good value
- Aggressive bidding in round 2 maximized winning bids
- Focusing on margin (my value minus bid price) rather than estimate price gave me clear decision rules
- I won 4 of 5 lots and scored +72, indicating the core strategy is sound

**What needs fixing:**
My budget tracking was unreliable. In this episode my starting budget was 200000, not 100. I eventually adapted by accepting the game's feedback on remaining budget, but I should check the actual game state at the start of each episode rather than assuming a standard budget. This prevented costly errors but I can be more precise.

When computing remaining budget mid-episode, I should rely on what the game shows me, not my own arithmetic, since arithmetic errors compound across lots.