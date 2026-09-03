---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1654
---
# Kuhn Poker Playbook

### Showdown Declarations
- When asked to declare my card at showdown, I always declare my exact card truthfully: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

### In Position (Player 2 / Second to Act)

- **Facing a Check:**
  - When holding **KING**, I always bet for maximum value: `[act: bet]`. Never check behind with a King.
  - When holding **JACK**, I always bet as a bluff: `[act: bet]`. Never check behind with a Jack because it has zero showdown equity and betting forces folds from Queens.
  - When holding **QUEEN**, I always check behind to realize showdown value against Jacks without paying off Kings: `[act: check]`.

- **Facing a Bet:**
  - When holding **KING**, I always call: `[act: call]`.
  - When holding **JACK**, I always fold: `[act: fold]`. Calling with a Jack is never profitable.
  - When holding **QUEEN**, I default to folding: `[act: fold]`. Only consider calling if the opponent has a proven, highly aggressive bluffing frequency.

---

### Out of Position (Player 1 / First to Act)

- **Opening the Action:**
  - When holding **KING**, I bet for value: `[act: bet]`.
  - When holding **QUEEN**, I always check: `[act: check]`. Never open-bet with a Queen.
  - When holding **JACK**, I mix between checking `[act: check]` and bluff-betting `[act: bet]` (defaulting primarily to `[act: check]`).

- **Facing a Bet After Checking:**
  - When holding **KING**, I call: `[act: call]`.
  - When holding **JACK**, I fold: `[act: fold]`.
  - When holding **QUEEN**, I fold by default: `[act: fold]`. Avoid calling down with a Queen out of position against standard value-heavy betting ranges.