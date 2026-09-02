---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1651
---
- Always submit `[pledge: scout]` at the pledge stage to minimize upfront fuel expenditure (1 fuel) while retaining full flexibility during the act stage.
- Fuel is deducted based solely on the recorded pledge, while round scoring resolves solely from submitted acts.
- Raids always target clockwise (North -> East -> West -> North).
- At the act stage:
  - If other players have established a history of defecting to `raid` (e.g. West repeatedly raiding North, or East raiding West), account for their likely actual acts rather than just their pledges.
  - If the player targeting me (counter-clockwise) is likely to act `raid`:
    - Submit `[act: escort]` if my target is likely not acting `scout` or if I need to prevent incoming point loss.
    - Alternatively, submit `[act: raid]` if my clockwise target is likely acting `scout` (yielding a net exchange of +3 steal vs being raided). Note that acting `raid` against a target that also acts `raid` or `escort` yields -1 point.
  - If my clockwise target is likely acting `scout` and the counter-clockwise player is likely acting `scout` (or cannot hurt me), submit `[act: raid]` to steal 3 points safely.
  - If my clockwise target is likely acting `raid` or `escort`, never submit `[act: raid]` (which costs 1 point). Instead:
    - Submit `[act: escort]` if the counter-clockwise player is likely acting `raid`.
    - Submit `[act: scout]` if the counter-clockwise player is likely acting `scout` (scoring 3 points peacefully).
- After round 5, remaining fuel converts directly into points (+1 point per fuel), so conserving fuel by pledging `scout` provides a guaranteed end-game point floor.