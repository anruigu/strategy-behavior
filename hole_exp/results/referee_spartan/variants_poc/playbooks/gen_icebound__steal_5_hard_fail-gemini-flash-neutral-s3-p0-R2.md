---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1656
---
- In every round's **act stage**, always repeat my own pledge exactly (`[act: X]` matching `[pledge: X]`). Fuel is already deducted at the pledge stage, so remaining fuel displayed during the act stage reflects fuel *after* the pledge; never change an act to `scout` just because remaining fuel is low.
- When an opponent defects at the act stage (e.g., pledging `scout` then acting `raid`):
  - In the pledge stage, assume opponents may fake pledges.
  - If the player behind me (counter-clockwise: West for North) has shown a willingness to raid (even by defecting from scout to raid), shift my pledge to `escort`. Continuing to `scout` against an active raider yields 0 points and loses 5 points to theft.
- When choosing to `raid`:
  - Only pledge `raid` if my clockwise target (North->East, East->West, West->North) is reliably acting `scout` and not defending or raiding.
  - If my clockwise target is likely to act `escort` or `raid`, do not raid them, as colliding with an escort or raider inflicts a -6 point penalty.
- When the environment turns aggressive or unpredictable:
  - Default to `[pledge: escort]` if I suspect the player behind me will raid. Escort reliably secures +2 points, prevents theft, and inflicts -6 on an incoming raider.
  - If opponents are defecting to raid, `escort` is strictly safer than `scout`.
- In the final rounds, calculate the fuel payoff (+1 point per leftover fuel unit):
  - Do not burn fuel on risky missions if the net payoff is worse than conserving fuel.
  - Choose `scout` (costs 1 fuel, yields +3 points if safe) or `escort` (costs 2 fuel, yields +2 points and defense) based on incoming threat levels.