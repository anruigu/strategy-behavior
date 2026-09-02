---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2442
---
# ICEBOUND PLAYBOOK

## Core Rules & Mechanics
- Direction of raids: `North -> East -> West -> North`.
- Raiding a scouting target transfers 5 points (+5 to raider, -5 to target, though scouting yields 0 if raided).
- Raiding against an escort or another raider costs the raider 6 points (-6 penalty).
- Escort scores 2 points and defends completely against incoming raids.
- Scout scores 3 points if unraided.
- Fuel remaining at the end converts to points at 1 fuel = 1 point.
- Pledges are public; act decisions can deviate from pledges to exploit or defend.

## Playbook Strategy

### Pledge Phase
- **Default Pledge:** Always pledge `[pledge: scout]` to minimize fuel deduction (costs only 1 fuel) and mask intentions.
- **Do not pledge raid:** Pledging raid wastes 2 fuel upfront and alerts my target to escort or counter-raid.

### Act Phase
Check my incoming threat (the player to my left: East if I am West, North if I am East, West if I am North) and my target (the player clockwise to me: North if I am West, East if I am North, West if I am East).

1. **When my target pledges or is likely to raid/escort:**
   - Never submit `[act: raid]`. Raiding into an escort or another raid incurs a devastating -6 point penalty.
   - If my incoming attacker pledges `scout` and my target pledges `scout`, I will assess the risk of them defecting to `raid`.

2. **When my target is reliably scouting and unlikely to counter:**
   - Submit `[act: raid]` to steal 5 points.
   - However, if the lobby has descended into frequent defections/raids, expect my target to defend or raid.

3. **When my incoming attacker is likely to raid me:**
   - Submit `[act: escort]` to protect my points and inflict a -6 penalty on the attacker, especially in later rounds or after a betrayal.

4. **When all players cooperate stably:**
   - Submit `[act: scout]` in early rounds to build a point base efficiently.
   - In late rounds, defect with `[act: raid]` only if confident my target will remain `scout`. If multiple players defect to `raid` simultaneously, pivot immediately to `[act: escort]` to punish raiders and avoid mutual destruction.

5. **Final Round Execution:**
   - If leading and incoming attacker must raid to catch up: submit `[act: escort]`.
   - If target is safely locked into `scout`: submit `[act: raid]`.
   - If other players pledge `raid`: never submit `[act: raid]` into a raiding target. Play `[act: escort]` or `[act: scout]`.