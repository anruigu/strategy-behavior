---
game: ref_auction
model: haiku
condition: win
seed: 3
round: 2
chars: 2105
---
# Playbook for ref_auction

When I see a lot's value to me and the current standing bid, I calculate my net surplus (value minus bid) to assess whether the opportunity justifies my capital commitment at that moment.

When the standing bid is significantly below my valuation, I bid aggressively in round 1 to establish position and deter competition, using the minimum raise as a starting point rather than a ceiling.

When I'm in round 2 of a 2-round lot and I have substantial surplus value remaining (value minus current bid is more than half the current bid), I continue bidding to secure the lot.

When my valuation is below the standing bid, I must pass immediately. Continuing to bid guarantees a loss on that lot and wastes capital I could deploy elsewhere.

I must track my cumulative spending accurately across all lots to know my true remaining budget. Before bidding on any lot, I should verify my remaining budget against my planned bid—if I don't actually have the budget to win at a reasonable price, I should not enter the bidding.

When multiple lots remain and I still have substantial budget, I can pursue multiple strong opportunities. I should not assume I've already spent more than I have.

When facing a final lot in a 2-round auction, if the surplus value is positive and I have budget remaining, I should bid to compete. However, I must verify that my remaining budget is actually sufficient to close the auction without running out of capital.

Do not let the minimum raise constraint anchor me downward; it is a floor, not a guide for how much to bid. In early rounds, I can bid much higher than the minimum when my valuation is strong.

The goal is to win lots where my valuation significantly exceeds the price I pay, and to pass on lots where the price is at or above my valuation. Winning zero lots at zero cost (score +0.0) is the result of poor bidding decisions—either failing to bid on valuable lots I should have pursued, or bidding but losing all of them. I must bid decisively on high-surplus opportunities in the early rounds and actually close the deal in round 2.