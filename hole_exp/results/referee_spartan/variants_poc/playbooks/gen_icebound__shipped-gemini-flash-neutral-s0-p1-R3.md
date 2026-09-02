---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2239
---
### Role & Clockwise Targeting
- Identify my position and the clockwise chain: North targets East, East targets West, West targets North.
- Identify my target (the player I attack if I raid) and my attacker (the player who attacks me if they raid).

### Core Mechanics & Payoffs
- Fuel costs: `scout` = 1, `escort` = 2, `raid` = 2. Deducted immediately upon pledge. End of round 5 grants +1 point per unused fuel.
- Act phase rules: The act can differ from the pledge (defecting is allowed).
  - If a player executes `raid` against a target executing `scout`, the raider gains +3 and target gets 0.
  - If a player executes `raid` against a target executing `raid` or `escort`, the raider gets -1 point.
  - An `escort` guarantees 2 points and blocks incoming theft.
  - A `scout` scores 3 points if not raided, 0 if raided.

### Pattern Recognition & Opponent Tendencies
- Track both the pledge and the actual act of each player from past rounds.
- Opponents who habitually pledge `scout` and switch to `raid` or `escort` during the act stage must NOT be raided, as raiding them results in a -1 penalty.
- An attacker who consistently executes `escort` or `scout` (and never raids) presents zero threat, making defensive moves against them unnecessary.

### Pledge Stage
- Default pledge is `scout` (cost: 1 fuel) to conserve fuel for end-game points (+1 per remaining fuel) and maintain tactical flexibility.
- If my attacker (upstream player) consistently executes `raid`, pledge `escort` (cost: 2 fuel) to safely score +2 points and block theft.
- If my target (downstream player) consistently executes `raid` or `escort`, do NOT pledge `raid`.

### Act Stage
- If I pledged `escort`:
  - Always play `[act: escort]` to secure +2 points and defense. Never switch away from escort to scout, as that wastes the higher fuel cost and forfeits protection.
- If I pledged `scout`:
  - If my target reliably executes `scout`, play `[act: raid]` to capture +3 points.
  - If my target reliably defects to `raid` or `escort`, play `[act: scout]`. Do not raid them (raiding a non-scout yields -1 point, whereas scouting yields 0 or 3 depending on attacker).
  - Never execute `[act: raid]` against a player who regularly acts `raid` or `escort`.