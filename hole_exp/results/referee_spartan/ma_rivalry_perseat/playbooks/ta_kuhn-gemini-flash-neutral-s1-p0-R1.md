---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1629
---
### Showdown Declarations
* When asked to declare my card at showdown, I always declare the exact card I was dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

### Player 1 Strategy (Opening Seat)

* **Opening with KING:**
  * I always bet: `[act: bet]`.
  * *What did not work:* Checking the King to induce bluffs often resulted in the opponent checking behind, surrendering value.

* **Opening with QUEEN:**
  * I always check: `[act: check]`.
  * When the opponent bets after my check, I evaluate the opponent:
    * Against opponents who bluff Jack frequently, I call: `[act: call]`.
    * If the opponent only bets Kings for value or rarely bluffs, I fold: `[act: fold]`.

* **Opening with JACK:**
  * I default to checking: `[act: check]`.
  * When facing a bet after checking a Jack, I always fold: `[act: fold]`. Never call with a Jack facing a bet.

---

### Player 2 Strategy (In Position)

* **Facing an Opening Bet:**
  * If I hold a **KING**, I always call: `[act: call]`.
  * If I hold a **QUEEN**, I usually fold: `[act: fold]`, calling only if the opponent bluffs frequently.
  * If I hold a **JACK**, I always fold: `[act: fold]`.

* **Facing an Opening Check:**
  * If I hold a **KING**, I always bet: `[act: bet]`.
  * If I hold a **QUEEN**, I always check back: `[act: check]`. Never turn the Queen into a bluff or value bet here.
  * If I hold a **JACK**, I mix checking and bluffing:
    * Check back `[act: check]` if the opponent is prone to calling with Queens.
    * Bet `[act: bet]` only if the opponent folds Queens reliably to bets. Avoid over-bluffing when opponents call down lightly.