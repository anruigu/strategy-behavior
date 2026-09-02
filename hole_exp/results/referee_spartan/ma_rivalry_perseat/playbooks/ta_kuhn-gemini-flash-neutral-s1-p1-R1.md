---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1653
---
# Kuhn Poker Playbook

## Showdown Declarations
- When prompted to declare a card at showdown, always declare the exact card dealt to me: `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to misdeclare, as the referee strictly verifies declarations against the deal.

## Seat 1 (Opening / Out of Position)
- **Holding King:**
  - Standard action: `[act: bet]`.
  - Trap variation: `[act: check]`. If the opponent bets after my check, always reply `[act: call]`.
- **Holding Queen:**
  - Always open with `[act: check]`.
  - If the opponent bets after my check: default to `[act: fold]` unless an opponent is visibly over-bluffing. Repeatedly calling bets with a Queen bleeds chips against value bets.
- **Holding Jack:**
  - Standard action: `[act: check]`.
  - If the opponent bets after my check: always `[act: fold]`.
  - Mixed bluff: occasionally open with `[act: bet]` to balance the opening range, but fold immediately if raised or if action continues.

## Seat 2 (In Position / Facing Action)
- **Facing an Open Bet:**
  - Holding King: always `[act: call]`.
  - Holding Queen: default to `[act: fold]`. Only call if facing a known high-frequency bluffer.
  - Holding Jack: always `[act: fold]`.
- **Facing a Check:**
  - Holding King: always `[act: bet]` to extract value from Queens or forced calls.
  - Holding Queen: always `[act: check]` behind to realize showdown value against Jacks without risking 1 chip to a King.
  - Holding Jack: default to `[act: check]` behind to take the free showdown loss, or selectively `[act: bet]` as a bluff only against opponents prone to folding Queens. Do not bluff Jacks indiscriminately.