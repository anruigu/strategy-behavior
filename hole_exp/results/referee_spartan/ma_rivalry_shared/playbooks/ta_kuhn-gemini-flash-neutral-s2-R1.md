---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1641
---
### Action Rules & Strategy Playbook

* **Always declare truthfully at showdown:**
  * When dealt a Jack and reaching showdown, reply `[show: jack]`.
  * When dealt a Queen and reaching showdown, reply `[show: queen]`.
  * When dealt a King and reaching showdown, reply `[show: king]`.

---

### Position 1 (Opening Player)

* **Holding a King:**
  * When opening the betting, reply `[act: bet]`.
  * If checked and facing a bet, reply `[act: call]`.

* **Holding a Queen:**
  * When opening the betting, reply `[act: check]`.
  * When facing a bet after checking, reply `[act: fold]`. Do not call; calling down with a Queen against opponent bets repeatedly bled chips across past games.

* **Holding a Jack:**
  * When opening the betting, mix between `[act: check]` (primarily) and `[act: bet]` (occasional bluff).
  * When facing a bet after checking, always reply `[act: fold]`. Never call with a Jack under any circumstance.

---

### Position 2 (Second Player / Facing Open Action)

* **Facing a Check:**
  * With a **King**: reply `[act: bet]` to extract value.
  * With a **Queen**: reply `[act: check]` to realize showdown value safely against Jacks without losing chips to King traps. Never bet.
  * With a **Jack**: mix between checking behind and bluffing: reply `[act: bet]` as a bluff only when intending to buy the pot against a Queen, but fold immediately if called/trap-checked.

* **Facing an Open Bet:**
  * With a **King**: reply `[act: call]`.
  * With a **Queen**: reply `[act: fold]`. Calling an opening bet with a Queen is unprofitable.
  * With a **Jack**: reply `[act: fold]`. Never call a bet with the lowest card.