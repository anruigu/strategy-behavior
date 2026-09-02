---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1627
---
# Kuhn Poker Playbook

## Showdown Declarations
- When prompted to declare a card at showdown, always declare the exact card dealt to me: `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to misdeclare, as the referee strictly verifies declarations against the deal.

## Seat 1 (Opening / Out of Position)
- **Holding King:**
  - Standard action: `[act: bet]` to extract immediate value.
  - Trap variation: `[act: check]`. If the opponent bets after my check, always reply `[act: call]`.
- **Holding Queen:**
  - Always open with `[act: check]`.
  - If the opponent bets after my check: `[act: fold]`. Folding avoids paying off opponent King value bets and bluff-stabs.
- **Holding Jack:**
  - Open with `[act: check]` as standard play.
  - If the opponent bets after my check: always `[act: fold]`.
  - Optional balanced bluff: open with `[act: bet]` at low frequency to deny equity when checked to, but always fold if faced with resistance.

## Seat 2 (In Position / Facing Action)
- **Facing an Open Bet:**
  - Holding King: always `[act: call]`.
  - Holding Queen: always `[act: fold]` against baseline play. Opponent open bets heavily weight King value.
  - Holding Jack: always `[act: fold]`.
- **Facing a Check:**
  - Holding King: always `[act: bet]` to extract value from Seat 1 checks.
  - Holding Queen: always `[act: check]` behind to take the free showdown and beat Jacks while avoiding a King trap.
  - Holding Jack: `[act: check]` behind to take free showdown, or selectively `[act: bet]` as a bluff only against opponents who consistently fold Queens to delayed bets. Default to `[act: check]`.