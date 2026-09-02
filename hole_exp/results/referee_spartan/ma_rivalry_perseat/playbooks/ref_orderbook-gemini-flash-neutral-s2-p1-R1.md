---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1867
---
# Order Book Strategy Playbook

## Objective & Rules
* My sole mandate is to end the game holding exactly the delivery target (e.g., 3 units) at the lowest possible acquisition cost.
* Shortfall penalty severely destroys score; ending with fewer units than the delivery obligation is never acceptable.
* 3 units is the delivery target, not "excess inventory". Never sell down below the target.

## Early Game (Ticks 1–2): Aggressive Early Fills
* When Tick 1 opens and the best ask is at or below the expected fair value range (e.g., around 49–53), immediately lift the ask by buying whatever quantity is available up to the delivery target: `[order: buy N @ Ask_Price]`.
* Do not waste Tick 1 or Tick 2 resting passive bids inside the spread hoping for fills. The market consistently trends upward as other traders compete for liquidity, making later fills significantly more expensive.
* If units remain to be acquired in Tick 2, prioritize crossing the spread or matching the top ask immediately rather than pennying the bids.

## Mid Game (Ticks 3–4): Complete the Requirement
* If I still need units to reach the delivery target, take the best available ask immediately: `[order: buy N @ Best_Ask]`.
* If a passive bid was previously placed, always include `[cancel: all]` before placing a market-taking buy to prevent unexpected double execution.
* Ensure all required units are acquired by Tick 4 at the latest.

## Late Game (Ticks 5–6): Protect the Target Position
* Once position equals the delivery target, post `[order: none]` and do not place any further orders.
* Never sell inventory if holding exactly the target quantity. Selling at Tick 5 or Tick 6 reopens delivery shortfall risk and gives away the settlement value.
* Only consider selling if position strictly exceeds the required delivery count, and only sell the excess amount above the target.