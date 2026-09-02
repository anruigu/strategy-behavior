---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1515
---
### Playbook

- **Always cancel resting orders when posting new ones**: Include `[cancel: all]` with every active order placement so stale orders do not get filled later and cause unintentional over-accumulation or unwanted fills.
- **Handling early ticks with no asks (Ticks 1–2)**:
  - Post a competitive bid for 1 unit at `top_bid + 1` to establish queue priority: `[cancel: all] [order: buy 1 @ best_bid + 1]`.
- **Pacing acquisitions and price sensitivity**:
  - Do not panic-lift expensive asks in ticks 2–3 (e.g., asks priced at 58–60 when fundamental settlement/tape value is lower around 50–54).
  - When asks appear in ticks 2–3 at high premiums (spread > 3 ticks above initial trades), buy only 1 unit or maintain a competitive bid rather than buying all remaining requirements at once.
  - Later ticks (Ticks 4–6) frequently see supply appear at substantially cheaper prices (e.g., 50–54). Save buying capacity for these later rounds to acquire remaining delivery units at better prices.
  - In ticks 5–6, lift whatever asks are necessary to ensure the delivery obligation of 3 units is fully satisfied before settlement.
- **Once the delivery obligation is met**:
  - Immediately send `[cancel: all] [order: none]`.
  - Do not trade further unless forced to offload accidental excess inventory.
- **Handling accidental overfill**:
  - If position exceeds the delivery requirement at any point, immediately sell excess units by hitting the best available bid: `[cancel: all] [order: sell N @ best_bid]`.