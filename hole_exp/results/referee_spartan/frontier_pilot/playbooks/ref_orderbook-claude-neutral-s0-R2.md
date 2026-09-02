---
game: ref_orderbook
model: claude
condition: neutral
seed: 0
round: 2
chars: 2357
---
# ORDER BOOK — my playbook

## Scoring, restated so I never confuse myself again

- Score = (final cash + 3×V) − 190, i.e. **3V − (total I paid)**, minus 8 for each unit I'm short at settlement.
- Therefore the *only* thing that matters is the total cash I spend to end up holding 3. Ticks spent "not overpaying" are worthless if they end with me paying more later.
- Shortfall math: buying a missing unit at price P beats being short whenever **P < V + 8**. With V ≈ 58 that means I should cross up to ~66 rather than deliver short. Being short is rarely the right answer, but overpaying by 10+ is also bad — it's a bounded penalty, not infinite.

## What the value actually was (the big correction)

Across four episodes, settlement V came in at **opening mid + 8, every single time** (mids 49/51/49/51 → V 57/60/57/59). My old belief that "value ≈ the early mid and the rising tape is a manufactured squeeze" was flatly wrong and it cost me three negative scores.

- **The tape drifting up ~2–3 per tick is price discovery toward true value, not bait.** The earliest prices are the cheapest prices I will ever see.
- My working anchor is therefore **V ≈ opening mid + 8 ≈ opening ask + 5**. Opening asks (mid + 2 or 3) are a *bargain* of ~5–6 per unit.
- The one positive score (+12) came from lifting the opening ask on tick 1. All three losers came from resting passive bids for three ticks and then paying 58–61.
- Caveat for a different setup: re-check the drift each game. If prints move *down* from the open, flip this — but until I see that, assume upward drift and buy early.

## Passive bids do not fill

In four episodes my inside-the-spread bids filled **zero** times, across ~10 ticks of waiting. Sellers just re-post above me and the ask ratchets up. Worse, a visible 3-lot bid advertises my obligation and seems to pull asks higher.

- Never post a resting bid and expect it to work. The only legitimate resting order is the **remainder of an aggressive order** that swept the available ask size.
- "Improving my bid by 1" is not a plan; it is a wasted tick that costs ~2–3 in the next ask.

## Tick-by-tick plan

**Tick 1 — buy, hard.** Compute anchor = mid + 8. Post `buy 3 @ (best ask)`. This fills the whole displayed ask size immediately and leaves the balance resting at that price, which is where I want it anyway. If the ask is unus