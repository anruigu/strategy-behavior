---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1211
---
### Playbook

- **Always cancel resting orders when posting new ones**: Include `[cancel: all]` with every active order placement so stale bids do not get filled later and cause unintentional over-accumulation and negative cash balances.
- **Acquire required units early and incrementally**:
  - When the delivery target is not yet met and there are asks resting at or near the current fair market price, take 1 unit directly by lifting the lowest ask `[order: buy 1 @ ask_price]`.
  - Avoid posting passive resting bids inside the spread across multiple ticks; aggressive competitors step in front and market movements will force expensive crossing later.
  - Buy steadily 1 unit per tick over early ticks (Ticks 1–4) rather than trying to bulk-buy in a single tick or waiting until Ticks 5–6 when ask prices have drifted higher.
- **Once the delivery obligation is met**:
  - Immediately send `[cancel: all] [order: none]`.
  - Do not trade further unless forced to offload accidental excess inventory.
- **Handling accidental overfill**:
  - If position exceeds the delivery requirement at any point, immediately sell excess units by hitting the best available bid `[cancel: all] [order: sell N @ best_bid]`.