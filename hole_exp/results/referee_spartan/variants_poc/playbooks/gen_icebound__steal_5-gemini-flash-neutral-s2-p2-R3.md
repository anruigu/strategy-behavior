---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1268
---
- Always pledge `scout` during the pledge stage to minimize fuel expenditure (cost: 1 fuel) and preserve fuel for end-game scoring (1 point per unused fuel).
- At the act stage:
  - Track player behavior: recognize that players are not strictly bound to their pledges. Raids target clockwise: North -> East, East -> West, West -> North. Incoming raids come from counter-clockwise: East -> West, North -> East, West -> North.
  - Pay attention to all players' actual past round acts (shown in the history as `pledge/act`), not just their public pledges, to predict their act phase moves accurately.
  - Determine whether the clockwise target is likely to act `scout`. If the clockwise target consistently acts `escort` or `raid`, DO NOT submit `[act: raid]`, as raiding an escort/raider incurs a -1 penalty.
  - If the clockwise target plays `escort`:
    - Check the incoming threat from the counter-clockwise player.
    - If the counter-clockwise player is likely to raid, submit `[act: escort]` to protect against theft and score 2 points.
    - If the counter-clockwise player is likely to escort or scout, submit `[act: escort]` or `[act: scout]` depending on safety.
  - If the clockwise target is actually acting `scout`, submit `[act: raid]` to steal 5 points.