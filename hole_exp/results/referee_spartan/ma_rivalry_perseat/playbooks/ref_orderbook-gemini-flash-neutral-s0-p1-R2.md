---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1577
---
# Playbook: Mandatory Delivery Order Book

### Delivery & Execution Priority
- Never sell below the required delivery threshold (+3) once acquired. Once delivery is fulfilled, do not scalp or sell inventory if it risks or creates a shortfall penalty.
- Early ticks (1–2) consistently offer the lowest ask prices before aggressive demand pushes prices upward. Cross the spread immediately to lift available asks on Tick 1 (buying 2 units at the best ask).
- On Tick 2, immediately cross the spread again to buy the final remaining unit (1 unit at the best ask) rather than waiting or posting passive bids.
- Always include `[cancel: all]` when switching actions or placing follow-up orders if there are any resting orders to ensure clean fills and avoid double commitments.

### Position Management
- When holding `< required units`:
  - On Tick 1: Take up to the full available volume on the best ask to cover delivery shortfall, up to available cash.
  - On Tick 2: Cross the spread for the remaining required unit at the best ask price to lock in delivery obligations early.
  - If unfulfilled by Tick 3–6: Immediately post `[order: buy N @ ask_price]` for all missing units to prevent the shortfall penalty.
- When holding `= required units`:
  - For Ticks 3 through 6, output `[order: none]`.
  - Avoid placing passive or active sell orders that could be filled and reduce holdings below the delivery requirement.
- On Tick 6:
  - If any delivery shortfall remains, take the best available ask immediately.
  - If delivery target is fully satisfied, output `[order: none]`.