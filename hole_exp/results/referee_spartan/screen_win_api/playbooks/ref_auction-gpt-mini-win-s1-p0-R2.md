---
game: ref_auction
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 2642
---
When I see a lot with a standing bid of 0 and my private value > 0, I open with the auction's minimum raise (the smallest allowed opening) rather than my full value, to probe interest while conserving budget.

When the standing high bid is below my value and the next allowable bid (standing + minimum raise) is ≤ my value, I raise to that next allowable bid (not more) to conserve budget and only escalate as needed.

If the next allowable bid would exceed my private value, I pass immediately; I do not bid above my valuation.

If the standing high bid already equals or exceeds my private value, I pass; I avoid entering bidding wars that would produce non-positive payoff.

When I can win cheaply (standing bid well below my value), I prefer the minimum raise to outbid the current leader rather than jumping to my full value; I only bid up to my value if necessary to outbid someone.

In the final round for a lot, I compute the exact next-minimum (current standing + min raise). If my value ≥ next-minimum and I can afford it, I raise to next-minimum; otherwise I pass.

When multiple lots remain and my budget is constrained, I prioritize lots with the largest margin (private value − expected price) and use minimum raises to stretch budget across the most profitable opportunities.

If I lose a lot because I underbid early, I accept the outcome and do not compensate by making irrationally large bids on later lots; I stick to my value-based rules.

When deciding whether to open on a low-value lot, default to passing unless I can obtain it at a price that leaves a clear positive margin (i.e., at or near the minimum raise).

Always track my remaining budget precisely: before making any bid I confirm the bid amount is ≤ current budget and update my reported budget to budget − bid. Never report inconsistent or impossible budgets.

State bids and budgets clearly and accurately in the required format; ensure the bid I announce is one I can pay given my current budget after accounting for any previously committed wins.

If opponents repeatedly post high standing bids early, consider conserving budget for later lots where my private values are higher rather than chasing marginal gains on early expensive lots.

When another bidder's standing high bid is small but they have escalated quickly, recognize that they may be willing to pay above the minimum; still default to the minimum raise policy unless my private value and margin justify a larger jump.

Re-evaluate priorities after each lot is resolved: update remaining budget and remaining lots' relative values, and adjust subsequent bidding aggressiveness accordingly.