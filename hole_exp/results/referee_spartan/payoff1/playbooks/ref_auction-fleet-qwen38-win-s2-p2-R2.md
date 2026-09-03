---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2387
---
# Playbook

**Budget discipline is non-negotiable and the first thing I verify.** I read the starting budget from the problem statement and use that exact number. I never substitute a different figure based on assumption or habit. Before every bid, I calculate remaining budget as: starting budget minus the sum of all prices I paid for lots I've won. I write that number down. If my remaining budget is less than the minimum raise, I pass. I never declare a budget figure I haven't derived this way from the stated starting budget.

**Never bid above my private value for a lot.** This is a hard ceiling. If a lot is worth 35 to me, I never bid 36 or higher regardless of the round or the competition.

**In round 1 of a two-round lot, I bid the minimum raise only if my value exceeds the current high bid by at least twice the minimum raise.** This keeps me in the auction at low cost while preserving budget for the final round. If the surplus is thin, I pass in round 1 and wait.

**In round 2 (the final round), I bid the minimum raise if I want the lot, provided the minimum raise is at or below my value.** The minimum raise is the lowest price that wins. Bidding anything higher only reduces my surplus for no strategic benefit—if a rival outbids me, I lose regardless; if they don't, I've just overpaid. I do not use "value minus margin" as my round-2 bid; that is a mistake that gives away surplus for free.

**I allocate budget across lots by expected surplus.** When I can see the set of lots, I rank them by (my value − current price level). I reserve budget for high-surplus lots and am willing to walk away from low-surplus lots if the price gets close to my value.

**I track who has won previous lots and at what price.** If a rival has been winning at high prices, they may be budget-constrained, and I can let them exhaust themselves. If a rival has been passing, they may be saving budget for a lot they value highly—I should be cautious bidding against them on that lot.

**When my remaining budget is less than my value for the current lot, I bid only what I can afford.** The budget is the real constraint. If the minimum raise exceeds my remaining budget, I pass.

**I do not chase losses.** If I've lost two or three lots in a row, I do not raise my bids on subsequent lots beyond what the value and budget justify. I simply apply the same rules to the next lot.