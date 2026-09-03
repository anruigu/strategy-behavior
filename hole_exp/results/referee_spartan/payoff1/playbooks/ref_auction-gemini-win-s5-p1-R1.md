---
game: ref_auction
model: gemini
condition: win
seed: 5
round: 1
chars: 1163
---
I must carefully read the first prompt to find my exact starting budget. I will not invent or estimate a starting budget, as doing so leads to invalid bids and overspending. 

To determine my remaining budget at any point, I will subtract the total amount I have paid for lots I have already won (as shown in the "Results so far" section) from my exact starting budget. I will ignore lots won by other bidders.

When determining my bid, I will check my remaining budget. I will never bid an amount greater than what I have left.

When considering a lot, I will subtract the standing high bid and minimum raise from my valuation. If I can beat the standing bid while keeping the bid below my valuation and within my remaining budget, I will place a bid. 

When my remaining budget is insufficient to make the minimum raise, or when any valid bid would exceed my valuation for the lot, I will pass by outputting `[bid: pass]`. 

When outputting my budget token, I will always output the remaining budget *before* the current bid is resolved, meaning I do not subtract my current proposed bid from the budget token. I only subtract costs for lots I have already won.