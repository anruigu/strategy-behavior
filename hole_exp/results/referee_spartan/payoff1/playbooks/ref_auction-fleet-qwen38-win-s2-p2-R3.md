---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 2469
---
# Playbook

**Budget is starting budget minus prices paid for lots I actually won.** I determine "won" only at the end of a lot's final round. A bid I make in round 1 that is later outbid commits me to nothing. I never deduct a round-1 bid from my budget unless I ultimately win the lot. Before every reply I compute: remaining budget = stated starting budget − (sum of my winning bids on previously completed lots). If I haven't won anything yet, my remaining budget is the full starting budget. I write that exact number in the [budget:] token. I never guess, round, or carry forward a stale figure.

**The minimum valid bid is always current_high_bid + minimum_raise_increment.** The "minimum raise" stated in the prompt is the increment, not the bid itself. If the current high is 5 and the minimum raise is 3, my next bid must be at least 8, not 3. I always compute this sum before deciding to bid.

**Never bid above my private value for a lot.** This is a hard ceiling. If a lot is worth 30 to me, I never bid 31 or higher regardless of round or competition.

**In round 1 of a two-round lot, I bid the minimum valid bid (current high + increment) only if my value exceeds the current high by at least twice the minimum raise increment.** This keeps me in cheaply for round 2. If the surplus is thin, I pass in round 1 and save budget.

**In round 2 (the final round), I bid the minimum valid bid (current high + increment) if I want the lot and that amount is at or below my value.** I do not bid more than the minimum valid bid—bidding higher only reduces surplus with no strategic benefit. If the minimum valid bid exceeds my value, I pass.

**I allocate budget across lots by expected surplus.** I rank lots by (my value − expected winning price). I reserve budget for high-surplus lots and walk away from low-surplus ones when the price approaches my value.

**I track who has won previous lots and at what price.** If a rival has been winning at prices above my values, they are likely overpaying or have high values I can't match—letting them exhaust their budget is fine. If a rival has been passing, they may be saving for a lot they value highly; I should be cautious on that lot.

**When my remaining budget is less than the minimum valid bid, I pass.** The budget is a hard constraint.

**I do not chase losses.** If I've lost several lots in a row, I do not raise my bids beyond what value and budget justify. I apply the same rules to the next lot.