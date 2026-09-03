---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2567
---
# Playbook: ref_auction

**Read the starting budget from the game description and write it down on your very first turn.** Do not assume a default. The rules will state a specific number ("You start with a budget of N"). That number is your starting budget. Every subsequent calculation flows from it. If you catch yourself using a number you didn't see in the rules, stop and re-read.

**Budget tracking is the single most important discipline in this game.** After every lot I win, I subtract the price I paid from my remaining budget. Before every bid I place, I recompute: remaining = starting budget − (sum of all prices I've already paid for lots I've won). I write that number in the [budget:] token. I never estimate, never round, never carry a number forward from a previous turn without re-deriving it. If my remaining budget is less than the minimum raise, I pass.

**If I am uncertain whether I can afford a bid, I pass.** A lost lot is better than a bid the system rejects or a budget I can't actually cover.

**Round 1 of any lot: bid the minimum raise.** This signals interest, puts pressure on the other bidders, and costs me as little as possible while I gather information. The only exception is if the minimum raise would take me over my remaining budget — in that case I pass.

**Round 2 (final round) of any lot: bid the minimum raise if and only if it is within my remaining budget and the resulting price is below my private value.** I never bid more than the minimum raise in the final round. The moment the gavel drops, no one gets another chance, so paying a cent more than necessary is a pure loss. If the minimum raise exceeds my private value, I pass — the lot is not worth the price.

**When my private value is much higher than the current bid, I resist the urge to bid aggressively.** A large surplus (value minus price) is an outcome I want, not a reason to bid more. The other bidders don't know my value; I profit by staying low and letting them reveal their values to each other.

**When the current high bid is already above my private value, I pass immediately** regardless of which round it is.

**I never let a lot I lost motivate me to overbid on the next one.** Each lot is independent. My only concern on any given lot is whether the price I pay is below my value for that lot and within my remaining budget.

**At the start of each lot, I check whether my remaining budget can even cover the minimum raise.** If it can't, I pass on that lot and move on. I do not bid at a price I can't afford hoping the system will let me.