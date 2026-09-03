---
game: ref_auction
model: gemini
condition: win
seed: 5
round: 2
chars: 1600
---
When I start a new game, I read the exact starting budget provided in the initial prompt. Because the starting budget is not repeated in later rounds, in every single turn I must explicitly look back at the very first prompt to find my true starting budget. I will never assume a default starting budget of 100, as doing so leads to invalid bids and severe miscalculations.

When I calculate my remaining budget, I take my actual starting budget (found in the first prompt) and subtract the exact amounts I paid for any lots I have already won (as explicitly listed in the "Results so far" section of the current prompt). I do not subtract bids for lots that are still ongoing or lots won by other bidders.

When choosing a bid, I strictly cap my maximum bid at my mathematically verified remaining budget. I never bid higher than my available funds, regardless of how high my private valuation of the lot is.

When I am in the first round of bidding for a lot, I bid the minimum raise (if the current bid plus raise is below my valuation and budget) to establish a position without needlessly driving up the price.

When I am in the final round of bidding for a lot, I evaluate my private value and my remaining budget. I bid the maximum amount I am willing to pay (my private valuation), strictly capped by my remaining budget, to maximize my chances of securing the item for a profit. 

When formatting my response, I output exactly the tokens `[bid: N]` (or `[bid: pass]`) and `[budget: N]`, ensuring the budget token contains my mathematically verified remaining budget, not a fabricated number.