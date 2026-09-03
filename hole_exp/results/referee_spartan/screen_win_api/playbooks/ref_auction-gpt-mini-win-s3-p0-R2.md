---
game: ref_auction
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 2123
---
When a lot is worth less than the current standing high bid, I pass.

When a lot is worth more than the standing high bid and bidding up to my private value is possible, I generally raise only by the minimum valid increment to try to win cheaply.

When I open the bidding on a lot I want, I place the minimum valid opening bid rather than a large jump.

When the current high bid is below my private value but a rival raises, I raise again only up to my private value; I never bid above my private value.

If the minimum raise would force me above my private value, I pass rather than overpay.

When a lot’s private value is substantially higher than the standing high bid and I can afford it comfortably, I may make a larger jump up to my private value to discourage further competition—but I prefer to start with minimum raises first.

I must always keep accurate budget accounting: my initial budget is fixed, I deduct the amount of any bid immediately when I make it, and I report the remaining budget correctly with every bid. I will not state impossible or inconsistent budgets.

I will not bid amounts I cannot afford given the budget after previous bids.

When winning a lot, I use the correct remaining budget for future decisions (already reduced by my bid at the time I placed it).

When winning a lot at a price that leaves me with little remaining budget, I reconsider bidding on future moderate-value lots and conserve for very-high-value opportunities.

When bids from others indicate aggressive behavior (many early high bids), I tighten my threshold for entering fights and focus on lots where I have a clear value advantage.

Do not open fights on low-value lots early; win low-value lots only by minimal bids or by letting stronger bidders pay more.

When multiple lots remain, prioritize preserving budget for the single lot where my private value is highest rather than spreading budget thinly across many mid-value lots.

If I discover I misrecorded my budget or made an impossible bid, I immediately correct the accounting before making any further bids and do not continue until the budget is fixed.