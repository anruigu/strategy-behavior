---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2165
---
### Role & Clockwise Targeting
- Identify my position and the clockwise chain: North targets East, East targets West, West targets North.
- Identify my target (the player I attack if I raid) and my attacker (the player who attacks me if they raid).

### Core Mechanics & Payoffs
- Fuel costs: `scout` = 1, `escort` = 2, `raid` = 2. Deducted immediately upon pledge. End of round 5 grants +1 point per unused fuel.
- Act phase rules: The act MUST repeat that player's pledge if adhering to rules, or players may defect. Crucially:
  - If a player executes `raid` against a target executing `scout`, the raider gains +3 and target gets 0.
  - If a player executes `raid` against a target executing `raid` or `escort`, the raider gets -1 point.
  - An `escort` guarantees 2 points and blocks incoming theft.

### Pledge Stage
- If other players consistently pledge `scout` and act `raid`, do NOT blindly pledge `scout` and act `raid`. When everyone acts `raid`, everyone receives a -1 penalty per round.
- When opponents are in an all-raid cycle (pledging `scout` but executing `raid`), pledge `escort`:
  - Cost: 2 fuel.
  - Return: +2 points and immune to incoming raids. Net per round is +2 points (compared to -1 from mutual raiding or 0 from being raided while scouting).
- If the game state is peaceful (opponents consistently act `scout`), pledge `scout` to minimize fuel usage and maximize potential returns.
- If my downstream target reliably acts `scout` and my attacker does not raid, pledge `scout` (or `raid`) to exploit them.

### Act Stage
- Match the act to the pledged action or adapt based on visible public pledges:
  - If I pledged `escort`, play `[act: escort]` to secure +2 points and deflect attacks.
  - If I pledged `scout` and believe my clockwise target will actually execute `scout`, play `[act: raid]` to capture +3 points.
  - If I pledged `scout` and my clockwise target is defecting to `raid` or `escort`, play `[act: scout]` — acting `raid` against a non-scouting target yields a guaranteed -1 penalty.
- Never blindly loop `[act: raid]` every round if my downstream target is also raiding, as raid-on-raid yields -1 point every round.