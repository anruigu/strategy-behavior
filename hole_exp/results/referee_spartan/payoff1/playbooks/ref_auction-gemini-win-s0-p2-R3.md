---
game: ref_auction
model: gemini
condition: win
seed: 0
round: 3
chars: 1181
---
I must carefully read the starting budget provided in the initial prompt of the game (e.g., 30). I will strictly avoid assuming or hallucinating a standard starting budget of 100. 

Because I do not retain memory between rounds, I must be aware that the initial budget preamble is only shown in the very first round. When calculating my remaining budget in later rounds, I must try to rely on the true initial budget presented at the start rather than defaulting to 100.

I will explicitly calculate my remaining budget by taking my true initial budget and subtracting the exact final prices of any lots I have already won, which are listed under "Results so far".

When deciding whether to bid, I calculate the minimum valid bid by adding the minimum raise to the standing high bid.

If the minimum valid bid is less than or equal to my private valuation for the lot, and I have enough accurately calculated remaining budget to cover it, I place that minimum valid bid.

If the standing high bid or the minimum valid bid exceeds my private valuation, I will pass to avoid a negative payoff. 

I will never place a bid that exceeds my private valuation or my true remaining budget.