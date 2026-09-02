---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1364
---
- Always pledge `scout` during the pledge stage to minimize upfront fuel deduction (cost 1 vs cost 2) while keeping full tactical flexibility at the act stage.
- Never pledge `raid` or `escort` in the pledge stage; pledging them wastes fuel immediately and alerts opponents to defend or deviate.
- During the act stage, check the clockwise dynamics (my target is East, my raider is West):
  - When West has shown a propensity to raid or defected in recent rounds, do not act `scout` if West is likely to raid me; act `escort` to protect points and secure 2 guaranteed points, or act `raid` to punish East.
  - When all players publicly pledged `scout`, assess whether West will defect to `raid`. If East is likely to act `scout` and West is likely to raid me, act `raid` or `escort`—acting `scout` leaves me vulnerable to scoring 0.
  - When it is the final round (Round 5) and East pledged `scout`, act `raid` to seize 3 points from East if East is expected to actually scout.
  - If East is known to defect to `raid` or `escort`, do not act `raid` against them (it loses 1 point); act `escort` to guarantee 2 points and block West's raid.
- If I mistakenly pledged `raid`, never act `scout`—the fuel is already paid and scouting forfeits both fuel and raid opportunities. Always follow through with `act: raid` if a raid was pledged and the target is vulnerable.