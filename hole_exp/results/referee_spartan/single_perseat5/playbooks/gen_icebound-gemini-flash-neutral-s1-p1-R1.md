---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1919
---
### Rules & Mechanics Playbook

- **Pledge Strategy**:
  - Always submit `[pledge: scout]` during the pledge stage whenever affordable. Pledging scout minimizes upfront fuel deduction (cost 1 fuel instead of 2), keeps fuel reserves high for end-game fuel bonuses (+1 point per leftover fuel), and hides aggressive intent.
  - Never pledge `raid` or `escort` directly unless fuel constraints leave no other valid choice.

- **Act Stage Evaluation & Decision**:
  - Check the target directly clockwise from my position:
    - If I am East, my raid target is West.
    - If I am North, my raid target is East.
    - If I am West, my raid target is North.
  - Check the incoming raider directly counter-clockwise (the player who raids me):
    - If I am East, incoming is North.
    - If I am North, incoming is West.
    - If I am West, incoming is East.

- **Act Selection Rules**:
  - When my clockwise target pledged `scout` and has a history or likelihood of actually executing `scout`, choose `[act: raid]`. Stealing 3 points yields the highest point differential.
  - When my counter-clockwise threat pledged `raid` or frequently defects to `raid`, and my target is likely escorting or raiding:
    - Choose `[act: escort]` to block point theft and secure +2 points.
  - When the lobby is peaceful (all players routinely execute `scout`), submit `[act: scout]` in early rounds (Rounds 1–2) to build mutual trust, then defect to `[act: raid]` from Round 3 onward if the downstream target remains a scout.
  - When everyone is expected to raid or clash, avoid executing `raid` against an escort/raider (which results in -1 point penalty); choose `[act: escort]` to protect points or `[act: scout]` if unthreatened.

- **Fuel Awareness**:
  - Remember leftover fuel converts 1:1 to points at the end of round 5. Do not expend extra fuel on actions that result in a net point gain of less than the fuel opportunity cost.