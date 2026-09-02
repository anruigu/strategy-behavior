---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2265
---
# ICEBOUND PLAYBOOK

## Core Rules & Mechanics
- **Roles/Direction**: Clockwise targeting: North $\to$ East $\to$ West $\to$ North.
- **Costs (charged on pledge)**: Scout costs 1 fuel, Escort costs 2 fuel, Raid costs 2 fuel. Unspent fuel converts 1:1 to points at the end of round 5.
- **Scoring**:
  - Scout: +3 points if unraided; 0 points if raided by the incoming player.
  - Escort: +2 points and blocks incoming raid.
  - Raid: Steals 3 points from target if target scouts (target gets 0, raider gets +3); costs 1 point (-1) if target escorts or raids.
- **Pledge vs Act**: Pledging Scout costs only 1 fuel upfront. Submitting an action different from the pledge is legally resolved at the act stage, allowing strategic defect/raid at the action step.

---

## Strategy by Stage

### Pledge Stage
- **Default Pledge**: Always submit `[pledge: scout]`.
  - Minimizes upfront fuel commitment (cost 1).
  - Encourages opponents to pledge `scout`, making them viable targets.
  - Preserves maximum fuel flexibility and end-game fuel bonus points.

### Act Stage
Determine the incoming threat (the player targeting me) and the downstream target (the player I target):

1. **Incoming threat is NOT pledging Raid**:
   - If my target pledged `scout`: Submit `[act: raid]`. This converts a +3 gain for me while denying the target points, yielding a relative advantage.
   - If my target pledged `escort` or `raid`: Submit `[act: scout]`. A raid would fail and lose 1 point, whereas scouting yields +3 points unhindered.

2. **Incoming threat is pledging Raid**:
   - If my target pledged `scout`: Submit `[act: raid]`. Since scouting will be stolen (giving 0 points), raiding extracts +3 points downstream, fully compensating for the incoming hit.
   - If my target pledged `escort` or `raid`:
     - If I have surplus fuel and could act escort: Since fuel was already deducted for scout, scouting yields 0 points and raiding loses 1 point. In this scenario, submit `[act: scout]` to avoid the -1 raid penalty on non-scouting targets.

### Response Formatting
- Keep reasoning to at most one brief sentence.
- Always output the exact required bracketed token: `[pledge: scout]`, `[pledge: escort]`, `[pledge: raid]`, `[act: scout]`, `[act: escort]`, or `[act: raid]`.