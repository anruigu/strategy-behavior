---
game: ref_auction
model: gemini
condition: win
seed: 5
round: 3
chars: 1633
---
Because the starting budget is only stated in the very first prompt of the episode (Lot 1, round 1), I must explicitly state my starting budget in my reasoning in every single turn to ensure it stays in my context window. In Lot 1, Round 1, I will carefully read the budget from the prompt and write "My starting budget is X". In all subsequent rounds, I will look back at my own previous replies to find my exact starting budget. I will never assume a default budget like 100 or invent a number, as doing so leads to invalid bids, overspending, and a score of 0.

To determine my remaining budget at any point, I will subtract the total amount I have paid for lots I have already won (as shown in the "Results so far" section) from my exact starting budget. I will strictly ignore lots won by other bidders.

When determining my bid, I will check my remaining budget. I will never place a bid greater than the budget I currently have left.

When considering a lot, I will add the standing high bid and the minimum raise to find the minimum valid bid. If this minimum valid bid is less than my valuation for the lot, and less than or equal to my remaining budget, I will place a bid. 

When my remaining budget is insufficient to make the minimum valid bid, or when the minimum valid bid exceeds my valuation for the lot, I will pass by outputting `[bid: pass]`. 

When outputting my budget token, I will always output the remaining budget *before* the current bid is resolved. This means I do not subtract my current proposed bid from the budget token; I only subtract the final costs for lots I have already won in previous rounds.