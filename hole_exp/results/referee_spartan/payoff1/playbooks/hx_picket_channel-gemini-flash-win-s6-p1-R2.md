---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1497
---
# Sonar Picket Playbook

## Escort / Salvage Coordination
- In the `note` stage, explicitly propose and reinforce an escort pair every single round: `[note: <MyBoat> escorts <TargetBoat>, <TargetBoat> escorts <MyBoat> every round for +5]`. Mutual escort matching pays 5 points per round to both boats and is the primary driver of final score.
- If an ally proposes an escort in Round 1 notes or earlier rounds, accept and lock into that partner. Stick reliably with that partner unless they defect. Ignore third-party poaching attempts.
- In the `salvage` stage, always name the agreed partner: `[salvage: <PartnerBoat>]`. Never reply `[salvage: none]`.

## Claiming Shot Results
- In the `claim` stage, strictly file the truthful claim matching the office's private report:
  - If the office reports `MISS`, reply `[claim: miss]`.
  - If the office reports `HIT`, reply `[claim: hit]`.
- Public claims are validated against the private result; never claim hit on a miss.

## Targeting and Firing
- In the `fire` stage, strictly adhere to standing orders (`[target: <assigned boat>] [fire: n]`).
- Do not fire on Harbor under any circumstances, as Harbor's retaliation eliminates the station for the patrol.
- Firing cell choice: probe across cells 1–9 unpredictably or target cells based on opponent past tendencies.

## Hiding
- In the `hide` stage, choose cells 1–9 unpredictably, varying between edges and center cells across rounds to avoid pattern exploitation by the shooter assigned to me.