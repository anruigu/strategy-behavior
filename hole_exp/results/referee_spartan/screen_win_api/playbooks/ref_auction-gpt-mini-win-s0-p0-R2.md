---
game: ref_auction
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 2332
---
When the standing high bid is already >= my private value, I pass to avoid negative surplus.

When the standing high bid is below my private value and I want the lot, I raise only the minimum required to become the high bidder (current + minimum raise), not to my full value, to conserve resources.

When no one has bid and my private value > estimate, I open with the minimum competitive bid (the smallest allowed bid above zero) rather than committing my full value; I do this when the expected surplus (value − bid) is positive.

When I am currently the high bidder and the next required minimum raise would exceed my private value, I pass and let the other bidders fight; I do not raise beyond my value to try to protect a current winning position.

When my current high bid already equals my private value, I do not raise further.

I preserve budget for later lots: avoid spending most of my funds on an early lot unless the surplus (value − price) justifies a large commitment.

I never bid more than my private value and never bid more than my remaining uncommitted budget.

When I place a bid I must report my available budget consistently: I track committed funds separately. Concretely:
- Available (uncommitted) budget = starting budget − sum of my standing/high bids on lots I currently lead.
- When I submit a bid, I immediately commit that amount (it reduces available budget) and report available = starting − total committed.
- If I get outbid later, the previously committed amount is released back into available budget and I update reported available accordingly.
I ensure every [budget: N] I report equals my current available (uncommitted) budget after committing the new bid.

I will not engage in price wars where continuing to raise would lead to expected negative surplus; I will stop once the next required raise makes my surplus non-positive.

If bids from others appear to exceed reasonable values but I can still obtain positive surplus by outbidding minimally, I may outbid; otherwise I pass.

When deciding bids between rounds on the same lot, I apply the same minimum-raise and surplus checks each round rather than trying to average or split bids across rounds.

I update my bookkeeping after every auction event (win, loss, outbid) and use that updated available budget in all subsequent decisions.