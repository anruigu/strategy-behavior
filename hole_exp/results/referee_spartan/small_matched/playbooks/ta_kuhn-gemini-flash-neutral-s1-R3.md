---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1906
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
  - When holding **QUEEN**, I call at roughly 1/3 frequency to prevent opponent bluffing exploits, but fold by default (`[act: fold]`) against neutral or passive opponents. If opponent opens frequently, call: `[act: call]`.

---

### Out of Position (Player 1 / First to Act)

- **Opening the Action:**
  - When holding **KING**, I mix between betting `[act: bet]` (roughly 2/3 frequency) and checking to trap `[act: check]` (roughly 1/3 frequency). Default to `[act: bet]`.
  - When holding **QUEEN**, I always check: `[act: check]`. Never open-bet with a Queen.
  - When holding **JACK**, I primarily check `[act: check]` (about 2/3 to 3/4 frequency) but occasionally bluff-bet `[act: bet]`. Default to `[act: check]`.

- **Facing a Bet After Checking:**
  - When holding **KING**, I always call: `[act: call]`.
  - When holding **JACK**, I always fold: `[act: fold]`.
  - When holding **QUEEN**, I mix between folding (`[act: fold]`) and calling (`[act: call]`). Default to `[act: fold]`, but switch to calling if the opponent regularly bets when checked to.