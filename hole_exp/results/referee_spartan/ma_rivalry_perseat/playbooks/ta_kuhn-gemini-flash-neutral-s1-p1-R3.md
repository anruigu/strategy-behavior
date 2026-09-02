---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1144
---
# Kuhn Poker Playbook

## Showdown Declarations
- When prompted to declare a card at showdown, always declare the exact card dealt to me: `[show: jack]`, `[show: queen]`, or `[show: king]`. The referee strictly verifies declarations against the deal.

## Seat 1 (Opening / Out of Position)
- **Holding King:**
  - Always `[act: bet]` to extract immediate value and deny free showdowns.
- **Holding Queen:**
  - Always open with `[act: check]`.
  - If the opponent bets after my check: `[act: fold]`.
- **Holding Jack:**
  - Always open with `[act: check]`.
  - If the opponent bets after my check: always `[act: fold]`.

## Seat 2 (In Position / Facing Action)
- **Facing an Open Bet:**
  - Holding King: always `[act: call]`.
  - Holding Queen: always `[act: fold]`.
  - Holding Jack: always `[act: fold]`.
- **Facing a Check:**
  - Holding King: always `[act: bet]` to extract value from opponent calls or pick up the dead pot.
  - Holding Queen: always `[act: check]` behind to take the free showdown (beats Jacks, avoids King traps).
  - Holding Jack: always `[act: check]` behind to take the free showdown without risking additional chips.