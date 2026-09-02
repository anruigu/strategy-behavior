---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1597
---
### Playbook for Kuhn Poker

* **Showdown Declarations:**
  * Always declare my true dealt card immediately with `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to misrepresent the card.

* **Playing as Player 1 (Opening Action):**
  * When opening with a **King**, always play `[act: bet]`.
  * When opening with a **Queen**, always play `[act: check]`.
  * When opening with a **Jack**, mix between `[act: check]` and `[act: bet]` (bluffing roughly one-third of the time to balance value bets).

* **Playing as Player 1 (Facing a Bet after Checking):**
  * When holding a **Jack**, always play `[act: fold]`. Never call with the lowest card.
  * When holding a **Queen**, default to `[act: fold]` unless the opponent over-bluffs; do not call routinely, as calling with a Queen against standard value-heavy betting ranges is unprofitable.
  * When holding a **King** (if checked earlier), always play `[act: call]`.

* **Playing as Player 2 (Facing an Opening Bet):**
  * When holding a **King**, always play `[act: call]`.
  * When holding a **Queen**, default to `[act: fold]`.
  * When holding a **Jack**, always play `[act: fold]`.

* **Playing as Player 2 (Facing an Opening Check):**
  * When holding a **King**, always play `[act: bet]` for value. Never check behind with the nuts.
  * When holding a **Queen**, always play `[act: check]` behind to take the free showdown and beat Jacks. Never bet a Queen.
  * When holding a **Jack**, play `[act: bet]` as a bluff to force Queen folds. Checking behind with a Jack guarantees zero showdown equity against checking ranges.