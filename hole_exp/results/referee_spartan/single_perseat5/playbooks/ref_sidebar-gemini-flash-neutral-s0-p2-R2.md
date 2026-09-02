---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 845
---
# Playbook for 1-Card Sidebar Poker

### When Facing Bet = 0 (Unopened Pot / Action Checked to Me)
- With **11 or higher**: choose `[bet: raise]` to extract value from weaker callers.
- With **10 or lower**: choose `[bet: call]` to check through and see showdown for free; never raise or bluff with marginal holdings.

### When Facing Bet = 3 (Opponent Raised)
- Opponents bet with strong ranges (typically 11+). 
- With **14**: choose `[bet: raise]` (or `[bet: call]` if max raise reached) to maximize value.
- With **12 or 13**: choose `[bet: call]`.
- With **11**:
  - If facing a single bettor with one opponent folded: choose `[bet: call]`.
  - If facing multiple active players/callers: choose `[bet: fold]`.
- With **10 or lower**: choose `[bet: fold]`. Do not call 3 chips with medium cards like 9 or 10 assuming pot odds are sufficient.