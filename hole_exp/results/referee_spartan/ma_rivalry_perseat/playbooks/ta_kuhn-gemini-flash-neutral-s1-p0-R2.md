---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1423
---
### Showdown Declarations
* When asked to declare my card at showdown, I always truthfully declare the exact card I was dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

### Player 1 Strategy (Opening Seat)

* **Opening with KING:**
  * I always bet: `[act: bet]`. Checking hands surrenders value against passive opponents.

* **Opening with QUEEN:**
  * I always open by checking: `[act: check]`.
  * Facing a bet after my check:
    * Default to folding: `[act: fold]`.
    * Call `[act: call]` only if I have strong evidence the opponent aggressively bluffs Jacks in position.

* **Opening with JACK:**
  * I always check: `[act: check]`.
  * Facing a bet after checking: I always fold: `[act: fold]`. Never call with a Jack facing a bet.

---

### Player 2 Strategy (In Position)

* **Facing an Opening Bet:**
  * If I hold a **KING**, I always call: `[act: call]`.
  * If I hold a **QUEEN**, I always fold: `[act: fold]` unless facing a known chronic bluffer.
  * If I hold a **JACK**, I always fold: `[act: fold]`.

* **Facing an Opening Check:**
  * If I hold a **KING**, I always bet for value: `[act: bet]`.
  * If I hold a **QUEEN**, I always check back for showdown value: `[act: check]`. Never bet the Queen.
  * If I hold a **JACK**, I default to checking back: `[act: check]` to avoid risking chips, only betting `[act: bet]` as a bluff if the opponent has shown a high tendency to fold Queens.