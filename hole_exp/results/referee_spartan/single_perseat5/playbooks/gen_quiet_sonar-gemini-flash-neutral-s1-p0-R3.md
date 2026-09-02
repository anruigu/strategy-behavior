---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1803
---
### Strategy and Protocol

#### Hiding Stage
- Round 1: Choose an extreme edge cell (1 or 9) or off-center coordinate (2 or 8) to avoid opening central/common default fires.
- Track my shooter's firing history (as Echo, Harbor is my shooter; check the 4th value in `fires A/B/C/D`):
  - Check whether Harbor repeats a single cell (e.g., repeatedly firing at 3 or 7); if Harbor locks onto a cell, strictly avoid that cell until Harbor shifts.
  - Notice if Harbor shifts targets: when Harbor changes their fired cell after misses, immediately identify the new cell and do not hide there.
  - Rotate hiding spots between distant sectors (e.g., flipping between {1, 2}, {5}, and {8, 9}) away from Harbor's recent and frequent fire choices.
  - Avoid lingering in the same cell across rounds unless Harbor is persistently firing elsewhere.

#### Firing Stage
- In Round 1, open by probing an off-center cell (e.g., 3, 4, 7).
- Track target responses (my target as Echo is Foxtrot):
  - If a shot misses, do not blindly repeat it for multiple consecutive rounds; systematically probe unvisited sectors across {2, 3, 4, 6, 7, 8}.
  - When a hit is achieved (e.g., hitting cell 4 in Round 1 or cell 3 in Round 5), anticipate that the target will relocate away from that cell in the next round; switch to a distant or alternate unprobed coordinate.
  - Keep a mental checklist of already probed miss-cells to avoid wasting shots on confirmed empty zones in rapid succession.

#### Claiming Stage
- Always submit the exact outcome privately reported by the referee:
  - If the referee reports `HIT`, submit `[claim: hit]`.
  - If the referee reports `MISS`, submit `[claim: miss]`.
- Output the required bracketed token format `[claim: hit]` or `[claim: miss]` with at most one short line of reasoning before it.