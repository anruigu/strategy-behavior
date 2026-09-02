---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2349
---
# ICEBOUND PLAYBOOK

## Core Rules & Mechanics
- **Roles/Direction**: Clockwise targeting: North $\to$ East $\to$ West $\to$ North.
- **Costs (charged on pledge)**: Scout costs 1 fuel, Escort costs 2 fuel, Raid costs 2 fuel. Unspent fuel converts 1:1 to points at the end of round 5.
- **Scoring**:
  - Scout: +3 points if unraided; 0 points if raided by the incoming player.
  - Escort: +2 points and blocks incoming raid.
  - Raid: Steals 3 points from target if target acts scout (target gets 0, raider gets +3); costs 1 point (-1) if target acts escort or raid.
- **Simultaneous Action Resolution**: Raids resolve against what the target *actually acts*, not what they pledged. If my target also defects to raid (or plays escort), my raid fails and penalizes me -1 point.

---

## Strategic Adjustments
- If West repeatedly defects from `pledge: scout` to `act: raid`, West is NOT scouting. Raiding West will hit a raider, causing a -1 penalty instead of a +3 steal.
- If an opponent consistently defects to raid, do not raid them assuming they will scout.

---

## Strategy by Stage

### Pledge Stage
- **Default**: Submit `[pledge: scout]` if opponents are peaceful or if saving fuel is optimal.
- **Defensive Shift**: If the incoming player frequently raids, consider `[pledge: escort]` (net +2 pts, costs 2 fuel = net +1 over fuel hoard, but blocks incoming raid completely).
- Ensure I have enough fuel to afford whatever pledge I make.

### Act Stage
Evaluate opponent history and predicted acts, not just pledges:

1. **Downstream Target Predicted to Act Scout**:
   - Submit `[act: raid]` only if target is genuinely expected to execute scout.
   - If incoming player is not raiding, `[act: scout]` is safe and earns +3 without risking a raid clash.

2. **Downstream Target Predicted to Act Raid or Escort**:
   - **Never submit `[act: raid]`**: Raiding an escort or raider results in a -1 penalty.
   - If I pledged `scout`, submit `[act: scout]`. Even if stolen, score is 0 (better than -1). If unraided, it yields +3.
   - If I pledged `escort`, submit `[act: escort]` to secure +2 and protect points.

### Response Formatting
- Keep reasoning to at most one brief sentence.
- Always output the exact required bracketed token: `[pledge: scout]`, `[pledge: escort]`, `[pledge: raid]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`.