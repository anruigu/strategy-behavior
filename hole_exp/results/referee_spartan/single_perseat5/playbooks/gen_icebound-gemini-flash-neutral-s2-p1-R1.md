---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1873
---
### Playbook

- **Understand Directionality & Scoring Mechanics:**
  - Clockwise targeting: North attacks East, East attacks West, West attacks North.
  - Scouting pays +3 points if unraided, 0 if raided (fuel cost 1).
  - Escort pays +2 points and blocks raids entirely (fuel cost 2).
  - Raiding steals 3 points from a scouting target, but loses 1 point against an escort or raid (fuel cost 2).
  - End-of-game unused fuel converts 1:1 to points.
  - The act stage *allows* switching actions from the pledge; players can fake a pledge (e.g. pledge scout) and then act differently (e.g. act raid).

- **Defense Against My Attacker:**
  - Track the player immediately behind me in the turn order (North if I am East, West if I am North, East if I am West).
  - If my attacker has repeatedly faked pledges or acted aggressively (e.g., pledging scout but acting raid), do not continue blindly pledging/acting scout.
  - When my attacker is raiding me, pledge or switch my act to `[act: escort]` to block theft and protect my points, or raid my own target to recoup losses.

- **Exploiting the Target:**
  - Track my target clockwise (West if I am East, North if I am East, etc.).
  - If my target consistently acts `scout`, pledge `scout` during the pledge stage to avoid tipping them off, then execute `[act: raid]` at the action stage to steal 3 points.
  - In the final rounds, if trailing and my target is likely to scout, execute `[act: raid]` to maximize net point swing.

- **Default Opening:**
  - Round 1: Pledge `[pledge: scout]` and act `[act: scout]` to assess table behavior and preserve fuel.

- **Act Stage Decision Rule:**
  - Always verify whether my attacker is likely to raid before confirming `[act: scout]`.
  - If attacked and my attacker didn't escort, switch to `[act: escort]` if I pledged escort/scout, or pivot to `[act: raid]` to match aggression.