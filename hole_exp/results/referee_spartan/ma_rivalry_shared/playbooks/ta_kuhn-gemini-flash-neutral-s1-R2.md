---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1165
---
### Kuhn Poker Playbook

- **Showdown Declaration Rule:**
  - Whenever asked to declare my card at showdown, always declare the exact card dealt (`[show: jack]`, `[show: queen]`, or `[show: king]`). Never misdeclare.

- **As Player 1 (Opening Action):**
  - When dealt **JACK**: Always `[act: check]`.
  - When dealt **QUEEN**: Always `[act: check]`.
  - When dealt **KING**: Always `[act: bet]` to guarantee value and deny opponent free showdowns.

- **As Player 1 Facing a Bet (After Checking):**
  - When holding **JACK**: Always `[act: fold]`.
  - When holding **QUEEN**: Always `[act: fold]`.
  - When holding **KING**: Always `[act: call]`.

- **As Player 2 Facing an Open Bet:**
  - When holding **JACK**: Always `[act: fold]`.
  - When holding **QUEEN**: Always `[act: fold]`.
  - When holding **KING**: Always `[act: call]`.

- **As Player 2 Facing a Check:**
  - When holding **JACK**: Always `[act: bet]` as a bluff to fold out checking Queens.
  - When holding **QUEEN**: Always `[act: check]` behind to realize showdown value against Jacks. Never bet.
  - When holding **KING**: Always `[act: bet]` for guaranteed value. Never check behind with a King.