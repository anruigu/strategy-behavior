---
game: ref_auction
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1806
---
When a lot is presented and the current standing bid is below my private value, I raise by the minimum required to become/highlight the high bidder if that keeps the final price likely below my value.

When the current standing bid is above my private value, I pass immediately.

When I am already the high bidder and the lot price is below my private value, I do not automatically raise further; I only raise if an opponent outbids me and the new required price remains below my private value and my remaining budget.

When an opponent outbids me, I compare the new required minimum (current bid + minimum raise) to my private value and remaining budget; I bid only if that minimum is still below my private value and winning remains net-profitable.

When deciding whether to open bidding, I often open at the minimum raise only if the lot is clearly worth more to me than that opening; avoid high opening bids that consume budget unnecessarily.

When my remaining budget is tight relative to the number of remaining lots and my private values, I conserve budget by avoiding marginal bids and prefer to win fewer lots at positive surplus rather than chase every lot.

When the required minimum raise would exceed my remaining budget (so I cannot legally raise), I pass and do not attempt to re-enter that lot.

When I win a lot, I subtract the payment from my running budget immediately and use the updated budget for all subsequent decisions.

When multiple lots remain, I prioritize lots with the largest positive difference between my private value and the public estimate, but never pay more than my private value.

What did not work: I must not escalate bidding simply to be active—raising beyond the minimum without a clear surplus or locking myself out of later valuable lots led to worse outcomes.