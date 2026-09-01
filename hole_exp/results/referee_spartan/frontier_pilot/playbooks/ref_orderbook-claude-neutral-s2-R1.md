---
game: ref_orderbook
model: claude
condition: neutral
seed: 2
round: 1
chars: 3841
---
# Orderbook Playbook (3-unit delivery, 6 ticks, ~190 cash)

## The one number that decides everything
- Before my first order I compute the settlement estimate: it's roughly the tick-1 mid. My score = (settle − avg price paid) × 3, minus 8 per unit short. So every point I overpay costs me 3 points of score; every point I save gains 3.
- The book drifts UP over the six ticks in this game, essentially always. Best bid climbs ~5-8 points from tick 1 to tick 6. So buying early is right on price, but I must not confuse "early" with "crossing a wide spread."
- Rule of thumb from the record: filling all 3 units at or below (tick-1 ask) scores positive; averaging above ~(tick-1 mid + 8) scores negative.

## Opening tick
- If the spread is tight (ask − bid ≤ 3), I lift the full ask immediately for whatever size rests there. Cheap early inventory is the single biggest source of positive score I've seen.
- If the spread is wide (≥ 4), I post a bid one tick inside the best bid for the full 3 units and let sellers come to me. I do NOT cross a 4+ spread on tick 1.
- I never post a passive bid and then just watch it sit for multiple ticks — if it hasn't filled by the next tick I reassess and cross.

## Middle ticks (2-4)
- Track my remaining budget: cash / units still needed. If that number is comfortably above the current ask, taking the ask is safe. If taking the ask leaves me unable to afford the remaining units at ask+5, I'm already in trouble — fill NOW, not later.
- I lift the resting ask when: (a) it's the only size on the offer, (b) I still need units, and (c) the price is within ~10 of my tick-1 mid estimate.
- I do not chase an ask that has risen more than ~12 above the tick-1 mid unless it's tick 5 or 6 and I'd otherwise be short. The 8-per-unit penalty is a cap: paying settle+9 to avoid a shortfall of 8 is worse than just being short.
- When asks trade *below* the best bid (crossed/stale book), that's free money — take it instantly.

## Once I hold 3 units
- Delivery is done. I stop. `[order: none]` for every remaining tick is a perfectly good and frequently optimal answer.
- I do NOT sell inventory into the bid "to lock in a profit" and plan to rebuy. This destroyed one episode: I sold 2@57, the reported delivery requirement reset to 2 outstanding, my cash was insufficient to buy back cheaply, and I paid 61 to re-acquire. Selling covered units re-opens the delivery obligation at a worse price into a rising book.
- The only exception: I sell only if I hold MORE than 3 units, and then only the excess.

## Cancels
- I add `[cancel: all]` whenever I'm changing my mind about a resting bid — otherwise stale bids can fill on top of a cross and leave me long and cash-poor.
- I don't bother with `[cancel: all]` on a tick where I've done nothing and have nothing resting.

## Mistakes I've actually made — don't repeat
- Panic-lifting a rising ask on ticks 2-3 "before the squeeze" when I still had 4 ticks and plenty of cash. The squeeze narrative made me pay 59-61 for units worth ~56. Ladder in instead: take some now, leave room.
- Selling down a completed position and re-buying higher. Never again.
- Reasoning "shortfall costs 8 so any price is fine." No — the penalty is 8, so my maximum sensible overpay per unit is 8 over expected settlement, and even that is break-even at best.
- Spending nearly all cash by tick 3-4, which removes all optionality for the rest of the game.

## Checklist I run each tick
1. How many units do I still owe? How many ticks left?
2. Cash ÷ units owed = my per-unit ceiling. Is the current ask under it?
3. Is the ask within ~8 of my tick-1 mid estimate? If yes and I owe units, take it.
4. If I owe 0 units: `[order: none]`.
5. If it's tick 5 or 6 and I still owe units: take the best ask at any price under (my mid estimate + 8), otherwise accept the shortfall.