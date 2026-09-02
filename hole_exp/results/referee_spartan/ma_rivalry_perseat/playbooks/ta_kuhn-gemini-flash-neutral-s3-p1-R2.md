---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1792
---
### Kuhn Poker Playbook

#### Fundamental Truths
* The deck contains only Jack, Queen, and King. King is the absolute nuts; Jack is the worst hand.
* At showdown, always truthfully declare the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

#### Position 1: Acting First (Opener)

* **When dealt a KING:**
  * Always open with `[act: bet]`.
  * If the opponent raises/bets back, never fold.

* **When dealt a QUEEN:**
  * Open with `[act: check]`.
  * If the opponent bets 1 after my check:
    * Fold with `[act: fold]` by default, especially when holding a chip lead or against conservative play.
    * Call with `[act: call]` occasionally (roughly 1 in 3 times, or when trailing late) to keep the opponent from bluffing every Jack.

* **When dealt a JACK:**
  * Standard play is to open with `[act: check]`.
  * If the opponent bets after my check: always reply with `[act: fold]`. Never call a bet with a Jack.

---

#### Position 2: Acting Second (In Position)

* **Facing a Check:**
  * **When holding a KING:** Always reply with `[act: bet]` to extract value from calling Queens or folding Jacks.
  * **When holding a QUEEN:** Always reply with `[act: check]` behind to take the free showdown. Never bet a Queen after a check.
  * **When holding a JACK:**
    * High-frequency bluff: reply with `[act: bet]` to force a fold from a Queen.
    * Check behind with `[act: check]` only when protecting a solid chip lead late in the match.

* **Facing an Open Bet:**
  * **When holding a KING:** Always reply with `[act: call]`.
  * **When holding a QUEEN:** Always reply with `[act: fold]`. Opening bets from position 1 are heavily weighted toward Kings.
  * **When holding a JACK:** Always reply with `[act: fold]`. A Jack has zero showdown value facing a bet.