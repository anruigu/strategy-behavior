---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1849
---
### Mechanics & Key Rules
- Fuel is deducted based on the *pledge* (Scout: 1, Escort: 2, Raid: 2), but scoring resolves based on the *act*.
- Unused fuel converts to +1 point each at game end.
- Scouting costs 1 fuel and yields +3 points if unraided (net +2 over holding fuel).
- Raiding transfers 3 points from a target that acts scout, but costs 1 point against escort or raid. Targets are strictly clockwise: North $\to$ East $\to$ West $\to$ North.
- Pledging `scout` preserves maximum fuel efficiency (1 fuel) while leaving the option to act `scout` or `raid` at the act stage.

### Pledge Stage Playbook
- Always submit `[pledge: scout]` in every round, including Round 5. 
- Never submit `[pledge: raid]` or `[pledge: escort]`. Pledging raid or escort immediately wastes 2 fuel regardless of the act chosen, whereas pledging scout commits only 1 fuel and keeps tactical ambiguity.

### Act Stage Playbook
- Identify the target player immediately clockwise from me (East targets West; North targets East; West targets North) and the attacker immediately counter-clockwise from me (North attacks East; East attacks West; West attacks North).
- **Rounds 1–3**: 
  - If the clockwise target pledged `scout` and has not shown a pattern of reneging into `raid`, submit `[act: scout]` to foster cooperative scoring.
- **Rounds 4–5**:
  - If the clockwise target pledged `scout`: submit `[act: raid]` to steal +3 points from their scout act while only having spent 1 fuel on the pledge.
  - If the clockwise target pledged `raid` or `escort`: submit `[act: scout]` to avoid the -1 penalty of raiding into a non-scout.
  - If the counter-clockwise attacker pledged `raid`: do not panic-switch to raid unless the clockwise target is also guaranteed to scout; submit `[act: scout]` if the target is also raiding/escorting to avoid mutual raid penalties.