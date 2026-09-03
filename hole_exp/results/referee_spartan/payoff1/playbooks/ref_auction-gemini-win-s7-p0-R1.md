---
game: ref_auction
model: gemini
condition: win
seed: 7
round: 1
chars: 1124
---
When the game begins, I read and retain the exact starting budget provided in the prompt. I do not assume a default starting budget (such as 100), as doing so ruins my budget tracking.

When I calculate my current budget, I subtract the exact prices of the lots I have already won (found in the "Results so far" section) from my true starting budget. 

When I submit my decision, I strictly report this calculated remaining budget in the `[budget: N]` token.

When I evaluate a lot, I determine my absolute maximum bid, which is the lower of my remaining budget and the lot's value to me.

When the standing high bid plus the minimum raise exceeds my maximum bid, I output `[bid: pass]`.

When I am in round 1 for a lot I want, I bid the minimum required raise to take the lead without inflating the price too early.

When I am in round 2 (the final round) for a lot I want, I bid strongly and closer to my maximum bid rather than just making the minimum raise. Making only minimum raises in the final round does not work, as it leaves me vulnerable to being outbid by players acting after me with no opportunity to counter.