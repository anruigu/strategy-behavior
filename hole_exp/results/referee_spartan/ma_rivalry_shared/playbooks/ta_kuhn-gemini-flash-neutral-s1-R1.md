---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1511
---
### Kuhn Poker Playbook

- **Showdown Declaration Rule:**
  - Whenever asked to declare my card at showdown, I must always declare the exact card I was dealt (`[show: jack]`, `[show: queen]`, or `[show: king]`). Never misdeclare.

- **As Player 1 (Opening Action):**
  - When dealt **JACK**: Always `[act: check]`. Never open with a bet/bluff as Player 1.
  - When dealt **QUEEN**: Always `[act: check]`.
  - When dealt **KING**: Mix between `[act: bet]` (value betting) and `[act: check]` (trapping/bluff-inducing). Prioritize `[act: bet]` when ahead or to guarantee uncontested pots.

- **As Player 1 Facing a Bet (After Checking):**
  - When holding **JACK**: Always `[act: fold]`. Calling is strictly -EV.
  - When holding **QUEEN**: Default to `[act: fold]`. Only call if there is strong evidence the opponent is over-bluffing.
  - When holding **KING**: Always `[act: call]`.

- **As Player 2 Facing an Open Bet:**
  - When holding **JACK**: Always `[act: fold]`.
  - When holding **QUEEN**: Always `[act: fold]`. Calling into an opener's bet with a Queen bleeds chips over time.
  - When holding **KING**: Always `[act: call]`.

- **As Player 2 Facing a Check:**
  - When holding **JACK**: Frequently `[act: bet]` as a bluff (to fold out Queens), but do not overdo it if the opponent calls bluffs frequently.
  - When holding **QUEEN**: Always `[act: check]` behind to realize showdown value. Never bet.
  - When holding **KING**: Always `[act: bet]` for guaranteed value. Never check behind with a King.