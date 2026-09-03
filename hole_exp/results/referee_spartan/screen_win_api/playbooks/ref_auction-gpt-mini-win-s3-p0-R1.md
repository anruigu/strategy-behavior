---
game: ref_auction
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1788
---
When a lot is worth less than the current standing high bid, I pass.

When a lot is worth more than the standing high bid but less than or equal to my remaining budget, I raise only by the minimum valid increment to try to win cheaply.

When I open the bidding on a lot I want, I place the minimum valid opening bid rather than a large jump.

When the current high bid is below my private value but a rival raises, I raise again only up to my private value; I never bid above my private value.

When winning a lot at a price that leaves me with little remaining budget, I reconsider bidding on future moderate-value lots and conserve for very-high-value opportunities.

When a lot’s private value is substantially higher than the standing high bid and I can afford it comfortably, I am willing to make a larger jump up to my value to discourage further competition—but I prefer to start with minimum raises first.

When the minimum raise would force me above my private value, I pass rather than overpay.

When I win a lot, I immediately and accurately deduct the winning bid from my remaining budget and use that correct budget for all future decisions.

When bids from others indicate aggressive behavior (many early high bids), I tighten my threshold for entering fights and focus on lots where I have a clear value advantage.

Do not open fights on low-value lots early; win low-value lots only by out-waiting others with minimal bids or by letting stronger bidders pay more.

If I misrecord my budget or make an impossible bid, correct it immediately and do not continue bidding until the accounting is fixed.

When multiple lots remain, prioritize preserving budget for the single lot where my private value is highest rather than spreading budget thinly across many mid-value lots.