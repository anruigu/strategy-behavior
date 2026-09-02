---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1563
---
# Execution Playbook

### 1. Delivery & Inventory Management
* When I have acquired all required delivery units (e.g. position reaches required target), reply with `[order: none]` and do not place any more orders.
* When I am short of my delivery target, focus exclusively on acquiring the remaining units at the lowest possible total cost.

### 2. Early-Tick Aggression vs. Passive Waiting
* When cheap liquidity appears at the best ask in ticks 1–3, take it immediately rather than trying to penny-jump the bid queue; passive bids frequently get stepped ahead of while the market trends upwards, forcing expensive fills later.
* When the best ask is priced reasonably close to opening levels (or below subsequent market bids), cross the spread right away with `[order: buy N @ best_ask]` up to the delivery requirement.
* Do not wait until ticks 4–6 with zero inventory. Letting the clock run down without fills forces panic-buying at inflated prices (e.g., 58–60) resulting in negative scores.

### 3. Queue & Limit Order Strategy
* When placing a limit buy order on tick 1, do not bid only 1 unit if I need 3; bid for the full initial clip (up to 2–3 units) at or near the best ask.
* When resting bids are bypassed and other traders push the bid higher than my resting price, do not let uncompetitive bids sit—cancel and cross the available ask if the market is trending up.

### 4. Sizing Orders
* When purchasing from the ask book, buy up to the available depth at that price level without exceeding the remaining delivery deficit or available cash budget.