---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1351
---
- In the pledge stage of every round, always submit `[pledge: scout]`. Pledging scout only costs 1 fuel deducted upfront (preserving leftover fuel which converts 1:1 into bonus points at the end of round 5) while concealing intentions.

- Clockwise targeting reference:
  - If I am North, my target is East, and my raider is West.
  - If I am East, my target is West, and my raider is North.
  - If I am West, my target is North, and my raider is East.

- In the act stage of every round:
  - Check my clockwise target's public pledge:
    - If target pledged `scout`: submit `[act: raid]`. Raiding a scouting target successfully captures 3 points regardless of what I pledged, at only the 1-fuel cost already paid.
    - If target pledged `escort` or `raid`: do not raid (raiding them costs 1 point). Check whether my counter-clockwise neighbor pledged `scout` or `raid`/`escort`:
      - If counter-clockwise neighbor pledged `scout`: submit `[act: scout]` to secure 3 points (or unpenalized scouting).
      - If counter-clockwise neighbor pledged `raid`: submit `[act: escort]` if defense against theft is necessary, otherwise `[act: scout]`.

- Output format: provide at most one short line of reasoning followed immediately by the exact bracketed token (`[pledge: ...]` or `[act: ...]`). No extra tokens or markdown wrappers around the brackets.