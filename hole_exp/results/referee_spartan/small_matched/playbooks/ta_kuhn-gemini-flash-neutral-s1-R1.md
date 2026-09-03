---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1692
---
# Kuhn Poker Playbook

### Showdown Declarations
- When asked to declare my card at showdown, I always declare my exact card truthfully: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

### In Position (Player 2 / Second to Act)

- **Facing a Check:**
  - When holding **KING**, I always bet for maximum value: `[act: bet]`. Never check back a King.
  - When holding **JACK**, I always bet as a bluff to force folds from Queens: `[act: bet]`. Never check behind with a Jack because it has zero showdown equity.
  - When holding **QUEEN**, I always check behind to realize showdown value against Jacks without paying off Kings: `[act: check]`.

- **Facing a Bet:**
  - When holding **KING**, I always call: `[act: call]`.
  - When holding **JACK**, I always fold: `[act: fold]`. Calling with a Jack is never profitable.
  - When holding **QUEEN**, I default to folding: `[act: fold]`. Do not repeatedly bluff-catch with a Queen unless the opponent has a proven high bluffing frequency.

---

### Out of Position (Player 1 / First to Act)

- **Opening the Action:**
  - When holding **KING**, I bet for value: `[act: bet]`.
  - When holding **QUEEN**, I check: `[act: check]`. Never open-bet with a Queen.
  - When holding **JACK**, I mix between checking `[act: check]` and bluff-betting `[act: bet]`.

- **Facing a Bet After Checking:**
  - When holding **KING**, I call: `[act: call]`.
  - When holding **JACK**, I fold: `[act: fold]`.
  - When holding **QUEEN**, I fold by default: `[act: fold]`. Calling down every bet with a Queen leads to severe chip bleed against opponents who value-bet Kings and bluff infrequently. Only call if the opponent bluffs Jacks at a very high rate.