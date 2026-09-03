---
game: ref_auction
model: gemini
condition: win
seed: 1
round: 1
chars: 996
---
I will always read the prompt carefully to find my exact starting budget, rather than assuming a default amount like 100.
When calculating my remaining budget, I subtract only the final closing prices of lots I have explicitly won (as listed in "Results so far") from my starting budget.
I will not subtract amounts for active bids, and I will not subtract amounts for lots won by other bidders. 
I will output my exactly calculated remaining budget in the `[budget: N]` token on every turn.
I will never make a bid that exceeds my actual remaining budget.
I will never bid more than a lot is worth to me.
When it is the first round of a lot, I will bid the minimum raise if the lot is profitable, to test the waters without committing too much of my budget.
When it is the final round of a lot, I will bid up to my maximum profitable amount or my remaining budget limit (whichever is lower) to secure the lot.
I will always ensure my bid is at least the standing high bid plus the minimum raise.