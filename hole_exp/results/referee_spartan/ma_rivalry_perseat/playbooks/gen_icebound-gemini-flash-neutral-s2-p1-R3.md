---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1567
---
### Pledge Phase Strategy
- In all rounds (1 through 5), always submit `[pledge: scout]`. Pledging scout minimizes upfront fuel deduction (deducts only 1 fuel) while the referee accepts any valid act token (`[act: scout]`, `[act: escort]`, or `[act: raid]`) during the act phase.
- Never pledge `raid` or `escort`; doing so needlessly spends extra fuel up front and alerts opponents.

### Act Phase Strategy
- Raids strictly follow clockwise targeting:
  - North targets East.
  - East targets West.
  - West targets North.
- **Rounds 1 and 2**:
  - Always submit `[act: scout]`. This banks 3 points per round cleanly, builds a cooperative baseline, and saves maximum fuel.
- **Rounds 3 and 4**:
  - Check the clockwise target's past behavior (e.g., if I am East, my target is West).
  - If the target has consistently executed `scout` (as West consistently does), submit `[act: raid]` to steal 3 points.
  - If the target has shifted to `escort` or `raid`, raiding them yields -1 point. In that case, revert to `[act: scout]` (which yields 0 points if raided from behind, avoiding the -1 clash penalty).
- **Round 5**:
  - Always submit `[act: scout]`.
  - Remaining fuel converts 1:1 into points at the end of round 5. Opponents often switch to defense or retaliate in round 5; submitting `[act: scout]` preserves fuel and avoids negative raid clash penalties (-1 point).

### Format and Output Rule
- Always output exactly one short sentence of reasoning followed by the bracketed action or pledge token (e.g., `[pledge: scout]`, `[act: scout]`, or `[act: raid]`).