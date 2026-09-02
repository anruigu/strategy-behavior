---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1485
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
- When dealt a **Jack**, mix checking and bluffing: reply `[act: check]` most of the time, occasionally `[act: bet]` to balance.

---

### Player 1 Facing a Bet After Checking
- When holding a **Jack**, always reply `[act: fold]`.
- When holding a **Queen**, lean toward `[act: fold]` if the opponent value-bets heavily, calling at most 1/3 of the time. Calling repeatedly against a strong betting range loses chips fast.
- When holding a **King** (if checked initially), reply `[act: call]`.

---

### Player 2 Acting After Opponent Checks
- When dealt a **King**, always reply `[act: bet]`.
- When dealt a **Queen**, always reply `[act: check]`. Betting only gets called by Kings and folds out Jacks.
- When dealt a **Jack**, bluff by replying `[act: bet]` to push the opponent off Queen checks; do not passively check behind.

---

### Player 2 Facing an Opening Bet
- When dealt a **King**, always reply `[act: call]`.
- When dealt a **Jack**, always reply `[act: fold]`. Never call with a Jack under any circumstance.
- When dealt a **Queen**, reply `[act: fold]` unless specifically exploiting a frequent bluffing opponent.