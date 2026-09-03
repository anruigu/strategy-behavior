---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1718
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
- When opening the action: `[act: bet]` (Value bet to build pot / extract chips).

### Holding Queen
- When opening the action: `[act: check]` (Do not bet; betting folds worse hands and isolates against King).
- When facing a bet after checking:
  - `[act: fold]` as the default baseline against aggressive/value-heavy opponents to avoid leaking chips to King value bets.
  - Do not blindly call every bet with Queen; overcalling Queen into opponent bets was the primary leak leading to heavy negative scores.

### Holding Jack
- When opening the action:
  - Standard/defensive line: `[act: check]`.
  - Bluffing line: Mix in `[act: bet]` at a low frequency to balance opening ranges.
- When facing a bet after checking: `[act: fold]` (Never call with Jack facing a bet).

---

## As Player 2 (In Position / Facing Player 1)

### Opponent Opened with `[act: check]`
- **Holding King**: `[act: bet]` (Pure value bet).
- **Holding Queen**: `[act: check]` (Take free showdown to realize equity against Jack without paying off a trap).
- **Holding Jack**: `[act: bet]` (Pure bluff; Jack has zero showdown value, and betting consistently steals pots from Queen checks).

### Opponent Opened with `[act: bet]`
- **Holding King**: `[act: call]` (Guaranteed win).
- **Holding Queen**: `[act: fold]` (Unless opponent is confirmed over-bluffing, Queen folds facing an open bet).
- **Holding Jack**: `[act: fold]` (Guaranteed loss on call).