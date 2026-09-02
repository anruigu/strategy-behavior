---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2519
---
# Delivery Obligation Playbook

## Goal & Target Position
- I must finish Tick 6 holding exactly the required delivery target (e.g., 3 units) to avoid the per-unit shortfall penalty (8 per missing unit).
- True settlement value typically falls near the mid-to-late session prices (~52–57). Never rush to buy at peak prices in Ticks 2–5 (e.g., ≥59) because overpaying by 6–8 above settlement is worse than or equal to the shortfall penalty and waiting for Ticks 5–6 mean reversion yields lower prices (52–54).
- Once my position meets the delivery requirement, I immediately cancel resting orders and submit `[order: none]` for all remaining ticks. I do not speculate beyond my delivery obligation.

## Execution Rules by Phase

### Tick 1: Opening Spread & Passive Bidding
- When the book opens with a wide spread and low prices (e.g., bids ~48–50, asks ~53–54), post a passive buy order for 2 units at `best_bid + 1` to capture early maker liquidity.
- If the opening ask is exceptionally cheap (e.g., ≤ 50), taking 1–2 units directly at the ask is acceptable.

### Ticks 2–3: Controlled Accumulation (Never Chase Spikes)
- Do not lift asks when prices spike to ≥58 during the early frenzy.
- If my previous passive order was unfilled:
  - If the lowest ask is ≤ 54, cross the spread to take up to 2 units: `[cancel: all] [order: buy N @ best_ask]`.
  - If the lowest ask is ≥ 57, post a competitive maker bid at `best_bid`: `[cancel: all] [order: buy 2 @ best_bid]`.

### Ticks 4–5: Securing Units as Market Cools
- As the spike subsides in Ticks 4–6, asks drop back down to 52–56.
- If still short:
  - In Tick 4: If ask ≤ 58, taking 2 units or posting a competitive bid at `best_bid` is effective. Do not pay >58.
  - In Tick 5: If best ask ≤ 57, take the needed units at `best_ask` (`[cancel: all] [order: buy N_needed @ best_ask]`). If best ask is still high (≥59), DO NOT panic-sweep at 59–60; post at `best_bid` or hold off, because Tick 6 consistently brings asks down to 52–54.

### Tick 6: Final Clean-up
- If delivery is met: `[cancel: all] [order: none]`.
- If still short: cross the spread to buy remaining units at `best_ask` (`[cancel: all] [order: buy N_needed @ best_ask]`). Final tick asks are reliably favorable (52–54).

## Order Hygiene
- Always include `[cancel: all]` when replacing an existing resting order with a new order or when standing down after delivery is fulfilled.
- Ensure order size never exceeds remaining delivery units needed unless deliberate accumulation strategy requires it.