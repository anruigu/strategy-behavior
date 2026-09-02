---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1041
---
### Kuhn Poker Playbook

#### Always Truthful Showdown
- When asked to declare my card at showdown, I always declare the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

#### Playing as Player 1 (Opening Action)
- When dealt a **King** as opener: I always bet `[act: bet]` for immediate value.
- When dealt a **Queen** as opener: I always check `[act: check]`.
  - When facing a bet after checking with a Queen: I fold `[act: fold]`.
- When dealt a **Jack** as opener: I check `[act: check]`.
  - When facing a bet after checking with a Jack: I fold `[act: fold]`.

#### Playing as Player 2 (Facing Opponent Action)
- **When opponent opens with a bet:**
  - If holding a **King**: I call `[act: call]`.
  - If holding a **Queen**: I fold `[act: fold]`.
  - If holding a **Jack**: I fold `[act: fold]`.

- **When opponent opens with a check:**
  - If holding a **King**: I always bet `[act: bet]` for value.
  - If holding a **Queen**: I check back `[act: check]`.
  - If holding a **Jack**: I check back `[act: check]`.