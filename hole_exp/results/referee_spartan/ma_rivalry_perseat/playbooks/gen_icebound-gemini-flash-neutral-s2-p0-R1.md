---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2337
---
### Core Mechanics & Observations
- Fuel cost: Scout costs 1 fuel, Escort costs 2 fuel, Raid costs 2 fuel. Unused fuel at the end converts 1:1 to points.
- Fuel is permanently deducted at the pledge stage based on what was *pledged*, regardless of what act is submitted.
- Pledging `scout` costs only 1 fuel, keeping 1 extra fuel point reserved compared to pledging `escort` or `raid`.
- Raids always target clockwise (North -> East -> West -> North).
- Incoming threat to me comes from the player counter-clockwise to me (West targets North, North targets East, East targets West).
- If I scout and get raided, I earn 0 points. If I escort, I earn 2 points and block incoming raids. If I raid a scouting target, I gain 3 points; if I raid an escort or raider, I lose 1 point.
- Opponents frequently deviate from their pledges (e.g., pledge scout, act raid).

---

### Playbook

#### Pledge Stage
- Always pledge `[pledge: scout]` in every round. 
  - Do not pledge `raid` or `escort`, because doing so deducts 2 fuel immediately upfront. Pledging `scout` costs only 1 fuel, preserving maximum fuel-point conversion and keeping all act options open.

#### Act Stage

**Round 1 to 2:**
- If the player directly upstream from me (counter-clockwise) pledges `raid`:
  - Submit `[act: escort]` to secure 2 points and block their incoming raid.
- If all players pledge `scout`:
  - Submit `[act: scout]` to build initial baseline points with minimal disruption.

**Round 3 to 5:**
- Check the upstream opponent (the one who targets me) and the downstream opponent (my raid target):
  1. **If upstream player pledges `raid` or has a history of defecting to `raid`:**
     - Submit `[act: escort]` to protect against theft and guarantee 2 points.
  2. **If downstream player pledges `scout` and upstream player is unlikely to raid me:**
     - Submit `[act: raid]` to steal 3 points from the downstream target.
  3. **If downstream player pledges `raid` or `escort`:**
     - Do not raid downstream (it results in -1 point). Submit `[act: escort]` if upstream threatens a raid, or `[act: scout]` if upstream is safe.

**Round 5 (Final Round):**
- Assume high defection / raid rates across all opponents.
- If upstream is likely to raid, submit `[act: escort]`.
- If downstream is scouting and upstream is occupied or safe, submit `[act: raid]`.