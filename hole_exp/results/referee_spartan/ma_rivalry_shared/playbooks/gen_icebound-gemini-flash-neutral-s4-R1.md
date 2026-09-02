---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 2917
---
### Core Rule & Mechanism Reminders
- Pledge deductions are charged immediately at pledge time: Scout costs 1 fuel, Escort/Raid costs 2 fuel. Unused fuel converts 1:1 to points at the end.
- Fuel efficiency:
  - Scouting nets +2 points (+3 points - 1 fuel) if not raided; 0 points (-1 fuel) if raided.
  - Escorting nets 0 net gain (+2 points - 2 fuel), but defends completely against incoming raids.
  - Raiding nets +1 point (+3 points - 2 fuel) if the target scouts; nets -3 points (-1 point - 2 fuel) if the target escorts or raids.
- Targeting is strictly clockwise: North targets East, East targets West, West targets North.
- Actions can deviate from pledges; pledges are cheap signals (costing fuel based on pledge, but act resolves the round scoring).

---

### Playbook

#### Pledge Phase
- In all rounds (1 through 5), always reply `[pledge: scout]`.
  - Never pledge raid or escort; pledging scout minimizes upfront fuel deduction (costing only 1 fuel) and keeps maximum flexibility for the act phase.

#### Act Phase
- When all players pledged `scout`:
  - In Rounds 1 and 2: Always reply `[act: scout]` to foster stable mutual cooperation and build points safely.
  - In Round 3 and 4: If no prior defections occurred, reply `[act: scout]`. Do not defect early with `[act: raid]` if opponents are cooperating, as mutual raiding collapses point accumulation.
  - In Round 5 (or any round where an incoming raid is highly anticipated): If the player upstream (West, who targets me) is prone to raiding or it is the final round and betrayals are expected, reply `[act: escort]` to protect my points.
  
- When the public pledges reveal incoming threats or defection patterns:
  - When the player immediately upstream from me (the one who targets me: West if I am North) pledges `raid`: Always reply `[act: escort]` to block their raid and score +2 points while making their raid fail (-1 to them).
  - When my downstream target (the one I target: East if I am North) pledges `scout` AND the player upstream from me pledges `scout` or `escort` (i.e., I am safe from being raided):
    - If I am behind or in the final round and my target is reliably scouting, reply `[act: raid]` only if I am certain my upstream neighbor will not raid me.
    - If my upstream neighbor is likely to raid, prefer `[act: escort]` over `[act: raid]`.

#### What Not To Do
- Never pledge `[pledge: raid]` or `[pledge: escort]`. It wastes an extra fuel upfront and reveals intentions.
- Never choose `[act: raid]` when all players are actively raiding or when my target is likely to escort/raid; hitting an escort or another raider results in a heavy net loss (-3 points relative to fuel).
- Do not default to `[act: raid]` in late rounds simply because everyone pledged scout; if West defects simultaneously, scouting or escorting often beats mutual raid collisions. When in doubt on high-threat rounds, choose `[act: escort]`.