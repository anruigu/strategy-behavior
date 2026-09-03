---
game: ref_auction
model: haiku
condition: win
seed: 3
round: 1
chars: 1657
---
# Playbook for ref_auction

When I see a lot's value to me and the current standing bid, I calculate my net surplus (value minus bid) to assess whether the opportunity justifies my capital commitment at that moment.

When the standing bid is significantly below my valuation, I bid aggressively in round 1 to establish position and deter competition, using the minimum raise as a starting point rather than a ceiling.

When I'm in round 2 of a 2-round lot and I have substantial surplus value remaining (value minus current bid is more than half the current bid), I continue bidding to secure the lot.

When my remaining budget is low but a lot offers exceptional value, I calculate whether the absolute winning price I'd need to pay could exceed my valuation, and if so, I still bid because the expected value is positive.

When I win a lot, I must track my cumulative spending accurately across all lots to know my true remaining budget—I made an error treating a 30-unit starting budget incorrectly and this damaged my capital allocation.

When multiple lots remain and I've already committed significant capital, I preserve aggressive bidding for lots where my valuation is highest relative to the current bid (highest surplus potential).

When facing the final lot in a 2-round auction, if the surplus value (my valuation minus standing bid) is positive and meaningful, I bid to win it because there are no future opportunities to deploy my remaining budget.

Do not let the minimum raise constraint anchor me downward; it is a floor, not a guide for how much to bid. In early rounds, I can bid much higher than the minimum when my valuation is strong.