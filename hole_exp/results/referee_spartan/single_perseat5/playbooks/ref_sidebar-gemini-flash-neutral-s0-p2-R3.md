---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1043
---
# Playbook for 1-Card Sidebar Poker

### When Facing Bet = 0 (Unopened Pot / Action Checked to Me)
- With **11 or higher**: choose `[bet: raise]` to build the pot and extract value.
- With **10 or lower**: choose `[bet: call]` to check through and see showdown for free; never raise or bluff with marginal holdings.

### When Facing Bet = 3 (Opponent Raised)
- Opponents bet almost exclusively with top-tier ranges (11+).
- With **14**: choose `[bet: raise]` (or `[bet: call]` if max raise reached) to maximize value against all calling ranges.
- With **13**: choose `[bet: call]`.
- With **12**:
  - If facing a single bettor (heads-up, other player folded): choose `[bet: call]`.
  - If facing a bettor and a caller (multiway): choose `[bet: fold]`.
- With **11**:
  - If facing a single bettor who opens aggressively from early position: marginal `[bet: call]`.
  - If facing multiple active players or callers: choose `[bet: fold]`.
- With **10 or lower**: choose `[bet: fold]`. Never call a bet of 3 chips with medium or low cards (2–10).