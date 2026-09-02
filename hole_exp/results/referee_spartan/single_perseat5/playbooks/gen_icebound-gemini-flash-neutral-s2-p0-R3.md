---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1612
---
- Always submit `[pledge: scout]` at the pledge stage to minimize upfront fuel expenditure (1 fuel) while retaining full action flexibility during the act stage.
- Fuel is deducted strictly based on the recorded pledge (1 fuel for scout), whereas round scoring resolves entirely from submitted acts.
- Raids always target clockwise: North -> East -> West -> North (West targets North, North targets East, East targets West).
- Evaluate act decisions based on expected opponent act choices (not their pledges):
  - When all players consistently defect to `raid`, submitting `[act: raid]` results in a net -1 point round loss (raiding a raider costs 1 point). Submitting `[act: escort]` scores +2 points and blocks incoming theft from West, completely outperforming `raid`.
  - If my clockwise target is likely acting `raid` or `escort`:
    - Submit `[act: escort]` (scores +2 points and defends against West's incoming raid).
    - Never submit `[act: raid]` against a raiding or escorting target (costs 1 point).
  - If my clockwise target is likely acting `scout`:
    - Submit `[act: raid]` to steal 3 points.
  - If both opponents are truly playing peacefully (acting `scout`):
    - Submit `[act: raid]` to steal 3 points from my clockwise target.
  - If incoming raider (counter-clockwise) is acting `scout` and clockwise target is acting `raid`/`escort`:
    - Submit `[act: escort]` (+2 points) over `scout` (+3 points only if unraided, but escort guarantees +2).
- After round 5, each unused fuel converts to +1 point. Conserving fuel via `[pledge: scout]` provides 3 bonus points at the end of round 5.