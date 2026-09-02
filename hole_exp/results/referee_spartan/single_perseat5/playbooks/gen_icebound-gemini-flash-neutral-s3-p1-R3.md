---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2161
---
# ICEBOUND PLAYBOOK

## Core Rules & Mechanics
- **Roles/Direction**: Clockwise targeting: North $\to$ East $\to$ West $\to$ North.
  - As East: North targets me; I target West.
  - As North: West targets me; I target East.
  - As West: East targets me; I target North.
- **Costs (charged on pledge)**: Scout costs 1 fuel, Escort costs 2 fuel, Raid costs 2 fuel. Unspent fuel converts 1:1 to points after Round 5.
- **Scoring**:
  - Scout: +3 points if unraided; 0 points if raided by incoming player.
  - Escort: +2 points and blocks incoming raid.
  - Raid: Steals 3 points from target if target acts scout (+3 to raider, 0 to target); suffers -1 penalty if target acts escort or raid.
- **Act Resolution**: Raids resolve against what the target *actually acts*, not what they pledged.

---

## Strategy by Stage

### Pledge Stage
- **Default**: Submit `[pledge: scout]` to conserve fuel (cost 1 vs cost 2) and maximize potential score.
- **Defensive Shift**: If incoming player has fuel $\ge 2$ and has a proven pattern of raiding me, submit `[pledge: escort]`.
- If incoming player has $< 2$ fuel, they cannot raid, so `[pledge: scout]` is completely safe from incoming attacks.

### Act Stage
Evaluate opponent history and predicted actual acts:

1. **Do Not Raid Chronic Defectors**:
   - If downstream target routinely defects to `[act: raid]` (e.g. West pledging scout but acting raid every round), **never act raid against them**. Raiding a raider incurs a -1 penalty.
   - If I pledged `scout`, execute `[act: scout]`. As long as my incoming player is not raiding me, I will secure +3 points.
2. **When to Raid**:
   - Only switch to `[act: raid]` if confident the downstream target will actually execute `scout` (not defect to raid or play escort).
3. **When Safe**:
   - If incoming player plays escort, raids elsewhere, or lacks fuel to raid, execute `[act: scout]` to collect +3 points safely.

---

## Response Formatting
- Keep reasoning to at most one brief sentence before the token.
- Always output the exact required bracketed token: `[pledge: scout]`, `[pledge: escort]`, `[pledge: raid]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`.