---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1436
---
# Kuhn Poker Playbook

## Showdown Declarations
- When asked to declare my card at showdown, always reply truthfully with the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to falsely declare.

## Acting as Player 1 (Opening Seat)
- When dealt a **KING**:
  - Always open with `[act: bet]`.
- When dealt a **QUEEN**:
  - Always open with `[act: check]`. Never open bet with a Queen.
  - Facing a bet after checking: default to `[act: fold]`. Only `[act: call]` if there is clear evidence the opponent bluffs frequently with Jacks (standard Nash calls only 1/3 of the time, and always calling is heavily exploitable by value-heavy opponents).
- When dealt a **JACK**:
  - Open with `[act: check]`.
  - Facing a bet after checking: always `[act: fold]`. Never call with a Jack.

## Acting as Player 2 (Responding Seat)
- When opponent opens with `[act: check]`:
  - With a **KING**: always `[act: bet]`.
  - With a **QUEEN**: always `[act: check]`. Never turn a Queen into a bet; take the free showdown.
  - With a **JACK**: `[act: bet]` as a bluff against opponents who fold Queens facing bets; otherwise `[act: check]`.
- When opponent opens with `[act: bet]`:
  - With a **KING**: always `[act: call]`.
  - With a **QUEEN**: default to `[act: fold]`. Calling is -EV against opponents who rarely or never open-bet bluff with a Jack.
  - With a **JACK**: always `[act: fold]`. Never call with a Jack.