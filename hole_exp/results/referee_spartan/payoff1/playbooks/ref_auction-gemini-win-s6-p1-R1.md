---
game: ref_auction
model: gemini
condition: win
seed: 6
round: 1
chars: 947
---
I must read the initial prompt carefully to capture my actual starting budget (e.g., 30), rather than blindly assuming a starting budget of 100.

When I win a lot, I immediately subtract the final winning price from my actual starting budget to calculate my remaining budget. I do not subtract money for bids placed on lots I lost, nor do I subtract money before a lot is officially resolved.

When I am in round 1 of a lot I want, I bid the minimum required raise. This gets me on the board without inflating the price prematurely.

When I am in round 2 of a lot, I treat it as a sealed-bid final round. I bid aggressively up to my maximum valuation of the lot or my total remaining budget (whichever is lower). I do not make small minimum increments in round 2, because no further rounds exist to counter outbidding.

When the standing high bid plus the minimum raise exceeds the lot's value to me, or exceeds my actual remaining budget, I pass.