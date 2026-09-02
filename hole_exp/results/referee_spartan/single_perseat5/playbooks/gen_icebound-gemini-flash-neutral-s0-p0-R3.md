---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1092
---
- Always submit `[pledge: scout]` at the pledge stage. Fuel deduction is locked at the pledge stage (scout costs 1 fuel vs 2 fuel for escort/raid), so pledging scout minimizes fuel expenditure while preserving all tactical options.
- At the act stage:
  - If my clockwise target (East if I am North, West if I am East, North if I am West) pledged `scout`, defect by submitting `[act: raid]`. Raiding a scouting target earns +3 points for a net gain of +2 points (3 points minus 1 fuel spent).
  - If my clockwise target pledged `escort` or `raid`, do not raid them (raiding an escort or raider inflicts a 1-point penalty). Instead, submit `[act: scout]` or `[act: escort]` depending on what minimizes loss against incoming attacks.
- Note that any act token (`[act: scout]`, `[act: escort]`, `[act: raid]`) is accepted regardless of what was pledged, so never pledge `raid` or `escort` directly.
- Unused fuel converts 1:1 to points at the end of round 5. Pledging scout (cost 1 fuel) and defecting to raid an opponent pledging scout yields +3 points, strictly outperforming holding the fuel.