---
game: ref_orderbook
model: claude
condition: neutral
seed: 0
round: 3
chars: 4309
---
# ORDER BOOK — my playbook

## Scoring, restated so I never confuse myself again

- Score = (final cash + 3×V) − 190, i.e. **3V − (total I paid for my 3 units)**, minus 8 for each unit I'm short at settlement.
- The only thing that matters is **the total cash I spend to end up holding exactly 3**. Every tick I spend "not overpaying" is worthless if it ends with me paying more later.
- Shortfall math: buying a missing unit at price P beats being short whenever **P < V + 8**. With V ≈ 57–60 that means crossing up to ~65 still beats delivering short. Never deliver short.
- **Units beyond 3 are not free money.** Confirmed by episode 1: I bought 2 extra at 55, held them, then dumped them at 55 for zero PnL and pure risk. Marking of surplus units is unproven; treat position >3 as speculation, not as scoring.

## What the value actually is

Across eight episodes now, settlement V has tracked **opening mid + 8** (mids ~47–51.5 → V ~57–60). The anchor holds.

- **The tape drifting up ~2–3 per tick is price discovery toward true value, not bait.** The earliest prints are the cheapest prices I will ever see.
- Working anchor: **V ≈ opening mid + 8 ≈ opening best ask + 5–6**. The tick-1 ask is a bargain of roughly 5–6 per unit.
- Re-check drift each game. If prints move *down* from the open across ticks 1–2, flip the plan and buy late/passively. Until I see that, assume upward drift.

## Passive bids do not fill

Inside-the-spread resting bids have essentially never filled for me. Sellers re-post above me and the ask ratchets up. A visible 3-lot bid also advertises my obligation.

- Never post a resting bid and expect it to work. The only legitimate resting order is the **remainder of an aggressive order** that swept the displayed ask size.
- "Improving my bid by 1" is a wasted tick that costs ~2–3 in the next ask.

## Tick-by-tick plan (the version that scores +13)

**Tick 1 — buy hard.** Anchor = mid + 8. Post `buy 3 @ best ask` (or best ask + 1 if the ask looks thin — the +1 costs at most 1 and increases the chance of clearing more size; in ep. 4 `buy 3 @ 50` against a 49 ask still filled 2 @ 49). Typical fill: 2 units at the ask. Leftover 1 rests.

**Tick 2 — finish the job.** I will normally be at +2 with 1 to go and the ask now ~6–8 higher. **Take it anyway.** Cancel the stale rest and `buy 1 @ best ask`. Paying 56–57 for the last unit is correct: the alternative is 58–60 on tick 4 or a −8 penalty. This has never been the wrong call.

**Ticks 3–6 — do nothing.** Once position = 3 and delivery shows 0 to acquire, the score is locked in. Reply `[order: none]`.
- Do not buy extras "because the ask is below my anchor." My two best scores (+13, +13… and the flat +10s) all came from stopping at 3; the one time I bought extras I round-tripped them for zero and added variance.
- Do not sell. Selling puts me short into a V+8 penalty; no bid near V compensates.
- On the final tick add `[cancel: all]` as hygiene so nothing stale can fill.

## Expected shape of a good game

- Fill 2 @ ~opening ask on tick 1, 1 @ ~mid+8 on tick 2, average cost ~52–56, V ~57–60 → **+10 to +14**.
- Anything under +8 means I paid too much on tick 1 or waited. Anything negative means I went passive or went short.

## Cheap improvements to test next time (only one per game, and only on tick 1)

1. **Bid above the ask on tick 1** — e.g. `buy 3 @ ask + 3`. If the matching engine fills me at the resting ask price (price-time priority), this sweeps deeper size at no extra cost and could get all 3 units done at ~49–54, worth several extra points. If instead I get filled at my own limit, I lose ~3 per unit — a bounded, affordable experiment.
2. If tick 1 leaves me at +2 and tick-2 asks are *below* my tick-1 fill price, just take them; a down-drifting tape is the one case where patience would have paid.

## Rules I will not break

- Always end holding exactly 3. Check the "Delivery: N of 3 still to acquire" line every tick; it is the ground truth.
- Never let ticks 5–6 arrive with units still to buy. If at tick 4 I am still short, cross whatever the ask is, up to anchor + 8.
- Keep cash irrelevant to the decision — negative cash is fine mid-game as long as I end at exactly 3 units; but don't manufacture negative cash buying surplus.
- Every reply ends with the bracketed token.