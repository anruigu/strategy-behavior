---
game: ref_orderbook
model: claude
condition: neutral
seed: 1
round: 1
chars: 3548
---
## My playbook for ref_orderbook (buy-side delivery obligation)

**What the scoreboard actually rewards**
- My score is cash + 3×(settlement value) − starting cash, minus 8 per unit I'm short at the bell. Settlement value has consistently come in *well above* the opening mid — roughly opening mid + 6 to 8. So the opening ask is a bargain and every tick I wait, the market drifts up 2–3 toward true value. Speed of acquisition is the whole game.
- Concretely: if I can own 3 units for ~51–53 each I finish clearly positive; if I average 58–62 I finish flat to negative.

**Opening ticks**
- On tick 1, when I'm shown a tight book and I need N units, I cross immediately: `buy N @ (best ask + 1)`. I do not "improve the bid." Resting a passive bid one tick above the book has never filled for me — the other traders trade with each other above me and I waste the tick while the price runs away.
- If the tick-1 cross only fills part of my requirement (ask depth is usually 2), I cross again on tick 2 for the rest at the new best ask, provided the price is still at or below my value estimate + 8. It almost always is, this early.
- I aim to be fully delivered by tick 2–3. Being flat at tick 3 with three units to buy is the failure mode that produced my worst results.

**Estimating value on the fly**
- My working value estimate is: opening mid + 7, cross-checked against where the tape settles mid-game (the tape flattens near true value by ticks 4–5).
- I'll pay up to my value estimate + 8 rather than take a shortfall, because a missing unit costs me the mark *plus* 8. But I never let that be my plan; it's the emergency price.

**Cash discipline**
- Before any cross, I check: after this fill, do I still have (units still needed) × (best ask + 5) in cash? If not, I size down so my last required unit is always affordable. Ending a tick with 6–20 cash and units still to buy is how I get squeezed.

**Once I hold my full delivery — the rule I broke and must not break again**
- When the screen says "0 of 3 units still to acquire," that reflects my *current* position, not a discharged obligation. If I sell, the requirement comes straight back and I have to buy it again into a rising, thin book at a loss. That single sell turned a flat book into my worst score.
- So: once position = required units, I post `[order: none]` every remaining tick unless I'm adding cheap units I can afford. I never sell inventory I'm required to hold, no matter how attractive the resting bids look.
- I only consider buying *extra* units (beyond the requirement) if the ask is clearly below my value estimate and I have spare cash after reserving nothing — usually I don't, so usually I sit.

**Order syntax habits**
- One order per tick, so I make each one count: crossing orders early, `none` late.
- I add `[cancel: all]` whenever I'm changing my mind on a resting bid, so I don't accidentally get filled twice or leave a stale bid that eats cash I've earmarked.
- I never post a passive bid inside the spread as a "cheaper try" when I still have units to buy and fewer than 4 ticks left — it costs me a tick and the price is higher next time.

**Quick decision table I run each tick**
- Units still needed > 0 and ask ≤ value estimate + 8 → cross for as many as I can afford.
- Units still needed > 0 and ask absurdly high (> value + 8) → cross for as much as keeps me solvent anyway if it's the last two ticks; a shortfall of 8/unit plus the lost mark is worse than overpaying a few points.
- Units needed = 0 → `[order: none]`. Hold to settlement.