---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1462
---
# Playbook: Mandatory Delivery Order Book

### Delivery & Execution Priority
- Never sell below the required delivery threshold (+3) once acquired. Shortfall penalties severely penalize under-delivery relative to settlement value.
- Early ticks (1–2) consistently offer the lowest ask prices before aggressive demand pushes prices upward. Cross the spread immediately to lift available asks on Tick 1 (buying available volume up to the delivery requirement at the best ask).
- On Tick 2, immediately cross the spread again to buy the final remaining unit(s) at the best ask rather than waiting or posting passive bids.
- Always include `[cancel: all]` when transitioning actions or placing orders if there are any resting orders on the book.

### Position Management
- When holding `< required units`:
  - Tick 1: Post `[order: buy N @ best_ask]` for the available volume on the best ask up to the required delivery amount.
  - Tick 2: Post `[cancel: all] [order: buy N @ best_ask]` for all remaining units needed to satisfy the delivery requirement.
  - Ticks 3–6 (if any delivery units still needed): Immediately cross the spread with `[cancel: all] [order: buy N @ best_ask]` to eliminate the shortfall.
- When holding `= required units`:
  - From Tick 3 through Tick 6, output `[cancel: all] [order: none]`.
  - Do not post speculative sell or buy orders; hold the full inventory directly into settlement to guarantee positive returns and avoid penalty risk.