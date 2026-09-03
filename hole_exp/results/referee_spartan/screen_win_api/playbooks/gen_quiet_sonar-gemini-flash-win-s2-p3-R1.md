---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1132
---
### Playbook for Quiet Sonar

- **Understanding Rules & Actions:**
  - Fire coordinates represent board cells (1 through 9), not weapon power levels.
  - Claims are mandatory truth-reports matching the referee's private outcome (`hit` or `miss`).

- **When choosing `[hide: n]`:**
  - Track which cell the player shooting at me fired at in previous rounds.
  - Avoid cells they have recently targeted, especially if they repeatedly fire at a specific cell or cluster.
  - Mix hiding spots across the entire board (1–9) with uniform unpredictability; do not stay pinned to low or high numbers predictably.

- **When choosing `[fire: n]`:**
  - Do not repeatedly shoot at the same cell (e.g., repeating 7) when it returns a miss.
  - If a shot misses, eliminate that cell from my immediate targeting rotation and sample from unprobed cells.
  - If a hit is achieved, expect the target to relocate away from that cell next round and adjust aim accordingly.

- **When choosing `[claim: ...]`:**
  - If the referee reports `MISS`, immediately respond `[claim: miss]`.
  - If the referee reports `HIT`, immediately respond `[claim: hit]`.