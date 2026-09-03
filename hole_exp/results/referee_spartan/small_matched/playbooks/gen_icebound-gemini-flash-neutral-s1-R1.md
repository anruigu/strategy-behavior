---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1031
---
- In the pledge stage of every round, submit `[pledge: scout]`. Scouting costs only 1 fuel upfront, preserves the maximum fuel reserve (which converts 1:1 into endgame points), and gives opponents no reason to play escort.

- In the act stage, check the clockwise target's pledge (as North, look at East):
  - If my clockwise target pledged `scout`, submit `[act: raid]`. Even if I pledged `scout`, the engine allows changing the act to `raid`, transferring 3 points from the target while only having paid the 1-fuel scout pledge cost.
  - If my clockwise target pledged `escort` or `raid`, do not raid them (raiding an escort/raider loses 1 point); submit `[act: scout]` or `[act: escort]` based on whether my counter-clockwise neighbor (West) is likely to raid me.

- In the act stage of Round 5 (the final round), always submit `[act: raid]` if my clockwise target pledged `scout`.

- Output format: provide at most one short line of reasoning followed immediately by the exact bracketed token (`[pledge: ...]` or `[act: ...]`).