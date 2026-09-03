---
game: ref_auction
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 2157
---
When a standing high bid is already above my private value, I pass and keep my remaining budget unchanged.

When the standing high bid is below my private value in the final bidding round, I am willing to jump up to my private value to try to win the lot.

When the standing high bid is below my private value in the first round, I raise by the minimum raise to probe and conserve budget.

When the standing high bid is close to my private value (within one minimum raise), I still pass rather than overpay — never raise above my private value.

When I can win a lot at or below the minimum profitable price (price < my private value), I prefer to bid the minimum required to become/highlight the current leader to keep the eventual price low.

When I have already won multiple lots and my remaining budget is limited, I prioritize lots with the largest surplus (my value − estimate/price) and otherwise tighten to minimum raises or pass.

When a rival suddenly jumps high in the final round above my value, I do not enter a bidding war; I pass immediately.

When a lot has no bids at opening and my value is modest, I place a small opening bid equal to the minimum raise to avoid paying too much later; when my value is high and I expect competition, I may be prepared to bid up to my value in the final round.

Always state my remaining budget correctly after every bid or pass and do not reset it accidentally.

When multiple lots remain and budget is constrained, I allocate budget to maximize expected surplus: prefer winning fewer high-surplus lots at near my valuation rather than many low-surplus lots.

When the minimum raise would still leave room to profit (new price < my value), prefer the minimum raise rather than a larger increment to avoid signaling willingness to pay more.

When I can win a lot cheaply in round one, I still consider saving budget if there are later lots with significantly higher private value; be ready to forgo a low surplus win for a future higher surplus opportunity.

When in doubt on whether to contest, default to conserving budget unless winning yields clear positive surplus relative to remaining opportunities.