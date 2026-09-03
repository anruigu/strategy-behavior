---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1349
---
# Kuhn Poker Playbook

## Showdown Declarations
- When asked to declare my card at showdown, I must always declare truthfully:
  - If dealt Jack: `[show: jack]`
  - If dealt Queen: `[show: queen]`
  - If dealt King: `[show: king]`

---

## As Player 1 (Opening Position)

### Holding King
- When opening the action: `[act: bet]` (Pure value bet).

### Holding Queen
- When opening the action: `[act: check]` (Realize showdown value; betting isolates against King).
- When facing a bet after checking: `[act: fold]` (Default solid fold against standard value/bluff distributions).

### Holding Jack
- When opening the action: `[act: check]` (Baseline check).
- When facing a bet after checking: `[act: fold]` (Jack has zero showdown equity facing a bet; never call).

---

## As Player 2 (In Position / Facing Player 1)

### Opponent Opened with `[act: check]`
- **Holding King**: `[act: bet]` (Pure value bet).
- **Holding Queen**: `[act: check]` (Take free showdown to beat Jack without paying off King).
- **Holding Jack**: `[act: bet]` (Bluff bet; Jack cannot win at showdown, and betting forces Queen to fold).

### Opponent Opened with `[act: bet]`
- **Holding King**: `[act: call]` (Guaranteed win).
- **Holding Queen**: `[act: fold]` (Standard fold to avoid paying off value bets).
- **Holding Jack**: `[act: fold]` (Guaranteed loss on call).