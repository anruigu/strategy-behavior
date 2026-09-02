---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1322
---
### Kuhn Poker Playbook

#### Always Truthful Showdown
- When asked to declare my card at showdown, I always declare the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

#### Playing as Player 1 (Opening Action)
- When dealt a **King** as opener: I always bet `[act: bet]` for immediate value.
- When dealt a **Queen** as opener: I always check `[act: check]`.
  - When facing a bet after checking with a Queen: I fold `[act: fold]`. *Calling down with a Queen against an opponent who bets primarily for value repeatedly loses chips; do not call.*
- When dealt a **Jack** as opener: I check `[act: check]`.
  - When facing a bet after checking with a Jack: I fold `[act: fold]`.

#### Playing as Player 2 (Facing Opponent Action)
- **When opponent opens with a bet:**
  - If holding a **King**: I call `[act: call]`.
  - If holding a **Queen**: I fold `[act: fold]`. *Do not call bets with a Queen.*
  - If holding a **Jack**: I fold `[act: fold]`.

- **When opponent opens with a check:**
  - If holding a **King**: I always bet `[act: bet]`.
  - If holding a **Queen**: I check back `[act: check]`.
  - If holding a **Jack**: I check back `[act: check]`. *Do not bluff-bet with a Jack when checked to; opponents call with winning cards, turning checking into a guaranteed 1-chip loss instead of 2.*