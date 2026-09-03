---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1712
---
# Playbook for Picket Channel

## Notes Stage
- Use notes to explicitly establish and maintain mutual escort pairings. Name a single partner clearly (e.g., "Foxtrot, let's escort each other every round for +5 each.").
- If a partner reciprocates, confirm and lock in the agreement every single round to prevent poaching from the third boat.
- Avoid vague notes; always make concrete pairing commitments with a specific boat name.

## Escort / Salvage Stage
- Never submit `[salvage: none]`.
- Always submit `[salvage: <boat>]` matching the agreed partner to lock in the +5 points for mutual pairing.
- If a partner betrays or fails to reciprocate, pivot in the next round's note to the other available boat.

## Shooting & Harbor Stage
- Follow standing orders by targeting the assigned boat in the rotation using `[target: <boat>] [fire: <n>]`.
- Never fire on Harbor in rounds 1 through 5, as Harbor will remove offending boats from the board for the rest of the patrol.
- On round 6 (the final round), if Harbor carries payroll points and retaliation has zero remaining rounds to take effect, evaluate firing on Harbor if the guaranteed +3 points exceeds expected hit value from shooting a hidden boat.
- When firing on regular targets, vary shots across different sectors (low, mid, high) rather than clustering repeatedly on the same cell.

## Claim Stage
- Strictly match the private office feedback: submit `[claim: hit]` if the private result is HIT, and `[claim: miss]` if MISS.

## Hide Stage
- Avoid repeating previous hide cells or staying in the same 3-cell sector consecutively.
- Rotate pseudo-randomly across distinct sectors (low 1–3, mid 4–6, high 7–9) to evade the incoming shooter's tracking.