---
game: ref_auction
model: gemini
condition: win
seed: 7
round: 2
chars: 1294
---
When the game begins, I find my exact starting budget in the very first prompt (Lot 1, round 1). I must check this first prompt on every subsequent turn to retrieve my true starting budget, rather than ever assuming a default like 100, because the budget instructions are not repeated in later rounds.

When I calculate my current budget, I subtract the exact prices of the lots I have already won (found in the "Results so far" section) from my true starting budget. 

When I submit my decision, I strictly report this calculated remaining budget in the `[budget: N]` token.

When I evaluate a lot, I determine my absolute maximum bid, which is the lower of my true remaining budget and the lot's value to me. I must never bid more than my remaining budget.

When the standing high bid plus the minimum raise exceeds my maximum bid, I output `[bid: pass]`.

When I am in round 1 for a lot I want, I bid the minimum required raise to take the lead without inflating the price too early.

When I am in round 2 (the final round) for a lot I want, I bid strongly and closer to my maximum bid rather than just making the minimum raise. Making only minimum raises in the final round does not work, as it leaves me vulnerable to being outbid by players acting after me with no opportunity to counter.