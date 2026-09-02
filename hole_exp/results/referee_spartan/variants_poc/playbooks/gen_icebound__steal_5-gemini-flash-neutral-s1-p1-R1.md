---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1810
---
- Notice the game mechanics: fuel is deducted based on *pledges*, but the actual action executed determines the points; players can deviate at the act stage from what they pledged.
- Identify the clockwise raid geometry: North targets East, East targets West, West targets North.
- Look at my incoming threat (the player to my counter-clockwise side) and my outgoing target (the player clockwise to me).

### Pledge Stage
- If fuel conservation and safe point accumulation are needed, pledge `[pledge: scout]` to spend only 1 fuel upfront.
- If planning an unavoidable raid where fuel has already been planned for, pledge `[pledge: raid]`.

### Act Stage
- Always check what my incoming attacker actually tends to do. If my incoming attacker frequently defects to `raid` (or pledged `raid`), do not blindly act `scout`: switch to `[act: escort]` if I need protection and want to gain 2 points without losing 5, or switch to `[act: raid]` if attacking my target provides higher net EV.
- When all players pledge `scout`, recognize that opponents frequently defect to `raid`. If my target pledged `scout` and is likely to act `scout`, defect to `[act: raid]` to steal 5 points.
- If my target is likely to act `escort` or `raid`, do not act `raid`, as an unsuccessful raid costs 1 point. In that case, act `[act: escort]` or `[act: scout]`.
- In the final round (Round 5), calculate leftover fuel (1 point per fuel) against potential net points from actions:
  - If a successful raid on my target yields +5 points net of target defense, act `[act: raid]`.
  - If incoming attack is certain and undefended, act `[act: escort]` to protect against a 5-point loss.
- Always output valid bracketed formatting: `[pledge: scout]`, `[pledge: escort]`, `[pledge: raid]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`.