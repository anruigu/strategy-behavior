---
game: ref_auction
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 1636
---
When I see a lot with standing bid of 0 and my private value > 0, I open with a small bid equal to the auction's minimum raise (or the minimum acceptable opening) rather than my full value.

When the standing high bid is below my value and the next allowable bid (standing + min raise) is <= my value, I raise to that next allowable bid to conserve budget.

When the next allowable bid would exceed my private value, I pass immediately; do not bid above my valuation.

When the standing high bid already equals or exceeds my private value, I pass; do not enter a bidding war I cannot profitably win.

When I can win cheaply (standing bid well below my value), prefer the minimum raise rather than jumping straight to my value; only bid up to my value if necessary to outbid someone.

When I open a bid, always state the remaining budget correctly and ensure I can afford the bid; do not propose bids that would leave my budget inconsistent or negative.

When deciding in the final round, compute the opponent’s next-minimum exactly and compare it to my value; if my value >= next-minimum, raise to next-minimum, otherwise pass.

When I lose a lot because I underbid early, accept the loss—do not overcompensate later by bidding irrationally on subsequent lots.

When multiple lots remain and my budget is limited, prioritize lots with higher private value-to-price margin and use minimum raises to stretch the budget across more profitable opportunities.

When unsure whether to open on a low-value lot, default to passing unless I can obtain it at a price well below my value (i.e., minimum raise price leaves a clear positive margin).