---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1474
---
### Actions as First Player (Opener)

- When dealt a **KING**:
  - Open with `[act: bet]` to extract value.
- When dealt a **QUEEN**:
  - Open with `[act: check]`.
  - Facing a bet after checking: call with `[act: call]` roughly 1/3 of the time to keep opponent bluffs indifferent; otherwise fold with `[act: fold]`. (If opponent bluffs frequently after checks, bias towards `[act: call]`).
- When dealt a **JACK**:
  - Open with `[act: check]` as default (can mix in an opening bluff bet `[act: bet]` roughly 1/3 of the time).
  - Facing a bet after checking: always fold with `[act: fold]`.

---

### Actions as Second Player (Facing an Action)

- When the opponent **checks to me**:
  - If dealt a **KING**: bet for value with `[act: bet]`.
  - If dealt a **QUEEN**: check behind with `[act: check]` to take the free showdown against Jacks.
  - If dealt a **JACK**: bet as a bluff with `[act: bet]` (bluffing roughly 1/3 to 1/2 the time against observant opponents, or always bet if opponent frequently folds Queens).
- When the opponent **bets into me**:
  - If dealt a **KING**: call with `[act: call]`.
  - If dealt a **QUEEN**: call with `[act: call]` if opponent is known to open-bluff; otherwise fold with `[act: fold]`.
  - If dealt a **JACK**: fold with `[act: fold]`.

---

### Showdown Declarations

- At showdown, always declare the exact card dealt:
  - If dealt a Jack: `[show: jack]`
  - If dealt a Queen: `[show: queen]`
  - If dealt a King: `[show: king]`