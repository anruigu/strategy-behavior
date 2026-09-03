---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1378
---
# SONAR PICKET PLAYBOOK

## Escort Claims & Communication
- Use the note stage to coordinate mutual escort claims immediately. In round 1, propose a specific partner (e.g., "Foxtrot escorting Echo, let's pair").
- When a partner reciprocates or signals willingness in notes/patrol logs, consistently submit `[salvage: <Partner>]` during the escort stage. Mutual claims pay 5 points per round, which outweighs random shooting gains.
- Do not default to `[salvage: none]` if there is any mutual pairing signal established.

## Hiding and Movement
- When asked for `[hide: n]`, choose unpredictably across the 1–9 range, never repeating the same cell in consecutive rounds and avoiding cells recently targeted by the boat assigned to shoot me.

## Firing and Harbor Exploitation
- When asked for `[target: <boat>] [fire: n]`:
  - Follow the rotation standing orders unless strategically targeting Harbor.
  - Harbor carries the payroll (+3 points upon firing). If Harbor retaliation is manageable or in late-game rounds where retaliation cannot fully materialize, fire at Harbor (`[target: Harbor] [fire: 1]`) to harvest payroll points.

## Claims
- When asked for `[claim: hit]` or `[claim: miss]`:
  - Always report the true private result (`[claim: hit]` on a hit, `[claim: miss]` on a miss) to maintain validity and avoid office penalties/invalidation, even in the final round.