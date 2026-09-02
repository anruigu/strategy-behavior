---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1592
---
### Showdown Declarations
* When asked to declare my card at showdown, I always truthfully declare the exact card I was dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

### Player 1 Strategy (Opening Seat)

* **Opening with KING:**
  * I always bet: `[act: bet]`. Checking surrenders value against passive opponents.

* **Opening with QUEEN:**
  * I always open by checking: `[act: check]`.
  * Facing a bet after my check:
    * Default to folding: `[act: fold]`.
    * Call `[act: call]` if the opponent is aggressively betting every time I check.

* **Opening with JACK:**
  * Mix between checking `[act: check]` (standard) and bluff betting `[act: bet]` (roughly 1/3 of the time) to balance the range and prevent opponents from betting uncontested.
  * Facing a bet after checking: I always fold: `[act: fold]`. Never call with a Jack facing a bet.

---

### Player 2 Strategy (In Position)

* **Facing an Opening Bet:**
  * If I hold a **KING**, I always call: `[act: call]`.
  * If I hold a **QUEEN**, I mix: fold `[act: fold]` against balanced players, but call `[act: call]` (approx. 1/3 of the time) if the opponent bluffs opening Jacks.
  * If I hold a **JACK**, I always fold: `[act: fold]`.

* **Facing an Opening Check:**
  * If I hold a **KING**, I always bet for value: `[act: bet]`.
  * If I hold a **QUEEN**, I always check back for showdown value: `[act: check]`. Never bet the Queen.
  * If I hold a **JACK**, I mix: bet `[act: bet]` as a bluff (roughly 1/3 of the time) to take down pots when the opponent folds Queens, otherwise check back `[act: check]`.