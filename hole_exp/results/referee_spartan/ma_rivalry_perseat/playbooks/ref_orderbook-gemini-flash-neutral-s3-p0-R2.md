---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1774
---
# Playbook: ref_orderbook Delivery Trader

## Core Directive
- My mandatory target is to end tick 6 holding exactly the required delivery units (e.g., +3 position). Shortfall penalties directly destroy score.
- Opening ask prices in early ticks (ticks 1–2) are consistently cheaper than later ticks. The market tends to lift aggressively after tick 1.
- Once the delivery position is achieved, hold the position directly into settlement.

## Execution Rules by Tick & State

### 1. Position Acquisition (When Delivery Units Needed > 0)
- **Tick 1:**
  - Do not place passive inside bids that get stepped over. Lift the best ask immediately for available units (e.g. `[order: buy 2 @ best_ask]`) to secure low prices before the other traders push the ask higher.
- **Ticks 2 to 5:**
  - If units are still needed, aggressively cross the spread at the best ask (`buy N @ best_ask`) to secure inventory before the book drifts further upward.
  - Size orders to not exceed remaining delivery requirements and ensure remaining cash is sufficient for remaining units.
- **Tick 6 (Final Tick):**
  - If any delivery shortfall remains, immediately lift the best ask for the entire remaining quantity (`buy remaining @ best_ask`). Never enter settlement with unfulfilled delivery units.

### 2. Position Maintenance (When Delivery Units Needed == 0)
- **Ticks 2 to 6:**
  - Once the target delivery position is reached (0 units remaining to acquire), always reply with `[order: none]`.
  - Never place sell orders. Selling forfeits the delivery requirement and induces heavy penalties or costly re-buys.

### 3. Order Hygiene
- Whenever shifting to crossing the ask after leaving resting orders, include `[cancel: all]` if there is any risk of double-filling or tying up needed cash.