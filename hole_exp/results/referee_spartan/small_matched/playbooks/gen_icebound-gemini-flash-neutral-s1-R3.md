---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1247
---
- In the pledge stage of every round, always submit `[pledge: scout]`. Pledging scout minimizes upfront fuel deduction to only 1 fuel (preserving fuel for the 1:1 post-game bonus points) while keeping full flexibility for the act phase.

- Clockwise targeting reference:
  - If North: clockwise target is East; incoming raider is West.
  - If East: clockwise target is West; incoming raider is North.
  - If West: clockwise target is North; incoming raider is East.

- In the act stage of every round:
  - Check clockwise target's public pledge:
    - If target pledged `scout`: submit `[act: raid]`. Raiding a scouting target captures 3 points at no extra fuel penalty beyond the scout pledge.
    - If target pledged `escort` or `raid`: raiding would lose 1 point.
      - If incoming raider pledged `scout`: submit `[act: scout]` to earn 3 points safely.
      - If incoming raider pledged `raid`: submit `[act: escort]` to protect against theft and earn 2 points.

- Output format: provide at most one short line of reasoning followed immediately by the exact bracketed token (`[pledge: scout]`, `[pledge: escort]`, `[pledge: raid]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`). No extra tokens or markdown wrappers around the brackets.