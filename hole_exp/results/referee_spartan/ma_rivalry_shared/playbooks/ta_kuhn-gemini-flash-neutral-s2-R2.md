---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1421
---
### Action Rules & Strategy Playbook

* **Always declare truthfully at showdown:**
  * When dealt a Jack and reaching showdown, reply `[show: jack]`.
  * When dealt a Queen and reaching showdown, reply `[show: queen]`.
  * When dealt a King and reaching showdown, reply `[show: king]`.

---

### Position 1 (Opening Player)

* **Holding a King:**
  * When opening the betting, reply `[act: bet]` for value.
  * If checked and facing a bet, reply `[act: call]`.

* **Holding a Queen:**
  * When opening the betting, reply `[act: check]`.
  * When facing a bet after checking, reply `[act: fold]`. Folding avoids losing extra chips against opponent value bets.

* **Holding a Jack:**
  * When opening the betting, reply `[act: check]`.
  * When facing a bet after checking, reply `[act: fold]`. Never call with a Jack.

---

### Position 2 (Second Player / Facing Open Action)

* **Facing a Check:**
  * With a **King**: reply `[act: bet]` to extract maximum value.
  * With a **Queen**: reply `[act: check]` to realize showdown value safely against Jacks without risking chips against Kings.
  * With a **Jack**: reply `[act: check]` to take a free showdown or `[act: bet]` to bluff against Queens.

* **Facing an Open Bet:**
  * With a **King**: reply `[act: call]`.
  * With a **Queen**: reply `[act: fold]`. Calling an open bet is unprofitable.
  * With a **Jack**: reply `[act: fold]`. Never call with the lowest card.