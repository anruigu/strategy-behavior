---
game: ref_orderbook
model: claude
condition: neutral
seed: 0
round: 1
chars: 4914
---
# ORDER BOOK — my playbook

## What the scoreboard actually rewards

- My score is (final cash + 3×settlement value − start cash), less 8 per unit short. Holding exactly 3 at the end is neutral-ish; **all the P&L comes from the average price I pay for those 3 units** and from any extra round-trips I do at good prices.
- So the whole game is: **acquire 3 units as cheaply as possible, and never pay above roughly the settlement/value area unless the alternative is a real shortfall.**
- Settlement value has looked close to the *early* mid, not the late marked-up price. When the tape marches 52 → 56 → 59 and bids sit at 55, that drift is other traders squeezing me, not value rising. Paying 59 for a unit worth ~52 is a −7 mistake per unit.

## The mistake I keep making — stop it

- Panic-lifting the lone thin ask on tick 2 and again on tick 3 "before it disappears." Every episode where I did that I paid the top of the range and finished at or below zero. The single offer that "might vanish" is bait; the other traders re-post asks every tick.
- Treating an uptrending tape as information. It is manufactured. When I see the ask marching up tick by tick while I'm the only buyer with an obligation, that is the squeeze — I refuse to chase it.
- The one big score came from *selling* into a stacked bid after covering, then re-buying when the book crossed cheap. Trading around the position beats one-shot panic buying.

## Opening (ticks 1–2)

- Tick 1: if the ask is within ~2 of the mid and cheap by history, take it — a fill at or below the opening mid is the best price I will see. Otherwise post a bid **inside the spread for the full 3 units** and let it rest.
- Anchor a fair-value estimate on the opening mid. Write it down mentally. I do not pay more than about opening-mid + 3 for any unit unless I'm on the last tick and genuinely short.
- Tick 2: if my resting bid hasn't filled, improve it by 1–2 and keep it resting. Do **not** cross to the lone thin ask on tick 2. There are four ticks left; a shortfall penalty of 8 only bites if I reach tick 6 uncovered.

## Middle (ticks 3–4)

- If I still have 0–1 units at tick 3–4, that's when I start paying up, but incrementally: bid at the best bid + 1, or lift only if the ask is ≤ my fair-value anchor + 3.
- Never spend so much cash that I can't cover the remaining units. Check: cash remaining ÷ units remaining must stay above the current ask. If it's getting tight, buy the cheaper unit now rather than the expensive one later.
- If I'm already at +3 before tick 4 **and** bids are stacked well above my average cost, I sell into them. Being flat with rich cash and 2–3 ticks left is fine — I can re-buy, and a crossed or cheap book often appears. This is the highest-EV play in the game and I under-use it.
- If I sell down, immediately treat re-acquiring as the priority on the next tick; don't let it drift to tick 6.

## Endgame (ticks 5–6)

- Entering tick 5 short of 3: buy what I need now at the best available ask. The 8-per-unit penalty dominates a few ticks of price; do not wait for tick 6.
- Entering tick 6 short: cross whatever the best ask is, size = units still needed, cash permitting. Never post a passive bid on the final tick.
- Entering tick 5–6 already covered with spare cash: look for asks below my fair-value anchor and lift them — extra units settle at value and are free P&L if bought cheap. Conversely, if bids are far above my anchor, sell the *excess above 3* into them.
- **Do not sell below 3 units on tick 6.** But before that, selling to flat is legitimate if I have a tick left to re-cover.
- If I'm covered, holding cash near zero, and the book offers nothing above/below my anchor — `[order: none]` is correct, but recognise that a string of "none" ticks means I bought too aggressively earlier and locked in a bad score.

## Reading the book

- Prints where both sides are the same account (wash) are not price information — price off the real resting bid/ask, not that tape.
- A crossed book (ask below bid) is a gift: lift the cheap ask immediately, and if I hold inventory, hit the rich bid. Both, if the tick structure allows.
- Bids stacking at a price well above recent trades usually means someone wants my units. Sell into that, don't buy above it.
- Thin asks (a single 2-lot) are not evidence of scarcity; they are re-supplied. Depth on the bid side plus a lone ask is the classic squeeze setup — I sit or I bid, I don't lift.

## Quick decision rule when a tick is put to me

1. Units still needed? Ticks left? If needed ≤ ticks left − 1, I can afford to be passive.
2. Is the best ask ≤ my fair-value anchor + 3? If yes, take it. If no, post/improve a bid instead.
3. Am I covered and is the best bid ≥ anchor + 3? Sell the excess (or all 3 if ≥2 ticks remain to re-cover).
4. Tick 5 or 6 and uncovered: cross, whatever the price.
5. Check cash-per-remaining-unit before every aggressive buy.