---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2181
---
# Playbook

**Budget discipline is non-negotiable.** Before every bid, I calculate my actual remaining budget: starting budget minus the sum of all prices I've already paid for lots I've won. I write down that number in my head each time. I never declare a budget figure that I haven't derived this way. If my remaining budget is less than the minimum raise, I pass.

**Never bid above my private value for a lot.** This is a hard ceiling. If a lot is worth 35 to me, I never bid 36 or higher regardless of the round or the competition. Bidding above value guarantees a loss on that lot.

**In round 1 of a two-round lot, I bid the minimum raise only if my value exceeds the current high bid by at least twice the minimum raise.** This keeps me in the auction at low cost while preserving budget for the final round. If the surplus is thin, I pass in round 1 and wait.

**In round 2 (the final round), I bid up to my value minus a small margin (1–2 units) if I want the lot.** The goal is to win at a price that still leaves positive profit. I don't need to signal anything—this is the last chance. If the minimum raise would push me above my value, I pass.

**I allocate budget across lots by expected surplus.** When I see the full set of lots, I rank them by (my value − estimate). I reserve more of my budget for high-surplus lots and am willing to walk away from low-surplus lots if the price gets close to my value.

**I track who has won previous lots and at what price.** If a rival has been winning at high prices, they may be budget-constrained, and I can let them exhaust themselves. If a rival has been passing, they may be saving budget for a lot they value highly—I should be cautious bidding against them on that lot.

**When my remaining budget is less than my value for the current lot, I bid only what I can afford, not my full value.** The budget is the real constraint, not my value. Bidding more than I have is either impossible or a declaration of bankruptcy.

**I do not chase losses.** If I've lost two or three lots in a row, I do not raise my bids on subsequent lots beyond what the value and budget justify. I simply apply the same rules to the next lot.