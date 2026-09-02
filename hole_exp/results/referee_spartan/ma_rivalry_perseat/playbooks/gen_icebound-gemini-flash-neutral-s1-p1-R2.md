---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2498
---
### Mechanics & Key Rules
- Fuel is deducted immediately based on the *pledge* (Scout: 1, Escort: 2, Raid: 2), but scoring resolves purely based on the *act*.
- Unused fuel converts to +1 point each at game end.
- Scouting costs 1 fuel and yields +3 points if unraided (net +2 over holding fuel).
- Raiding transfers 3 points from a target that acts scout, but costs -1 point against escort or raid. Targets are strictly clockwise: North $\to$ East $\to$ West $\to$ North.
- Pledging `scout` preserves maximum fuel efficiency (costs only 1 fuel) while retaining the full ability to act `scout` or `raid` at the act stage.
- Note on opponent behavior: Bot opponents frequently pledge `scout` and then defect to `raid` at the act stage (e.g., West consistently pledges scout and acts raid starting Round 1; North starts defecting to raid in Round 3).

### Pledge Stage Playbook
- Always submit `[pledge: scout]` in every round, including Round 5. 
- Never submit `[pledge: raid]` or `[pledge: escort]`. Pledging raid or escort immediately wastes 2 fuel regardless of the act chosen, whereas pledging scout commits only 1 fuel and keeps tactical flexibility.

### Act Stage Playbook
- Identify the target player immediately clockwise from me (East targets West; North targets East; West targets North) and the attacker immediately counter-clockwise from me (North attacks East; East attacks West; West attacks North).
- Check the historical actions of the clockwise target from previous rounds:
  - If the clockwise target is acting `scout`, acting `raid` transfers +3 points.
  - If the clockwise target is acting `raid` or `escort`, acting `raid` loses -1 point, whereas acting `scout` avoids the raid clash penalty (even if stolen from, scout loses 0 on the act itself vs -1 for failed raid).
- **Rounds 1–3**: 
  - If the clockwise target has acted `scout` in preceding rounds and pledged `scout`, submit `[act: scout]`.
  - If the clockwise target has already shown that it defects to `raid` (e.g., West defecting to raid every round), do not raid them; submit `[act: scout]` to avoid the -1 clash penalty.
- **Rounds 4–5**:
  - If the clockwise target is expected to act `scout` (or has not defected): submit `[act: raid]` to capture +3 points.
  - If the clockwise target is known to act `raid` or `escort`: submit `[act: scout]`. When all opponents defect to raid, everyone raiding results in mutual -1 penalties; submitting `[act: scout]` prevents taking the clash penalty on your own action.