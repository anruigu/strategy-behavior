---
game: ref_auction
model: gemini
condition: win
seed: 0
round: 2
chars: 1151
---
- I will carefully read my starting budget from the initial instructions in the very first turn (e.g., "You start with a budget of X") and use exactly that number. I will never assume a default budget of 100.
- Since the initial instructions are not repeated in later rounds, I will look back at the first prompt or my own previous `[budget: N]` outputs to remember my budget.
- I will calculate my remaining budget strictly as my starting budget minus the total amount I have paid for lots I have already won, or by subtracting the cost of newly won lots from my previous turn's budget.
- I will not subtract active, unresolved bids from my remaining budget. 
- When deciding to bid, I will ensure my proposed bid does not exceed my true remaining budget and does not exceed the value of the lot to me.
- I will bid the minimum required amount (standing high bid plus the minimum raise) to take the lead, provided it is profitable and within my budget.
- If the required minimum bid is higher than my remaining budget or higher than my valuation of the lot, I will pass.
- I will always output my remaining budget accurately in the `[budget: N]` tag.