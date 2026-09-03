---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 3041
---
# Playbook: ref_auction

**Read the starting budget from the game description and write it down on your very first turn.** Do not assume a default. The rules will state a specific number ("You start with a budget of N"). That number is your starting budget. Every subsequent calculation flows from it. If I catch myself using a number I didn't see in the rules, stop and re-read.

**Budget tracking formula — apply before every single bid, no exceptions:**

remaining = starting_budget − (sum of prices I paid for lots I have already won)

I compute this from scratch each time. I do not carry a number forward from a previous turn. I do not guess. I do not use a number that doesn't come from this formula. The [budget:] token I write must be the output of this formula. If I write a number that I cannot derive by doing the arithmetic above, I have made an error and I stop.

**Affordability check before every bid:** The price I would be paying if I win this lot is my bid amount (the number after [bid:]). I can only place that bid if: (sum of prices I've already paid for won lots) + (my bid amount) ≤ starting_budget. If it exceeds, I pass. This is not about "minimum raise" as an abstract increment — it is about whether the total price I'd commit to is within my starting budget.

**If I am uncertain whether I can afford a bid, I pass.** A lost lot is better than a bid the system rejects or a budget I can't actually cover.

**Round 1 of any lot: bid the minimum raise.** This signals interest, puts pressure on the other bidders, and costs me as little as possible while I gather information. The only exception is if the minimum raise would take me over my remaining budget — in that case I pass.

**Round 2 (final round) of any lot: bid the minimum raise if and only if (a) the resulting bid price is below my private value, and (b) the affordability check above passes.** I never bid more than the minimum raise in the final round. The moment the gavel drops, no one gets another chance, so paying a cent more than necessary is a pure loss. If the minimum raise exceeds my private value, I pass. If it exceeds my remaining budget, I pass.

**When my private value is much higher than the current bid, I resist the urge to bid aggressively.** A large surplus (value minus price) is an outcome I want, not a reason to bid more. The other bidders don't know my value; I profit by staying low and letting them reveal their values to each other.

**When the current high bid is already above my private value, I pass immediately** regardless of which round it is.

**I never let a lot I lost motivate me to overbid on the next one.** Each lot is independent. My only concern on any given lot is whether the price I pay is below my value for that lot and within my remaining budget.

**At the start of each lot, I recompute my remaining budget from the formula and check whether it can cover the minimum raise price.** If it can't, I pass on that lot and move on. I do not bid at a price I can't afford hoping the system will let me.