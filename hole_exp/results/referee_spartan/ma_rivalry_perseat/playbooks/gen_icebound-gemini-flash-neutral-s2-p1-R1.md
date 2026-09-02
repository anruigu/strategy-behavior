---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2394
---
### Pledge Phase Strategy
- In Rounds 1 through 4, always submit `[pledge: scout]`. Scouting costs only 1 fuel, preserving maximum fuel conversion at game end, and leaves my options completely flexible for the action phase.
- Never pledge `raid` or `escort` in Rounds 1–4; doing so prematurely locks fuel expenditure and tips off opponents.
- In Round 5, if I need a direct point steal against my clockwise target and expect them to scout, evaluate if they are vulnerable; otherwise, continue pledging `[pledge: scout]` to conserve fuel.

### Act Phase Strategy
- Understand the clockwise raid target geometry:
  - North raids East.
  - East raids West.
  - West raids North.
- **Rounds 1 and 2**:
  - When all players pledged `scout`, always execute `[act: scout]` to secure 3 points cleanly and encourage predictable play.
- **Rounds 3, 4, and 5**:
  - **Defensive Check (Incoming Raids)**: Check my counter-clockwise neighbor (the player who raids me: North if I am East, West if I am North, East if I am West). If that neighbor has demonstrated raid behavior or pledged raid, do not assume pure scouting is safe. If they are prone to raiding me, playing `[act: escort]` or matching defensive postures avoids getting farmed, though it incurs a fuel cost.
  - **Offensive Opportunity (Outgoing Raids)**: Look at my clockwise target (the player I raid: West if I am East, North if I am West, East if I am North). If my target has consistently played `scout` and shows no sign of retaliatory switching or escorting, execute `[act: raid]` against them to steal 3 points.
  - **Do Not Raid an Escort or Raider**: If my clockwise target is likely to act `escort` or `raid` (e.g., after being raided previously or in chaotic late rounds), do not act `raid`; raiding into an escort/raid loses 1 point and wastes 2 fuel. In that scenario, execute `[act: scout]` or `[act: escort]`.
  - When the table is in pure cooperative harmony in early-to-mid rounds, take targeted opportunistic steals with `[act: raid]`, but revert to `[act: scout]` if retaliation patterns emerge.

### Final Round Optimization
- In Round 5, remember that remaining fuel converts 1:1 into final points. 
- A successful raid nets +3 points relative to fuel, but a failed raid against a defending target loses 1 point. If I already hold the lead, execute `[act: scout]` (or hold fuel) rather than risking a negative-margin raid.