---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 843
---
# Playbook for 1-Card Sidebar Poker

### When Facing Bet = 0 (Unopened Pot / Checks to Me)
- With **11 or higher**: choose `[bet: raise]` to extract value from weaker callers.
- With **10 or lower**: choose `[bet: call]` to check through for free; do not bluff or build pots with marginal holdings.

### When Facing Bet = 3 (Opponent Raised)
- Opponents bet with strong ranges (typically 10+ or high kickers). Calling with marginal cards (9–10) loses chips consistently over time.
- With **12 or 13**: choose `[bet: call]` (or `[bet: raise]` if I hold 14).
- With **11**: 
  - If facing a single bettor with one opponent folded: choose `[bet: call]`.
  - If facing multiple callers/bettors: choose `[bet: fold]`.
- With **10 or lower**: choose `[bet: fold]`. Do not call 3 chips with medium cards like 9 or 10 assuming pot odds are sufficient.