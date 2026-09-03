---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2126
---
# Playbook

**Budget tracking.** My budget only decreases when I actually win a lot, not when I place a bid. Before every response, I recompute: starting budget minus the sum of all lots I have already won. I state that exact number in my [budget] token. I never guess or round. If I started with 30 and won one lot at 40, my remaining budget is -10 (I'm over). I state it honestly.

**Budget is a hard constraint on bidding.** I will not place a bid that exceeds my remaining budget. If the minimum raise in the final round would cost more than I have left, I pass. This is non-negotiable even if the lot is high-value to me. With a tight total budget (e.g., 30 across 5 lots), I can realistically afford to win at most one or two lots, so I must be selective.

**Selectivity with a tight budget.** When my total budget is small relative to typical final prices, I should not enter every auction. In round 1, I only raise if I expect the final price to land within my remaining budget AND the lot's value to me comfortably exceeds that expected price. If the standing bid is already high and I have little budget left, I pass in round 1 and stay out.

**Round 1 (non-final round).** If I decide to enter, I raise to a moderate amount — enough to stay in the auction but well below my value and well below my remaining budget. I am not trying to win in round 1; I am staking a claim cheaply. I never bid more than what I can afford to eventually pay.

**Round 2 (final round).** This is the only round where the bid is binding. I bid exactly the minimum raise over the standing high bid, and no more. There is zero strategic benefit to bidding above the minimum in the final round. If the minimum raise would push my bid to or above my value, I pass. If the minimum raise exceeds my remaining budget, I pass.

**Never bid below the standing high bid.** A bid must exceed the current high to be valid. If I cannot or should not raise, I pass. I never accidentally submit a number that is below the standing bid.

**Never bid at or above my value.** Bidding at my value guarantees zero profit; above it guarantees a loss. In the