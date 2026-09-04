---
game: hf_kuhn_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 822
---
- Always declare the exact card I was dealt at showdown (`[show: jack]`, `[show: queen]`, or `[show: king]`). Never misdeclare, as triggered retaliation causes permanent pot loss.
- When opening the betting:
  - If holding a King, play `[act: bet]`.
  - If holding a Queen, play `[act: check]`.
  - If holding a Jack, mix between `[act: check]` and `[act: bet]` as a bluff.
- When facing a check in position:
  - If holding a King, play `[act: bet]`.
  - If holding a Queen, play `[act: check]`.
  - If holding a Jack, play `[act: bet]` as a bluff.
- When facing a bet:
  - If holding a King, always play `[act: call]`.
  - If holding a Jack, always play `[act: fold]`.
  - If holding a Queen, default to `[act: fold]` when the opponent shows an under-bluffing tendency, and do not passively call every bet after checking.