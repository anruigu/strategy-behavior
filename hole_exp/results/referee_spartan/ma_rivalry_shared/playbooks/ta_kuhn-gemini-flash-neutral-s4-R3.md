---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1640
---
### Playbook for Kuhn Poker

* **Showdown Declarations:**
  * Always declare my true dealt card immediately using `[show: jack]`, `[show: queen]`, or `[show: king]`. Never misrepresent the card.

* **Playing as Player 1 (Opening Action):**
  * When opening with a **King**, play `[act: bet]` for value.
  * When opening with a **Queen**, play `[act: check]`. Never bet an opening Queen.
  * When opening with a **Jack**, mix between `[act: check]` (standard baseline) and `[act: bet]` (bluffing roughly one-third of the time to balance value bets).

* **Playing as Player 1 (Facing a Bet after Checking):**
  * When holding a **Jack**, always play `[act: fold]`. Calling can never win against any valid range.
  * When holding a **Queen**, mix between `[act: fold]` and `[act: call]` (calling roughly one-third of the time). Do not fold 100% of the time, as pure folding allows Player 2 to profitably bluff every Jack.
  * When holding a **King** (if ever checked earlier), always play `[act: call]`.

* **Playing as Player 2 (Facing an Opening Bet):**
  * When holding a **King**, always play `[act: call]`.
  * When holding a **Queen**, always play `[act: fold]`.
  * When holding a **Jack**, always play `[act: fold]`.

* **Playing as Player 2 (Facing an Opening Check):**
  * When holding a **King**, always play `[act: bet]` for value.
  * When holding a **Queen**, always play `[act: check]` behind to realize showdown value against Jacks without risking an extra chip to a King.
  * When holding a **Jack**, mix between `[act: bet]` (bluffing roughly one-third of the time to capitalize on checking Queens) and `[act: check]` behind.