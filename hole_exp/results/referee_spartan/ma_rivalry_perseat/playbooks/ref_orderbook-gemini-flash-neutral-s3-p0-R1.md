---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1796
---
# Playbook: ref_orderbook Delivery Trader

## Core Directive
- My mandatory target is to end tick 6 with exactly the required delivery units (e.g., +3 position). Shortfall penalties directly destroy score.
- Once the delivery position is achieved, never sell down inventory. Hold the position to settlement.

## Execution Rules by Tick & State

### 1. Position Acquisition (When Delivery Units Needed > 0)
- **Tick 1:**
  - If the ask is relatively tight and within budget, either place an improved inside bid (`buy N @ best_bid + 1`) to capture early liquidity or take available ask liquidity immediately if prices are expected to drift upwards.
- **Ticks 2 to 5:**
  - When resting bids are not filling and other traders are driving the market up, aggressively cross the spread by buying from the best ask (`buy N @ best_ask`) to secure inventory before the book runs away.
  - Size buy orders to only what is needed to reach the target holding, ensuring remaining cash is sufficient for subsequent units.
- **Tick 6 (Final Tick):**
  - If any delivery shortfall remains, immediately lift the best ask for the entire remaining shortfall quantity (`buy remaining @ best_ask`). Never leave an unfulfilled delivery requirement on tick 6.

### 2. Position Maintenance (When Delivery Units Needed == 0)
- **Ticks 4 to 6:**
  - Once the target delivery position is reached (0 units remaining to acquire), always reply with `[order: none]`.
  - Never place sell orders to "lock in cash" or "reduce inventory risk." Selling destroys the delivery requirement, creates shortfall penalties, and forces costly re-buying or outright loss.

### 3. Order Hygiene
- If switching from a passive bidding strategy to crossing the spread, cancel stale resting bids if they risk double-filling beyond cash capacity.