---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1762
---
### Kuhn Poker Playbook

#### Showdown Declarations
- When asked to declare my card at showdown, always truthfully output `[show: jack]`, `[show: queen]`, or `[show: king]` matching the card I was dealt. Never misdeclare.

---

#### Playing as Player 1 (Opening Action)
- **With KING:** Output `[act: bet]` for pure value.
- **With QUEEN:** Output `[act: check]`. Never open-bet with a Queen.
- **With JACK:** Output `[act: check]` as standard, or mix in an occasional `[act: bet]` as a pure bluff to balance open-bet ranges.

---

#### Playing as Player 1 Facing a Bet (After Check-Bet)
- **With KING:** Always output `[act: call]` (slowplay trap/value).
- **With QUEEN:** Output `[act: fold]` as the default against opponents who do not over-bluff, but mix in `[act: call]` when pot odds or aggressive opponent bluff frequencies warrant catching bluffs.
- **With JACK:** Always output `[act: fold]`. Never call with a Jack under any circumstances; it has zero showdown value against any bet.

---

#### Playing as Player 2 Facing an Opponent Check
- **With KING:** Output `[act: bet]` to extract value from Queen calls or bluffs.
- **With QUEEN:** Always output `[act: check]` behind to safely realize showdown value against Jacks without risking an extra chip against slowplayed Kings.
- **With JACK:** Output `[act: bet]` as a bluff to fold out Queens if opponent checks weak ranges, or `[act: check]` if opponent frequently check-calls.

---

#### Playing as Player 2 Facing an Opponent Open Bet
- **With KING:** Always output `[act: call]`.
- **With QUEEN:** Output `[act: fold]`. Facing an open bet from Player 1, Queen rarely beats their value range unless opponent is known to open-bluff Jacks aggressively.
- **With JACK:** Always output `[act: fold]`.