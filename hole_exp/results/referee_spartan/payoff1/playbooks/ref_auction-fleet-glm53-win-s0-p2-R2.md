---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2315
---
- Budget bookkeeping is my biggest failure point: I repeatedly stated wrong numbers (30, then 75, then 25, then 0 — all in the same session). Before every reply, recompute budget as starting budget minus the sum of bids I actually WON (lost bids cost nothing), and state only that number. If I don't remember the starting budget exactly, track it relative to my last correct statement plus any wins since.
- When a lot is put to me, I read my private value V and the standing bid S. My rule: bid the minimum raise as long as the new bid is at most V minus a small margin (about 10% of V); otherwise pass.
- I never bid above my private value. Winning at just under value is barely better than losing, and overpaying is strictly bad.
- Raise by the minimum increment each time, not by large jumps. Minimum raises keep my final price low and cost nothing since the opponent gets only two rounds to respond.
- When I hold the high bid going into the final round and no one raises, I win at my own number — so keep my own bids as low as the minimum raise allows.
- On the opening round of a fresh lot with no bids, open at exactly the minimum raise rather than jump bidding.
- If the standing bid in the final round is already within one minimum raise of my value, I pass instead of raising — this worked well (lots 2 and 4: passing at/above V kept my score positive).
- The V−5 cutoff rule worked: on lot 3 the minimum raise took me to 43 against V=47, within 5 of value, and passing was correct — the winner paid 39, leaving me almost nothing if I'd pushed to win.
- Minimum raises in round 1 still invite opponents to leapfrog me massively in round 2 (bidder 1 jumped from 23 to a standing 44+ repeatedly). Expect the round-2 standing bid to often land at or near the estimate; my profit comes from lots where my V is well above the estimate, so I should commit budget mainly to those.
- I do not shade my budget downward to fake scarcity — my stated budget is a fact I must keep accurate, not a signal.
- Passing on a lot where the price exceeds my value is a win, not a loss; there are several lots and opponents overpaying them is good for me.
- One clean win at well under value (lot 1: V=42, paid 25, +17) carried my whole score. Prioritize grabbing one or two cheap lots early rather than fighting every round.