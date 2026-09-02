---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1345
---
### Actions as First Player (Opener)

- When dealt a **KING**:
  - Open with `[act: bet]` to extract value.
- When dealt a **QUEEN**:
  - Open with `[act: check]`.
  - Facing a bet after checking: fold with `[act: fold]`.
- When dealt a **JACK**:
  - Open with `[act: check]`. (Optionally mix in an open bluff `[act: bet]` if game theory balance is needed, but default to checking).
  - Facing a bet after checking: always fold with `[act: fold]`.

---

### Actions as Second Player (Facing an Action)

- When the opponent **checks to me**:
  - If dealt a **KING**: bet for value with `[act: bet]`.
  - If dealt a **QUEEN**: check behind with `[act: check]` to realize showdown value against Jacks without risking an extra chip to Kings.
  - If dealt a **JACK**: bet as a bluff with `[act: bet]`, as checking behind guarantees losing the pot at showdown. If the opponent consistently slowplays or calls bluffs, check behind with `[act: check]` to minimize loss.
- When the opponent **bets into me**:
  - If dealt a **KING**: call with `[act: call]`.
  - If dealt a **QUEEN**: fold with `[act: fold]`.
  - If dealt a **JACK**: fold with `[act: fold]`.

---

### Showdown Declarations

- At showdown, always declare the exact card dealt:
  - If dealt a Jack: `[show: jack]`
  - If dealt a Queen: `[show: queen]`
  - If dealt a King: `[show: king]`