---
game: ref_auction
model: gemini
condition: win
seed: 1
round: 3
chars: 1227
---
I will look back at the very first message of the episode to find my exact starting budget (stated explicitly as "You start with a budget of X"). I will NEVER assume a default starting budget like 100.
When calculating my remaining budget, I will subtract only the final closing prices of lots I have explicitly won (as listed in "Results so far") from my exact starting budget found in the first message.
I will not subtract amounts for active bids, and I will not subtract amounts for lots won by other bidders. 
I will output my exactly calculated remaining budget in the `[budget: N]` token on every turn.
I will never make a bid that exceeds my actual remaining budget. If the minimum required bid exceeds my remaining budget, I will pass.
I will never bid more than a lot is worth to me.
When it is the first round of a lot, I will bid the minimum raise if the lot is profitable and within my budget, to test the waters without committing too much.
When it is the final round of a lot, I will bid up to my maximum profitable amount or my remaining budget limit (whichever is lower) to secure the lot.
I will always ensure my bid is at least the standing high bid plus the minimum raise, provided I have the budget for it.