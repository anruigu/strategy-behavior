---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1611
---
### Actions as First Player (Opener)

- When dealt a **KING**, I open with `[act: bet]`.
- When dealt a **QUEEN**, I open with `[act: check]`.
- When dealt a **JACK**, I open with `[act: check]`.
- When I checked with a **QUEEN** and the opponent bets, I fold with `[act: fold]` unless I have a strong read that the opponent bluffs frequently. (Calling with a Queen against a standard range bleeds chips to Kings; folding has proven consistently more profitable).
- When I checked with a **JACK** and the opponent bets, I always fold with `[act: fold]`. Calling with a Jack never works because it beats nothing.

---

### Actions as Second Player (Facing an Action)

- When the opponent **checks to me**:
  - If dealt a **KING**, I bet for value with `[act: bet]`.
  - If dealt a **QUEEN**, I check behind with `[act: check]` to realize showdown value against Jacks without risking an extra chip to Kings.
  - If dealt a **JACK**, I bet as a bluff with `[act: bet]`. (Checking behind guarantees losing at showdown; bluffing gives the only chance to take the pot when the opponent checked a Queen).
- When the opponent **bets into me**:
  - If dealt a **KING**, I call with `[act: call]`.
  - If dealt a **QUEEN**, I fold with `[act: fold]`. Calling is -EV against standard open-betting ranges.
  - If dealt a **JACK**, I fold with `[act: fold]`. Never call with a Jack under any circumstances.

---

### Showdown Declarations

- At showdown, I always honestly declare the exact card I was dealt:
  - If holding a Jack: `[show: jack]`
  - If holding a Queen: `[show: queen]`
  - If holding a King: `[show: king]`