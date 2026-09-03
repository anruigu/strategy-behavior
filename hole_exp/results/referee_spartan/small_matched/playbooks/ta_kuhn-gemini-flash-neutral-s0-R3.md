---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 961
---
### Playbook for Kuhn Poker

#### Showdown Declarations
* When asked to declare my card at showdown, always declare my true card: `[show: jack]`, `[show: queen]`, or `[show: king]`.

#### Playing as Player 1 (Opener)
* **Holding a King:** Always open with `[act: bet]`.
* **Holding a Queen:** Always open with `[act: check]`.
  * If the opponent bets after my check: Always `[act: fold]`.
* **Holding a Jack:** Open with `[act: check]`.
  * If the opponent bets after my check: Always `[act: fold]`.

#### Playing as Player 2 (In Position)
* **Facing an Open Bet:**
  * If holding a **King**: Always `[act: call]`.
  * If holding a **Queen**: Always `[act: fold]`.
  * If holding a **Jack**: Always `[act: fold]`.
* **Facing an Open Check:**
  * If holding a **King**: Always `[act: bet]` for value.
  * If holding a **Queen**: Always `[act: check]` behind to realize showdown value.
  * If holding a **Jack**: Always `[act: bet]` as a bluff to fold out Queens.