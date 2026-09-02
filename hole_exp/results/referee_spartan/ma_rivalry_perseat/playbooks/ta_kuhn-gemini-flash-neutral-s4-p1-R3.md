---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1022
---
# Kuhn Poker Playbook

## Showdown Declarations
- When asked to declare my card at showdown, always declare the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to falsely declare.

## First Acting Seat (Opener)
- When dealt a **King** as opener: reply `[act: bet]`.
- When dealt a **Queen** as opener: reply `[act: check]`.
  - When facing a bet after checking a Queen: reply `[act: fold]`.
- When dealt a **Jack** as opener: reply `[act: check]`.
  - When facing a bet after checking a Jack: reply `[act: fold]`.

## Second Acting Seat (In Position)
- **When the opponent bets out:**
  - Facing a bet with a **King**: reply `[act: call]`.
  - Facing a bet with a **Queen**: reply `[act: fold]`.
  - Facing a bet with a **Jack**: reply `[act: fold]`.
- **When the opponent checks to me:**
  - With a **King**: reply `[act: bet]`.
  - With a **Queen**: reply `[act: check]` to realize showdown value against Jacks without risking an extra chip.
  - With a **Jack**: reply `[act: check]`.