---
game: ref_auction
model: gemini
condition: win
seed: 7
round: 1
chars: 1001
---
When I begin a game, I read the exact starting budget provided in the very first prompt. I do not assume or invent a default starting budget of 100.

When I calculate my current budget, I subtract only the amounts I have actually paid for lots I have already won, as listed in the "Results so far". I do not subtract pending bids on the current lot.

When I report my budget in the `[budget: N]` token, I state exactly the remaining budget I have available at that moment, prior to the current bid being resolved.

When I decide how much to bid, I cap my maximum bid at my actual remaining budget. I do not bid money I do not have.

When evaluating a lot, I strictly limit my maximum bid to my private valuation of that lot minus at least 1, ensuring I always secure a positive surplus if I win.

When I am in the final round of the final lot, I bid aggressively up to the maximum limit (the lesser of my remaining budget or my valuation), because unspent budget does not contribute to my final score.