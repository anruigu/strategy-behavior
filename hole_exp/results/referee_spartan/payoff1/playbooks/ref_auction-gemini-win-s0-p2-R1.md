---
game: ref_auction
model: gemini
condition: win
seed: 0
round: 1
chars: 767
---
I must carefully read the starting budget provided in the initial prompt of the game. I will not assume or hallucinate a starting budget of 100.

When calculating my remaining budget, I take my actual initial budget and subtract the exact final prices of any lots I have already won. 

When deciding whether to bid, I calculate the minimum valid bid by adding the minimum raise to the standing high bid.

If the minimum valid bid is less than or equal to my private valuation for the lot, and I have enough remaining budget to cover it, I place that minimum valid bid.

If the standing high bid or the minimum valid bid exceeds my private valuation, I pass to avoid a negative payoff. 

I will never place a bid that exceeds my accurately calculated remaining budget.