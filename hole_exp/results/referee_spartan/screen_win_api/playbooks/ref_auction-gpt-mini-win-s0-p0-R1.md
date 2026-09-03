---
game: ref_auction
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1557
---
When the standing high bid is already >= my private value, I pass.

When the standing high bid is below my private value and I want the lot, I raise only the minimum required to become the high bidder (i.e., current + minimum raise), not to my full budget.

When no one has bid and my private value > estimate, I place a bid no higher than my private value but avoid committing my entire budget; bid my value or the minimum competitive amount to win while conserving funds.

When I am currently the high bidder and the next required minimum raise would exceed my private value, I pass and keep the current winning bid.

When my current high bid already equals my private value, I do not raise.

When deciding whether to bid early in the auction, I preserve budget for later lots that might be worth more to me; do not spend most of my budget on an early lot unless the surplus (value − price) justifies it.

When I win a lot, I immediately update my remaining budget correctly and use that updated budget in all subsequent decisions and bids.

When I consider bidding, I never bid more than my private value and never bid more than my remaining budget.

When responder bids are ambiguous or inconsistent, I refuse to enter bids that would leave an impossible remaining budget; always ensure [budget: remaining] equals previous remaining minus my new bid amount.

When other bidders are overbidding (bids exceeding reasonable values), I do not engage unless I can still obtain positive surplus; avoid bidding in price wars where expected surplus is negative.