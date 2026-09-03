---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2652
---
Budget bookkeeping: my budget token must be a real ledger. Start at 30; while a bid of mine is pending, report budget minus that bid (that's what the bid states). If I lose the lot, the money comes back; if I win, the payment sticks. Never report a number I haven't computed from that ledger.

What this episode actually showed:
- Rivals jump hard between rounds: I bid 8, and the standing bid came back at 24. Minimum-raise crawling from a low open does not keep the price low — it just invites a big jump over me. On lots I seriously want, my round-1 bid should already be a meaningful fraction of my value (roughly 40-60% of value or of estimate, whichever I'm anchoring on), so a jump over me is expensive for them.
- Rivals push to near or above the estimate. Lot 1 went at 28 (est 41, value 48 to me — winning at 28 was fine, but my 8-then-28 crawl got outbid-tied and lost). Lot 2 went at 40 above my value 38. Only pass on thin margins there was right.
- My round-2 pass on lot 4 (standing 24, value 32, margin 8 after raise) and the 9 bid on lot 5 both followed the rules, but I still finished with 0. Being timid everywhere yields nothing. With 5 lots and 3 bidders, I must convert at least one good-margin lot, which means bidding assertively early rather than minimum-raising and hoping.
- Bidding exactly the standing high bid plus minimum raise in round 2 (28 on lot 1) can still lose on a tie or get beaten — if I'm going to contest round 2 at all, bid enough to actually win, not one notch above.

Bidding rules:
- Set my ceiling at private value minus a small margin; never bid above value.
- Round 1: open strong enough to discourage jumps — if value is well above the standing bid, bid roughly half my value (or standing + several raises), not the bare minimum. If the standing bid is already near or above my value, pass.
- Round 2 (final): if standing bid plus raise is comfortably below value, decide whether to go to a decisive number — sometimes bid value minus margin outright rather than one minimum raise, since one-notch leads get beaten or tied. If it's within ~20% of my value, pass; rivals push to near estimate and thin margins aren't worth it.
- Don't drain the whole budget on one marginal early lot; but don't hoard it either — an unspent budget at the end of 5 lots scores nothing. If it's the last lot (or last lot that fits my values), be willing to go close to value.
- When I've won a lot, recompute remaining budget before the next bid and preserve enough for one more strong-value opportunity.

If unsure of the budget number, recompute from scratch: 30, minus payments for lots I've won, minus my pending bid.