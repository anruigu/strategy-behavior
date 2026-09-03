---
game: ref_auction
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2161
---
When a lot is worth substantially more to me than the standing bid, I bid in small increments — minimum raise plus a little — to keep my price low while staying in the lead.

Remember the auction structure: each lot runs exactly 2 rounds. Round 2 is final — a winning round-2 bid ends the lot, there is no further contest. So a round-2 minimum raise is not "inviting a war," it's the winning move if it tops the standing bid. Bid the minimum raise in round 2 whenever my value clearly exceeds that bid.

Expect opponents to jump hard between rounds (e.g., 6→15, 8→20). Small round-1 opening bids at near-zero get blown past in round 2. In round 1, when my value is far above the estimate, a slightly larger opening bid (10-20% of value rather than the bare minimum) can deter the jump or at least leave me a cheap round-2 raise.

My hard rule for round 2 stands: if the standing high bid is already within about 25% of my value, I pass. Value 19 vs bid 15 was a correct fold — thin margins are near-zero profit. Marginal lots that get contested are not worth chasing; let them go.

Never bid at or above my value, and never raise a lot whose value to me is below the estimate if the bidding is climbing. Below-estimate lots are only worth a cheap round-1 probe; if anyone contests in round 2, I fold immediately.

Track the budget exactly. I started with 30, but mid-episode I reported 100 — a pure bookkeeping error. Recompute every time: stated budget minus amounts I've already committed to wins. When a round-2 raise would be final, check that the bid plus committed spend fits the budget before bidding.

The real score comes from big-gap lots (value far above estimate) won cheap — lot 4 (value 46, won at 24) produced the entire +22. Prioritize those, and take the round-2 win at the minimum raise rather than assuming further bidding.

Losing a lot at a price near my value costs nothing. The only true mistakes are winning thin (paying almost value), paying over value, and losing a big-gap lot by underbidding in the final round. Bid freely when the gap is big, fold fast when it's small, and always take the last-round win at the minimum legal raise.