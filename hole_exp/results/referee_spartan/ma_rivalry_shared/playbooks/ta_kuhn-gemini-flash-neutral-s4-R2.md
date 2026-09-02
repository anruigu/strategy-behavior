---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1627
---
### Playbook for Kuhn Poker

* **Showdown Declarations:**
  * Always declare my true dealt card immediately with `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to misrepresent the card.

* **Playing as Player 1 (Opening Action):**
  * When opening with a **King**, always play `[act: bet]` for direct value.
  * When opening with a **Queen**, always play `[act: check]`. Never bet an opening Queen.
  * When opening with a **Jack**, mix between `[act: check]` (standard) and `[act: bet]` (bluffing roughly one-third of the time to balance value bets).

* **Playing as Player 1 (Facing a Bet after Checking):**
  * When holding a **Jack**, always play `[act: fold]`. Never call with the lowest card.
  * When holding a **Queen**, play `[act: fold]` against standard opponents. If the opponent bets aggressively after checks, call a fraction of the time, but fold is the baseline.
  * When holding a **King** (if checked earlier), always play `[act: call]`.

* **Playing as Player 2 (Facing an Opening Bet):**
  * When holding a **King**, always play `[act: call]`.
  * When holding a **Queen**, always play `[act: fold]`.
  * When holding a **Jack**, always play `[act: fold]`.

* **Playing as Player 2 (Facing an Opening Check):**
  * When holding a **King**, always play `[act: bet]` for value. Never check behind with the nuts.
  * When holding a **Queen**, always play `[act: check]` behind to realize showdown value against Jacks without risking a bet against a King.
  * When holding a **Jack**, always play `[act: bet]` as a bluff to force folds from checking Queens. Checking behind guarantees a loss.