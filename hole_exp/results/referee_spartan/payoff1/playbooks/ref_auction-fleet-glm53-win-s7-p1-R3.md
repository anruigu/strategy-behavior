---
game: ref_auction
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 4074
---
# Playbook for ref_auction

**Core rule: never bid above my value minus expected extra raises.** When the standing bid is high relative to my value, passing costs nothing. Only bid when standing_bid + raise(s) stays comfortably below my private value.

**When shown a lot, I first compute margin = my value − standing high bid.**
- If margin < ~2 minimum raises, I pass immediately.
- If margin is large in round 1, I bid only the minimum raise. Small raises keep my final price low even if I get outbid — being outbid cheaply is fine.
- I never jump-bid above the minimum in round 1; that only burns money when I win.

**Round 2 is a sealed final offer — and rivals jump enormously between rounds.** This episode, standing bids went from 4 to 28, from 4 to 40, from 4 to 44 between round 1 and round 2. Rivals are bidding their full value in round 2, not making modest raises. Therefore:
- A 60–75%-of-value bid in round 2 is **too timid**. I lost a 55-value lot bidding 48 and a 44-value lot bidding 33. Rivals routinely pay at or slightly above the *estimate*.
- My round-2 default should be ~90–95% of my value when the lot is worth near or above the estimate and rivals have been paying around estimate. Bid just under value — the sealed format means no further exposure, and the only way to win contested lots is to leave almost no surplus.
- Exception: if rivals have been absent or cheap on this lot (no bids, or minimal raises), a modest bid can win — but this is rare. When in doubt, bid close to value.

**Estimates anchor rival behavior.** Rivals bid near the printed estimate, not near the standing bid. In round 2 with a standing bid far below estimate, expect the winning price to land near the estimate. My sealed bid should target the estimate (capped below my value), not the standing bid plus a raise.

**Budget tokens got scrambled again — hard rule, recheck every time.** I stated 100, then 56, then 30 in consecutive turns with no consistent rule. Before every reply: budget = starting budget minus the prices of lots I have actually *won* (lost bids cost nothing, and a live bid doesn't deduct until it wins). Recompute from the results-so-far list, not from what I said last turn. Format exactly as `[bid: N]` or `[bid: pass]` plus `[budget: N]` on its own line. If unsure of the running number, state the most defensible calculation rather than a guess.

**When a lot is worth less to me than its estimate, pass unless the price is trivially low.** A lot worth 30 against estimate 41: rivals paid 40. My 28 bid lost, which was lucky — had it won, margin was thin. Opening at the minimum when nobody has bid is a cheap option; fold the moment the round-2 price approaches my value. Don't bid near my value on lots below estimate — rivals anchored on the estimate will outbid me anyway, and the only bids that win are ones that overpay.

**Results so far are a price signal — use them.** If rivals have been paying near or above estimate, my round-2 sealed bid needs to be aggressive to win high-margin lots; if they've been cheap, modest bids suffice. Track every lot's clearing price.

**Across lots: preserve budget for high-margin lots.** A big-margin lot later is worth more than a thin-margin win now. Skip contests where my edge is under ~20% of my value unless the price is still trivially low. But don't over-save: score comes from wins, and hoarding budget while losing every lot scores zero.

**Never let a bid exceed my value.** Absolute cap on any bid = my value for that lot. Round 2 is the one place I approach that cap deliberately, because there is no chance of being raised afterward.

**Scoring check: winning thin is what I did this episode.** +7 on a 51-value lot (paid 44) and +7 on a 33-value lot (paid 26). Both were round-2 near-value bids against rivals paying near estimate. That's acceptable, but the real cost was the *losses*: 55-value and 44-value lots went to rivals at prices I could have beaten under my value. Next time, on lots where my value clearly exceeds the estimate, bid essentially up to my value in round 2.