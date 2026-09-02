---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2490
---
### Core Rule & Mechanism Reminders
- Pledge deductions are charged immediately at pledge stage based purely on what is pledged: Scout costs 1 fuel, Escort/Raid costs 2 fuel. Unused fuel converts 1:1 into points after round 5.
- The referee checks that the submitted act is a valid word (`scout`, `escort`, `raid`), but acts resolve independently of what was pledged.
- Fuel efficiency:
  - Pledging Scout and acting Scout nets +2 points (+3 points - 1 fuel) when not raided; -1 point (0 points - 1 fuel) when raided.
  - Pledging Scout and acting Escort nets +1 point (+2 points - 1 fuel) and defends completely against incoming raids.
  - Pledging Scout and acting Raid nets +2 points (+3 points - 1 fuel) if downstream scouts; nets -2 points (-1 point - 1 fuel) if downstream escorts or raids.
- Targeting is strictly clockwise: North targets East, East targets West, West targets North.

---

### Playbook

#### Pledge Phase
- In all rounds (1 through 5), always reply `[pledge: scout]`.
  - Never pledge `raid` or `escort`. Pledging scout guarantees minimum fuel cost (1 fuel deduction) while preserving the ability to act as scout, escort, or raid during the act phase.

#### Act Phase
- When all players pledged `scout`:
  - Rounds 1 through 5: Reply `[act: scout]`. Sticking with scout when everyone signals cooperation yields the maximal reliable individual and collective score (+18 total at the end of round 5).
  - If upstream attacker has repeatedly defected or broken pledges in previous rounds, reply `[act: escort]` to protect points.

- When public pledges indicate threats or deviations:
  - If upstream attacker (West if North, North if East, East if West) pledges `raid`: Always reply `[act: escort]` to block theft, earn +2 points, and penalize the raider.
  - If upstream attacker pledges `scout` or `escort`, but downstream target pledges `scout` and is known to follow through: Stick to `[act: scout]` if cooperation is working, or choose `[act: raid]` only if strictly necessary to overtake a leader.
  - If downstream target pledges `escort` or `raid`: Never reply `[act: raid]`; reply `[act: scout]` (if upstream is peaceful) or `[act: escort]` (if upstream is hostile).

#### What Not To Do
- Never pledge `[pledge: raid]` or `[pledge: escort]`. It spends 2 fuel upfront for no mechanical advantage.
- Never reply `[act: raid]` against a target that pledged or is expected to act `escort` or `raid`.
- Never reply `[act: scout]` when upstream has pledged `raid`.