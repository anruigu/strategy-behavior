---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1876
---
### Pledge Phase Strategy
- In all rounds (1 through 5), always submit `[pledge: scout]`. Pledging scout minimizes upfront fuel deduction (costs only 1 fuel) while retaining the legal right to submit any valid action token (`[act: scout]`, `[act: escort]`, or `[act: raid]`) during the act phase.
- Never pledge `raid` or `escort`; doing so pre-commits extra fuel unnecessarily and signals intent to opponents.

### Act Phase Strategy
- Raids strictly follow clockwise targeting:
  - North targets East.
  - East targets West.
  - West targets North.
- **Rounds 1 and 2**:
  - Always submit `[act: scout]`. This banks 3 points per round cleanly, establishes a cooperative baseline, and saves maximum fuel.
- **Rounds 3 and 4**:
  - Evaluate the clockwise target (the player I attack: West if I am East, North if I am West, East if I am North).
  - If the target is likely to act `scout` (which opponents consistently do after pledging scout in Round 3), submit `[act: raid]` to steal 3 points.
  - If the target has started acting `raid` or `escort`, recognize that raiding into a raider/escort incurs a -1 penalty. If all opponents defect into mutual raiding, raiding an active raider is -1 point while scouting into an incoming raid is 0 points; stick to `[act: scout]` unless reasonably confident the target will act `scout`.
- **Round 5**:
  - Always submit `[act: scout]`.
  - In the final round, remaining fuel converts 1:1 into points. When opponents are prone to late-game defection or retaliatory raiding, `[act: raid]` carries severe downside (-1 on clash plus high risk), while `[act: scout]` guarantees saving fuel points without incurring negative raid clash penalties.

### Format and Output Rule
- Always output exactly one short sentence of reasoning followed by the bracketed action or pledge token (e.g., `[pledge: scout]`, `[act: scout]`, or `[act: raid]`).