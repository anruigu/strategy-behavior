---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 2478
---
# Order Book Strategy Playbook

## Objective & Rules
* My sole mandate is to end the game holding exactly the delivery target (e.g., 3 units) at the lowest possible acquisition cost.
* Shortfall penalty (8 per unit short) destroys score; ending with fewer units than the delivery obligation is never acceptable.
* 3 units is the delivery target, not "excess inventory". Never sell down below the target.

## Pricing Dynamics & Settlement True Value
* The initial tape print at Tick 1 (e.g., trades at ~51–54) reflects true settlement value.
* Ticks 2–3 see an artificial squeeze driven by buyer panic, pushing asks up to 58–61.
* By Ticks 4–6, panic subsides and asks drop back down to fair value (49–54).
* Rushing to lift asks at 58–61 during the peak squeeze in Ticks 2–3 causes negative or zero score. Buying near true value (Tick 1 or patient fills in Ticks 4–6) generates positive score.

## Early Game (Ticks 1–2): Establish Bids, Avoid Panic Chasing
* On Tick 1, if there is no ask or the ask is too wide, place a competitive bid near the Tick 1 trade price (e.g., `[order: buy 3 @ P_tape]`) to capture any early passive fills.
* If an ask exists at or below the initial tape price, lift it immediately: `[order: buy N @ Ask_Price]`.
* On Tick 2, if asks spike sharply above the Tick 1 tape price (e.g., > 55 when tape was 51–52), do not chase by lifting inflated asks. Instead, maintain or adjust resting bids slightly below the inflated asks (e.g., `[order: buy N @ Bid_Price]`).

## Mid Game (Ticks 3–4): Opportunistic Buying
* If asks remain inflated (e.g., >= 58), hold discipline and do not sweep the top of the book. Asks will begin falling back towards true value as buyer demand exhausts.
* When asks re-enter the reasonable range (<= 54–55) or if Tick 4 arrives with units still required, take liquidity: `[cancel: all] [order: buy N @ Best_Ask]`.
* Always include `[cancel: all]` when crossing the spread to avoid accidental overfills from stale resting bids.

## Late Game (Ticks 5–6): Final Execution & Position Protection
* If still short of the delivery target by Tick 5, lift the best available ask immediately to guarantee the requirement is met, as prices drop to near true value in the final ticks.
* By Tick 6, ensure position equals the required delivery target.
* Once the delivery requirement is met (0 units left to acquire), post `[order: none]` and do not place any further orders.
* Never sell inventory if holding exactly the target quantity.