---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2550
---
# Order Book Strategy Playbook

## Objective & Rules
* My sole mandate is to end the game holding exactly the delivery target (e.g., 3 units) at the lowest possible acquisition cost.
* Shortfall penalty (8 per unit short) destroys score; ending with fewer units than the delivery obligation is never acceptable.
* 3 units is the delivery target, not "excess inventory". Never sell down below the target.

## Pricing Dynamics & Settlement True Value
* The initial tape print at Tick 1 (e.g., trades at ~49–53) reflects true settlement value.
* Ticks 2–3 see an artificial squeeze driven by buyer panic, pushing asks up to 57–60.
* By Ticks 4–6, panic subsides and asks collapse back down to fair value (49–54).
* Rushing to lift asks above fair value (>= 56) causes severe drag on score. Waiting for Ticks 5–6 when asks return to true value (<= 53) produces the highest scores (+9.0 vs +1.0).

## Early Game (Ticks 1–2): Establish Bids, Avoid Panic Chasing
* On Tick 1, if there is no ask or the ask is too wide, place a competitive bid for the full requirement at the Tick 1 trade price (e.g., `[order: buy 3 @ P_tape]`) to capture any early passive fills.
* If an ask exists at or below the initial tape price, lift it immediately: `[order: buy N @ Ask_Price]`.
* On Tick 2, if asks spike sharply above the Tick 1 tape price (e.g., > 55), do not lift asks. Cancel old resting bids and adjust your bid (e.g., `[cancel: all] [order: buy 3 @ Best_Bid+1]`). Always use `[cancel: all]` when updating resting bids to avoid accumulating duplicate orders.

## Mid Game (Ticks 3–4): Patient Holding & Spread Discipline
* Do not panic-lift asks at Tick 3 or Tick 4 if they remain elevated (> 55). The market reliably dumps back to fair value in Ticks 5–6.
* If asks drop to near fair value (<= 54) at Tick 3–4, begin taking liquidity: `[cancel: all] [order: buy N @ Best_Ask]`.
* Otherwise, maintain a bid just below the asks or sit patiently. Do not pay 57–59 out of impatience in Tick 4.

## Late Game (Ticks 5–6): Complete Fills & Freeze Book
* On Tick 5, asks reliably normalize to true value (~50–53). Sweep available asks to fulfill all remaining delivery requirements: `[cancel: all] [order: buy Remaining_Units @ Best_Ask]`.
* On Tick 6, if still short any units, lift the best available ask immediately to guarantee no delivery penalty.
* Once the delivery requirement is fully met (0 units left to acquire), cancel all resting orders and stop trading immediately: `[cancel: all] [order: none]`.
* Never sell inventory if holding the target quantity.