---
game: ref_auction
model: gemini
condition: win
seed: 0
round: 3
chars: 1423
---
- I will carefully read my starting budget from the initial instructions in the very first turn (e.g., "You start with a budget of X") and use exactly that number. I will never assume a default budget of 100.
- Since the initial instructions are not repeated in later rounds, I will look closely at my most recent `[budget: N]` output from my previous turns to remember my exact remaining budget. 
- I will never claim my budget wasn't provided, as it is always provided in the first turn's instructions and preserved in my own previous outputs.
- I will calculate my remaining budget strictly as my starting budget minus the total amount I have paid for lots I have already won.
- I will track won lots accurately by reading the "Results so far" section in the prompt. If I have not won any lots, my remaining budget is identical to my starting budget.
- I will not subtract active, unresolved bids from my remaining budget. 
- When deciding to bid, I will ensure my proposed bid does not exceed my true remaining budget and does not exceed the value of the lot to me.
- I will bid the minimum required amount (standing high bid plus the minimum raise) to take the lead, provided it is profitable and within my budget.
- If the required minimum bid is higher than my remaining budget or higher than my valuation of the lot, I will pass.
- I will always output my exact remaining budget accurately in the `[budget: N]` tag.