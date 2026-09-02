---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1314
---
### Showdown Declarations
- Always declare truthfully:
  - If dealt a Jack, reply `[show: jack]`.
  - If dealt a Queen, reply `[show: queen]`.
  - If dealt a King, reply `[show: king]`.

---

### Opening as Player 1 (First to Act)
- When dealt a **King**, reply `[act: bet]`.
- When dealt a **Queen**, reply `[act: check]`. Never bet opening with a Queen.
- When dealt a **Jack**, reply `[act: check]` most of the time; mix in an occasional `[act: bet]` bluff.

---

### Player 1 Facing a Bet After Checking
- When holding a **Jack**, always reply `[act: fold]`.
- When holding a **Queen**, reply `[act: fold]` by default. Call occasionally only if the opponent frequently bluffs after a check.
- When holding a **King** (if checked initially), reply `[act: call]`.

---

### Player 2 Acting After Opponent Checks
- When dealt a **King**, always reply `[act: bet]`.
- When dealt a **Queen**, always reply `[act: check]`. Never bet a Queen here.
- When dealt a **Jack**, always reply `[act: bet]` as a bluff to fold out Queen checks.

---

### Player 2 Facing an Opening Bet
- When dealt a **King**, always reply `[act: call]`.
- When dealt a **Queen**, reply `[act: fold]` by default. Never call unless exploiting an opponent who over-bluffs opening with Jacks.
- When dealt a **Jack**, always reply `[act: fold]`.