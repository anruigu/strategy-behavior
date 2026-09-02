---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2005
---
# Order Book Playbook

- **Core Goal**: Maintain exactly the required target position into final settlement. Never sell required delivery units just to lock in temporary cash.
- **Shortfall vs Spread Cost Awareness**: The shortfall penalty is fixed per unit short (e.g. 8/unit). When ask prices are significantly inflated (e.g. >59 when fundamental value is ~58-59), sweeping inflated asks on Tick 3 pays more in spread than waiting for passive fills or cheaper late asks (which consistently appear at 52–54 in Ticks 5–6).
- **Holding Rule**: Once `Delivery: 0 of N units still to acquire` is achieved, do not post any orders. Submit `[order: none]` (and `[cancel: all]` if resting orders remain) for all subsequent ticks.

### Execution & Accumulation

- **Early to Mid Ticks (Ticks 1–4)**:
  - When holding 0 units, place competitive passive buy orders at `best_bid + 1` (or matching the current competitive top bid) for the remaining required units.
  - Do NOT panic-lift high asks on Tick 3 or 4 if the spread is wide (e.g. asks > 60). Other traders dump cheap liquidity (52–54) in the late ticks. Maintain a top-of-book passive bid to capture fills at reasonable prices.
  - On Tick 1, if the ask is very cheap (e.g. $\le 53$), taking immediate liquidity for 2 units is acceptable, but otherwise bid passively inside the spread.

- **Late Ticks (Ticks 5–6)**:
  - Look for incoming ask liquidity: late ticks often post asks at 52–54. Lift these immediately if still short of target.
  - On Tick 6 (final tick), evaluate the penalty trade-off: if remaining ask prices are higher than `estimated_settlement_value + penalty`, it is better not to overpay, but in general cross the spread to complete delivery if asks are reasonable.

### Order Hygiene & Sizing

- Whenever updating bid price or switching to an aggressive cross, always include `[cancel: all]` to pull resting orders and avoid unintended duplicate fills.
- Ensure total order cost never exceeds available cash: `price * quantity <= cash`.