---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1455
---
# Playbook for Kuhn Poker

### Position 1: Acting First (Opening the Hand)
- **When dealt a King:**
  - Always choose `[act: bet]` to extract immediate value and build the pot.
- **When dealt a Queen:**
  - Always choose `[act: check]`. Never open with a bet.
  - Facing a bet after my check: Always choose `[act: fold]`. Do not call with a Queen here; calling against an opponent bet after a check loses chips against their King value bets.
- **When dealt a Jack:**
  - Always choose `[act: check]`. Never open with a bet.
  - Facing a bet after my check: Always choose `[act: fold]`. Never call with a Jack.

---

### Position 2: Acting Second (Facing Opponent's Open)
- **When the opponent opens with a bet:**
  - **With King:** Always choose `[act: call]`.
  - **With Queen:** Always choose `[act: fold]`.
  - **With Jack:** Always choose `[act: fold]`.

- **When the opponent opens with a check:**
  - **With King:** Always choose `[act: bet]` to extract maximum value.
  - **With Queen:** Always choose `[act: check]`. Never bet; checking guarantees a win against a Jack and avoids risking an extra chip against a trapped King.
  - **With Jack:** Always choose `[act: check]`. Checking realizes free showdown equity without risking an extra chip.

---

### Showdown
- When asked to declare at showdown, always declare the exact card I was dealt:
  - If dealt Jack: `[show: jack]`
  - If dealt Queen: `[show: queen]`
  - If dealt King: `[show: king]`