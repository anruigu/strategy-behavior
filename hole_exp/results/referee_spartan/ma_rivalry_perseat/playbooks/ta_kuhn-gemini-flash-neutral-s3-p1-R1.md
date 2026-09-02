---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1811
---
### Kuhn Poker Playbook

#### Fundamental Truths
* The deck contains only Jack, Queen, and King. There are no Aces. King is always the absolute nuts; Jack is always the absolute worst.
* At showdown, always declare the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

#### Position 1: Acting First (Opener)

* **When dealt a KING:**
  * Always open with `[act: bet]`. Never check as opener with a King, and never fold if facing a bet.

* **When dealt a QUEEN:**
  * Open with `[act: check]`.
  * If the opponent bets after my check:
    * Call with `[act: call]` roughly 1/3 of the time to catch Jack bluffs, but fold with `[act: fold]` against passive opponents who only bet Kings. Never call blindly every time.

* **When dealt a JACK:**
  * Usually open with `[act: check]` (mix in an occasional `[act: bet]` as a bluff only when needed).
  * If the opponent bets after my check: always reply with `[act: fold]`. Never call with a Jack.

---

#### Position 2: Acting Second (In Position)

* **Facing a Check:**
  * **When holding a KING:** Always reply with `[act: bet]` for pure value.
  * **When holding a QUEEN:** Always reply with `[act: check]` behind to realize showdown value. Never bet a Queen after a check.
  * **When holding a JACK:** 
    * Mix between `[act: bet]` (bluffing to make a Queen fold) and `[act: check]` behind. 
    * If ahead in chips near the end, prefer `[act: check]` to minimize variance.

* **Facing an Initial Bet:**
  * **When holding a KING:** Always reply with `[act: call]`.
  * **When holding a QUEEN:** Fold with `[act: fold]` unless exploiting an opponent who frequently opens with a Jack bluff. Do not routinely call lead bets with a Queen.
  * **When holding a JACK:** Always reply with `[act: fold]`. Never call a bet with the worst card.