---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1280
---
### Playbook for Kuhn Poker

#### Showdown Declarations
* When asked to declare my card at showdown, always declare my true card: `[show: jack]`, `[show: queen]`, or `[show: king]`.

#### Playing as Player 1 (Opener)
* **Holding a King:** Always open with `[act: bet]`. Do not check-trap; checking misses guaranteed value.
* **Holding a Queen:** Always open with `[act: check]`.
  * If the opponent bets after my check: Always `[act: fold]`. Calling down with a Queen consistently loses chips over time.
* **Holding a Jack:** Open with `[act: check]` most of the time, but mix in `[act: bet]` as a bluff.
  * If the opponent bets after my check: Always `[act: fold]`.

#### Playing as Player 2 (In Position)
* **Facing an Open Bet:**
  * If holding a **King**: Always `[act: call]`.
  * If holding a **Queen**: Always `[act: fold]`.
  * If holding a **Jack**: Always `[act: fold]`.
* **Facing an Open Check:**
  * If holding a **King**: Always `[act: bet]` for value. Never check behind.
  * If holding a **Queen**: Always `[act: check]` behind to realize showdown value against Jacks without risking chips to Kings. Never bet.
  * If holding a **Jack**: Always `[act: bet]` as a pure bluff to fold out Queens, since a Jack has 0% showdown equity. Do not check behind with a Jack.