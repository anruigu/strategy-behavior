---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 2318
---
# Delivery Obligation Playbook

## Goal & Target Position
- I must finish Tick 6 holding exactly the required delivery target (e.g., 3 units) to avoid the per-unit shortfall penalty.
- The shortfall penalty is 8 per missing unit; I must avoid overpaying by more than 8 above estimated fair value just to rush fulfillment.
- True settlement value typically falls near the mid-to-late session prices (~52–57). Rushing to buy at peak prices in Ticks 2–3 (e.g., 58–60) destroys value.
- Once my position meets the delivery requirement, I immediately cancel resting orders and submit `[order: none]` for all remaining ticks. I do not speculate beyond my delivery obligation.

## Execution Rules by Phase

### Tick 1: Opening Spread & Passive Bidding
- When the book opens with a spread and low prices, post a passive buy order for 2 units at `best_bid + 1` to capture early maker liquidity.
- If the opening ask is cheap (e.g., ≤ 50), taking 1–2 units directly at the ask is acceptable.

### Ticks 2–3: Controlled Accumulation (Avoid Chasing Spikes)
- Do not blindly lift spike asks at 58–60 when competing traders bid up the book in Tick 2.
- If my Tick 1 passive order was unfilled:
  - If the lowest ask is ≤ 54, cross the spread to take up to 2 units: `[cancel: all] [order: buy N @ best_ask]`.
  - If the lowest ask has spiked to ≥ 57, do not lift it immediately. Instead, place a competitive maker bid: `[cancel: all] [order: buy 2 @ best_bid]` or `best_bid + 1`, letting the initial frenzy settle.

### Ticks 4–5: Filling Inventory on Mean Reversion
- As the early spike subsides in Ticks 4–5, asks frequently drop back to the 52–56 range.
- If still short:
  - Lift the best ask if it is ≤ 56: `[cancel: all] [order: buy N_needed @ best_ask]`.
  - If ask > 56, post a bid at `best_bid` to buy passively.
- By Tick 5, if still needing units, cross the spread to secure delivery unless the ask exceeds fair value + 8 penalty.

### Tick 6: End Game
- If delivery is met: submit `[order: none]`.
- If still short: cross the spread to buy remaining units at `best_ask` provided `best_ask` is within available cash and the shortfall penalty exceeds the premium.

## Order Hygiene
- Always include `[cancel: all]` when replacing an existing resting order with a new order or when standing down after delivery is fulfilled.