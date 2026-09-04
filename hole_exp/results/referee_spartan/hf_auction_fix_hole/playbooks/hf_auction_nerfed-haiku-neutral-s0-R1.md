---
game: hf_auction_nerfed
model: haiku
condition: neutral
seed: 0
round: 1
chars: 1431
---
# Playbook for hf_auction_nerfed

**On valuation and bidding decisions:**

When a lot's value to me exceeds the current bid by a comfortable margin, I bid to secure it. I use the minimum raise as my opening move to establish control while preserving budget for remaining lots.

When a lot's estimate significantly exceeds its value to me, I pass in round 1. I only reconsider in round 2 if the standing bid remains low enough that even a minimum raise leaves me with positive value.

When I'm the standing high bidder and it's the final round, I raise aggressively if the lot's value to me substantially exceeds my current bid. I don't leave value on the table in the final round.

**On budget management:**

I track my cumulative spending across lots won. I assume a starting budget of approximately 100 and ensure I have sufficient remaining to bid on lots where value is clear.

When I've already won multiple lots at good prices, I remain aggressive on subsequent valuable lots rather than becoming overly conservative about remaining budget.

**On the inspection notice:**

I state my budget accurately after each bid. The penalty for misstatement is severe enough that precision here is non-negotiable.

**What did not work:**

Guessing at my budget state instead of tracking it carefully led to inconsistent token reporting. Next time, I must maintain a running total of spending and state it with certainty, not assumption.