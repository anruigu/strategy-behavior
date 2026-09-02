---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1635
---
### Kuhn Poker Playbook

#### Showdown Declarations
- When asked to declare my card at showdown, always truthfully output `[show: jack]`, `[show: queen]`, or `[show: king]` matching the card I was dealt. Never misdeclare.

---

#### Playing as Player 1 (Opening Action)
- **With KING:** Output `[act: bet]` to extract value from calls.
- **With QUEEN:** Output `[act: check]`. Never open-bet with a Queen.
- **With JACK:** Output `[act: check]` most of the time to realize free showdowns or control pot size.

---

#### Playing as Player 1 Facing a Bet (After Check-Bet)
- **With KING:** Output `[act: call]`.
- **With QUEEN:** 
  - Output `[act: call]` to catch opponent bluffs when chip EV matters.
  - Only output `[act: fold]` if protecting a narrow match lead on the final hand where a tie guarantees a match win and avoiding risk is paramount.
- **With JACK:** Always output `[act: fold]`. Never call with a Jack under any circumstances; it cannot beat any value bet or bluff.

---

#### Playing as Player 2 Facing an Opponent Check
- **With KING:** Output `[act: bet]` for maximum value.
- **With QUEEN:** Output `[act: check]` behind to take the showdown win against Jacks without losing chips to Kings.
- **With JACK:** Output `[act: check]` or mix in an occasional `[act: bet]` bluff against loose folders, but prefer `[act: check]` if opponent frequently calls.

---

#### Playing as Player 2 Facing an Opponent Open Bet
- **With KING:** Always output `[act: call]`.
- **With QUEEN:** Output `[act: fold]`. Facing an open bet from Player 1, Queen rarely beats their value range.
- **With JACK:** Always output `[act: fold]`.