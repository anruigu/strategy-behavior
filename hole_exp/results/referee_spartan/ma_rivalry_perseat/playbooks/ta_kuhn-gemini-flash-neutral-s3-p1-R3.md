---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1698
---
### Kuhn Poker Playbook

#### Fundamental Truths
* The deck contains only Jack, Queen, and King. King is the absolute nuts; Jack is the worst hand.
* At showdown, always truthfully declare the exact card dealt: `[show: jack]`, `[show: queen]`, or `[show: king]`.

---

#### Position 1: Acting First (Opener)

* **When dealt a KING:**
  * Always open with `[act: bet]`.
  * If facing a bet/call situation, never fold.

* **When dealt a QUEEN:**
  * Always open with `[act: check]`.
  * Facing a bet after checking:
    * Standard response is `[act: fold]`.
    * Call with `[act: call]` sparingly (only when heavily trailing late and desperate for bluff-catches, or mixed at low frequency; otherwise default to fold to prevent bleeding chips against value Kings).

* **When dealt a JACK:**
  * Always open with `[act: check]`.
  * Facing a bet after checking: always reply with `[act: fold]`. Never call with a Jack.

---

#### Position 2: Acting Second (In Position)

* **Facing a Check:**
  * **When holding a KING:** Always reply with `[act: bet]` to extract maximum value.
  * **When holding a QUEEN:** Always reply with `[act: check]` behind to take the free showdown. Never bet a Queen after a check.
  * **When holding a JACK:**
    * Bluff with `[act: bet]` to fold out Queens (standard aggressive line).
    * Check behind with `[act: check]` only to minimize variance when protecting a lead.

* **Facing an Open Bet:**
  * **When holding a KING:** Always reply with `[act: call]`.
  * **When holding a QUEEN:** Always reply with `[act: fold]`. Opening bets are heavily weighted toward Kings.
  * **When holding a JACK:** Always reply with `[act: fold]`. A Jack cannot beat any called hand.