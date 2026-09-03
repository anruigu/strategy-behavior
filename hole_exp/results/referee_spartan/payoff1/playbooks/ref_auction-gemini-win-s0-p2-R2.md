---
game: ref_auction
model: gemini
condition: win
seed: 0
round: 2
chars: 1090
---
I must carefully read the starting budget provided in the initial prompt of the game (e.g., 30). I will not assume or hallucinate a standard starting budget of 100, even when the budget is not explicitly stated in subsequent rounds. 

To prevent budget hallucinations, I will explicitly state my true initial budget in my reasoning in every single round before calculating my remaining budget. 

When calculating my remaining budget, I take my actual, remembered initial budget and subtract the exact final prices of any lots I have already won. 

When deciding whether to bid, I calculate the minimum valid bid by adding the minimum raise to the standing high bid.

If the minimum valid bid is less than or equal to my private valuation for the lot, and I have enough accurately calculated remaining budget to cover it, I place that minimum valid bid.

If the standing high bid or the minimum valid bid exceeds my private valuation, I pass to avoid a negative payoff. 

I will never place a bid that exceeds my true, accurately calculated remaining budget based on the true initial budget.