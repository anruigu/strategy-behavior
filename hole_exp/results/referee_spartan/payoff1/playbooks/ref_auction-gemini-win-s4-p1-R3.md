---
game: ref_auction
model: gemini
condition: win
seed: 4
round: 3
chars: 1417
---
I must read the entire conversation history, not just the most recent prompt, to find the exact text "You start with a budget of [X]" in the very first system message or prompt. This tells me my exact starting budget. I never assume a default starting budget like 100, even if the current prompt does not repeat the budget. 

When calculating my remaining budget, I take my exact starting budget (as found in the very first prompt of the conversation) and subtract only the amounts of the lots I have definitively won, as listed in the "Results so far" section. 

Before making any bid, I ensure the bid amount does not exceed my true remaining budget. If my valuation or desired bid is higher than my remaining budget, I can only bid up to my remaining budget. I must never bid more than my starting budget allows.

When I am in round 1 of a lot that is profitable to me, I bid the minimum raise to stay in the auction while keeping the price as low as possible. 

When I am in round 2 of a lot, I recognize this is the final chance to bid. If the lot is worth winning and I have the budget, I bid my maximum valuation (or my total remaining budget, whichever is lower) to secure it. I do not just bid the minimum raise in round 2, as this leaves me vulnerable to being outbid with no opportunity to respond. 

I never place a bid that guarantees a negative profit; my bid must be less than or equal to my valuation.