---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2809
---
# Playbook

**Budget tracking.** Start at 30. Every time I win a lot, subtract the final price I paid. My remaining budget at any point is 30 minus the sum of all prices I have already paid for lots I have won. I report this exact number in every [budget:] field.

**Affordability check — non-negotiable.** Before I place any bid, I compare the bid amount against my remaining budget. If the bid amount exceeds my remaining budget, I pass. No exceptions. A profitable lot I cannot afford is the same as a lot I lose. In my last episode I bid 24 with 18 in the bank and bid 20 with 18 in the bank; both bids were rejected and I lost both lots. The check is: if bid > budget, pass. Full stop.

**When to bid in round 1.** If my value for the lot exceeds (standing high bid + minimum raise) AND (standing high bid + minimum raise) ≤ my remaining budget, bid the minimum raise. This tests whether the opponent will chase without committing me to a high price. If my value does not exceed the minimum possible winning price, or if the minimum winning price exceeds my budget, pass.

**When to bid in round 2 (final).** Only bid if all three conditions hold:
1. (standing high bid + minimum raise) < my value for the lot.
2. (standing high bid + minimum raise) ≤ my remaining budget.
3. I have not already committed budget to a lot that would make this bid unaffordable.

Bid the minimum raise. Never bid above my value. Never bid above my budget.

**When to pass.** The moment the minimum raise exceeds my value OR exceeds my remaining budget, pass. Both conditions are independent reasons to pass. A lot worth 36 to me is still a bad bid if I only have 18 left and the minimum winning price is 24.

**Do not chase.** If an opponent raises above me and the next minimum raise would push me past my value or past my budget, pass immediately. The lot's value doesn't increase because I want it.

**Across lots — budget is a shared resource.** My 30 is the total across all 5 lots. Winning one lot cheaply reduces what I can spend on all remaining lots. I should factor this in: if I have already spent most of my budget, I should be more willing to pass on marginal lots (where value barely exceeds price) and save what's left for a lot where the margin is large. Conversely, early in the auction with full budget, I can afford to enter more lots and let the price discover itself.

**My mistakes to avoid.**
- Bidding an amount greater than my remaining budget. This is the most costly error: the bid is rejected, I lose the lot, and I gained nothing. Always run the affordability check before committing.
- Miscalculating remaining budget. After each win, immediately compute 30 − (sum of all winning prices) and carry that forward. Do not re-derive it from scratch each time or assume a different starting number.