---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1753
---
# Playbook for Kuhn Poker

### Position 1: Acting First (Opening the Hand)
- **When dealt a King:**
  - Standard action: Choose `[act: bet]` to extract immediate value or win the ante.
  - Mixed strategy / trap: Occasionally choose `[act: check]`. If the opponent bets after my check, always choose `[act: call]`.
- **When dealt a Queen:**
  - Always choose `[act: check]`. Never open with a bet.
  - Facing a bet after my check: Always choose `[act: fold]`. Do not call with a Queen here; calling against an opponent bet after a check loses chips against their King value bets.
- **When dealt a Jack:**
  - Default action: Choose `[act: check]`.
  - Facing a bet after my check: Always choose `[act: fold]`. Never call with a Jack.

---

### Position 2: Acting Second (Facing Opponent's Open)
- **When the opponent opens with a bet:**
  - **With King:** Always choose `[act: call]`.
  - **With Queen:** Always choose `[act: fold]`. Calling is unprofitable because the opponent's opening bet range heavily favors Kings.
  - **With Jack:** Always choose `[act: fold]`.

- **When the opponent opens with a check:**
  - **With King:** Always choose `[act: bet]` to win the pot or get called by weaker holdings.
  - **With Queen:** Always choose `[act: check]`. Never bet; checking guarantees a win against a Jack and prevents losing an extra chip to a trapped King.
  - **With Jack:** Always choose `[act: check]`. Do not bluff-bet with a Jack when checked to; opponents consistently call with Queens and Kings, making bluffing an unforced -2 chip loss.

---

### Showdown
- When asked to declare at showdown, always declare the exact card I was dealt:
  - If dealt Jack: `[show: jack]`
  - If dealt Queen: `[show: queen]`
  - If dealt King: `[show: king]`