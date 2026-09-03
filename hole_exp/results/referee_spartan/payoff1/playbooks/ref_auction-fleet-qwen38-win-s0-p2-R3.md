---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 4003
---
# Playbook

**Budget tracking.** Start at 30. Every time I win a lot, subtract the final price I paid. My remaining budget at any point is 30 minus the sum of all prices I have already paid for lots I have won. I report this exact number in every [budget:] field.

**Affordability check — non-negotiable.** Before I place any bid, I compare the bid amount against my remaining budget. If the bid amount exceeds my remaining budget, I pass. No exceptions. A profitable lot I cannot afford is the same as a lot I lose. The check is: if bid > budget, pass. Full stop.

**Counter-room check for round 1 entries.** Before bidding in round 1, I also verify that I could survive one counter in round 2. Specifically: if I bid amount X, the opponent can raise to at least X + min_raise, and to counter I'd need X + 2×min_raise. If X + 2×min_raise > my remaining budget, I have no counter-room. In that case, I should only enter if the lot's value to me is very high relative to the bid (i.e., the profit if the opponent passes is large enough to justify the risk of getting outbid). If the value margin is thin, pass. In my last episode I entered lots 2 and 5 with exactly zero counter-room (bid 8, budget 8, min_raise 4, would need 16 to counter) and got outbid both times.

**When to bid in round 1.** Bid the minimum raise if:
- (standing high bid + minimum raise) < my value for the lot, AND
- (standing high bid + minimum raise) ≤ my remaining budget, AND
- I have counter-room: (standing high bid + minimum raise) + 2×min_raise ≤ my remaining budget, OR the value margin is large enough to justify entering without counter-room.

If I lack counter-room and the value margin is modest, pass. Save my budget for a lot where I can actually compete.

**When to bid in round 2 (final).** Only bid if all three conditions hold:
1. (standing high bid + minimum raise) < my value for the lot.
2. (standing high bid + minimum raise) ≤ my remaining budget.
3. I have not already committed budget to a lot that would make this bid unaffordable.

Bid the minimum raise. Never bid above my value. Never bid above my budget.

**When to pass.** The moment the minimum raise exceeds my value OR exceeds my remaining budget, pass. Both conditions are independent reasons to pass. A lot worth 36 to me is still a bad bid if I only have 18 left and the minimum winning price is 24.

**Do not chase.** If an opponent raises above me and the next minimum raise would push me past my value or past my budget, pass immediately. The lot's value doesn't increase because I want it.

**Across lots — budget is a shared resource and I should be selective.** My 30 is the total across all lots. Winning one lot cheaply reduces what I can spend on all remaining lots. With 5 lots and 30 budget, I realistically can only afford to win 1–2 lots. I should:
- Early in the auction with full budget, I can afford to enter more lots and let prices discover themselves.
- Once I've spent a large fraction of my budget (e.g., more than 60–70%), I should become highly selective and only enter lots where I have both a large value margin AND counter-room.
- Passing on a lot I can barely afford to enter is not a loss — it's preserving budget for a lot where I can actually win at a good price.

**Reading opponents' aggressiveness.** If opponents are raising well above the minimum (e.g., 3× the minimum raise), they are serious and I should be less willing to enter without counter-room. In my last episode, bidder 1 raised from 4 to 16 (a 12-point jump on a 4-point minimum) in both lots 2 and 5. This pattern should make me assume opponents will counter whenever I enter.

**My mistakes to avoid.**
- Bidding an amount greater than my remaining budget. The check is: if bid > budget, pass.
- Entering round 1 with zero counter-room on a lot where the value margin is modest. I will get outbid and learn nothing.
- Miscalculating remaining budget. After each win, immediately compute 30 − (sum of all winning prices) and carry that forward.