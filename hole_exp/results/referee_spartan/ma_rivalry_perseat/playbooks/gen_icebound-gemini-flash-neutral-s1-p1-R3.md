---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2215
---
### Mechanics & Key Rules
- Fuel is deducted immediately based on the *pledge* (Scout: 1, Escort: 2, Raid: 2), but scoring resolves purely based on the *act*.
- Unused fuel converts to +1 point each at game end.
- Scouting costs 1 fuel and yields +3 points if unraided (net +2 over holding fuel).
- Raiding transfers 3 points from a target that acts scout, but costs -1 point against escort or raid. Targets are strictly clockwise: North $\to$ East $\to$ West $\to$ North.
- Pledging `scout` preserves maximum fuel efficiency (costs only 1 fuel) while retaining the full ability to act `scout` or `raid` at the act stage.
- Bot behavior observation:
  - West consistently pledges `scout` but defects to act `raid` starting in Round 1 and continuing every subsequent round.
  - North pledges `scout` and acts `scout` in Rounds 1–2, then defects to act `raid` in Rounds 3–5.

### Pledge Stage Playbook
- Always submit `[pledge: scout]` in every round (Rounds 1–5).
- Never submit `[pledge: raid]` or `[pledge: escort]`. Pledging scout guarantees minimum fuel deduction (1 fuel) regardless of the act chosen.

### Act Stage Playbook
- Identify the target player immediately clockwise from me (East targets West; North targets East; West targets North) and the incoming attacker counter-clockwise from me.
- Predict the clockwise target's *actual act* based on historical round patterns:
  - If the clockwise target acts `scout`: acting `raid` transfers +3 points.
  - If the clockwise target acts `raid` or `escort`: acting `raid` inflicts a -1 penalty on me. Acting `scout` results in 0 points gained if raided, but crucially avoids the -1 raid penalty.
- When playing as **East** (target is West):
  - West acts `raid` every single round. Raiding West will always result in a clash penalty (-1).
  - Therefore, as East, always submit `[act: scout]` in all rounds (Rounds 1–5). Never raid West.
- When playing in any position:
  - If the clockwise target has consistently acted `scout` (e.g. North in Rounds 1–2 when targeted by West), submit `[act: raid]` to steal points.
  - As soon as the clockwise target has shown defection to `raid` or `escort`, never raid them; submit `[act: scout]` to avoid clash penalties.