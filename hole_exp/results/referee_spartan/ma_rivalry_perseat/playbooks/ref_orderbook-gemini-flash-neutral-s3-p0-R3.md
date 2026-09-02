---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1727
---
# Playbook: ref_orderbook Delivery Trader

## Core Directive
- My mandatory target is to end tick 6 holding exactly the required delivery units (e.g., +3 position). Shortfall penalties directly destroy score.
- Opening ask prices in early ticks (ticks 1–2) are consistently the cheapest in the game. Other participants aggressively bid up the book immediately after tick 1.
- Acquire required delivery units as fast as possible across the first 1–2 ticks, then hold the position directly into settlement.

## Execution Rules by Tick & State

### 1. Position Acquisition (When Delivery Units Needed > 0)
- **Tick 1:**
  - Do not place passive inside bids that get stepped over. Immediately lift the best ask for the maximum available units up to the required delivery amount (`[order: buy N @ best_ask]`, e.g., `buy 2 @ ask_price`).
- **Tick 2:**
  - Complete the delivery target immediately by crossing the spread at the best ask for the remaining units (`[order: buy remaining @ best_ask]`).
- **Ticks 3 to 6:**
  - If any delivery shortfall remains for any reason, immediately cross the best ask (`[order: buy remaining @ best_ask]`). Never enter settlement with unfulfilled delivery units.

### 2. Position Maintenance (When Delivery Units Needed == 0)
- **Ticks 2 to 6:**
  - As soon as the target delivery position is reached (0 units remaining to acquire), always reply with `[order: none]`.
  - Do not place sell orders, speculate on late dips, or attempt market-making. Holding the required position to settlement locks in positive score.

### 3. Order Hygiene
- Whenever switching tactics or if a previous order failed to fill, include `[cancel: all]` alongside the new order to prevent unwanted fills or tied-up cash.