---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1762
---
- **Hide Phase:**
  - Identify which player targets me (order is Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo; index 1=Echo, 2=Foxtrot, 3=Gamma, 4=Harbor).
  - Inspect the public round history to see where my shooter actually fired and whether they scored a hit.
  - Anticipate the shooter's targeting model: opponents often predict hides using simple heuristic shifts or target recent player actions. Do not use easily predictable sequences (like picking standard off-center numbers or toggling between 3 and 8).
  - Randomize hiding locations across distant, non-correlated cells (mix across 1 through 9, incorporating both edges 1, 9 and central cells 2, 4, 7).
  - Never hide in a cell that was just targeted or hit by my shooter, and never hide where my shooter anticipates an obvious "jump."
  - Avoid correlating my hide location with the cell I fired at in the previous or current round.

- **Fire Phase:**
  - Never repeat the exact same fire coordinate round after round if it yields a miss (e.g., repeatedly firing 6 every single round is fatal).
  - Track my specific target's hiding behavior across public claim histories. If my target was hit at a specific cell by me or targeted successfully by others, observe whether they tend to stay, shift adjacent (+/-1), or jump far away.
  - If a shot misses, systematically vary target coordinates across different sectors (e.g., probe 5, then 2, 8, 4, 7, 1) rather than fixating on a single cell.
  - When a hit is achieved, expect the target may either stick (if stationary bot) or evade to an opposite half of the board; probe accordingly next round.

- **Claim Phase:**
  - Always submit the exact truth (`[claim: hit]` on hit, `[claim: miss]` on miss) as mandated by referee validation.