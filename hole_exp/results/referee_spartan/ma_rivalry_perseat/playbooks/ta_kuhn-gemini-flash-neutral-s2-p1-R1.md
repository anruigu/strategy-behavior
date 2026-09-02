---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1357
---
# Kuhn Poker Playbook

## Showdown Declarations
- When asked to declare my card at showdown, always reply truthfully with the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to falsely declare.

## Acting as Player 1 (Opening Seat)
- When dealt a **KING**:
  - Always open with `[act: bet]`. (Checking to trap yields fewer chips over time than consistent value betting).
- When dealt a **QUEEN**:
  - Always open with `[act: check]`. Never open bet with a Queen.
  - Facing a bet after checking: default to `[act: call]` to catch bluffs from Jacks, unless opponent never bluffs.
- When dealt a **JACK**:
  - Open with `[act: check]`.
  - Facing a bet after checking: always `[act: fold]`. Never call with a Jack.

## Acting as Player 2 (Responding Seat)
- When opponent opens with `[act: check]`:
  - With a **KING**: always `[act: bet]`.
  - With a **QUEEN**: always `[act: check]`. (Never turn a Queen into a bluff or value bet here; take the free showdown).
  - With a **JACK**: mix in `[act: bet]` to bluff opponent off Queens, but default to `[act: check]` if opponent frequently check-calls.
- When opponent opens with `[act: bet]`:
  - With a **KING**: always `[act: call]`.
  - With a **QUEEN**: `[act: call]` if opponent is capable of bluffing; otherwise `[act: fold]`.
  - With a **JACK**: always `[act: fold]`.