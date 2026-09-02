---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1679
---
# Order Book Playbook

- **Core Goal**: Maintain exactly the required target position into final settlement. Never sell required delivery units just to lock in temporary cash; selling units when delivery is satisfied creates unnecessary re-acquisition risk and crossing costs.
- **Holding Rule**: Once `Delivery: 0 of N units still to acquire` is achieved, do not post any sell orders. Submit `[order: none]` for all remaining ticks unless intentionally rebalancing an excess position above the target requirement.

### Execution & Accumulation

- **Early Ticks (Ticks 1–2)**:
  - When holding 0 units and the spread is wide, place passive buy orders at `best_bid + 1` to step ahead of the queue without paying the full ask.
  - Do not cross the spread immediately on Tick 1 unless the ask is unusually cheap relative to starting cash per unit.

- **Mid Ticks (Ticks 3–4)**:
  - If passive bids have failed to fill and the target delivery is still unfulfilled, cross the spread by lifting the best ask for available size up to the remaining delivery requirement.
  - Always verify that `price * quantity <= cash` before submitting crossing market orders.

- **Late Ticks (Ticks 5–6)**:
  - If `Delivery: K of N units still to acquire` with $K > 0$, immediately lift the lowest available ask(s) up to price $P$ that guarantees an immediate fill of $K$ units.
  - On Tick 6, if still short of the target, cross the spread immediately to avoid shortfall penalty.

### Order Hygiene

- When raising a bid price or switching from passive bidding to an aggressive market lift, always include `[cancel: all]` if resting buy orders could cause accidental overfills beyond available cash.