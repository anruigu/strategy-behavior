---
game: ref_auction
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 2701
---
When a lot’s current standing bid is below my private value, I consider winning it at the lowest possible price that still makes me the leader; I prefer the minimum legal raise when that secures positive surplus.

I treat “positive surplus” as value − price > 0 for routine bidding; I will consider bidding up to equal to my value only in edge cases where nonnegative surplus (value − price ≥ 0) is strategically justified (e.g., to block an opponent from a very valuable lot or when remaining lots are unattractive).

When the standing bid is already at or above my private value, I pass.

When the next legal bid would exceed my private value, I pass (unless I have a specific, justified reason to accept zero or negative surplus per the previous line).

When there are multiple lots remaining, I preserve budget by using the minimum legal raise rather than bidding for the full surplus immediately; I prioritize lots with higher private value relative to the estimate.

When my remaining budget is limited but the lot is highly valuable to me, I may bid more aggressively up to my private value; I will go all-in only if the all-in bid yields nonnegative surplus (value ≥ bid) and I accept reduced flexibility for later lots.

When I am currently the high bidder and get outbid, I only increase again if the new standing bid is still below my private value; I typically match the minimum legal raise to defend the lot rather than making large jumps.

When opening on a lot with no bids, I generally open with the minimum legal raise if the lot’s value exceeds that opening bid and I want to conserve budget for later contests.

I track my remaining budget exactly and never submit a bid that makes my stated budget inconsistent with my previous bids; I correct any bookkeeping mistakes immediately and do not rely on “accepting” an accounting error.

I base bidding decisions on my private valuations and budget constraints rather than blindly imitating opponents’ aggression; opponent behavior informs whether I expect further competition but does not override my value-based limits.

When faced with small increments or ties, prefer the legally minimal raise to deter marginal challengers while retaining budget for higher-priority lots.

If opponent winning prices reveal systematic overbidding relative to estimates, I exploit that by sticking to my private values and letting them overpay, but I will contest a lot if my private value justifies driving the price up (per my budget and surplus rules).

I will periodically re-evaluate my remaining budget against remaining lots’ private values after each lot to decide whether to conserve more or to invest in securing a currently valuable lot.