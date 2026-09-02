---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1871
---
### Playbook for Quiet Sonar

#### General Rules & Mechanics
- Cells 1–9 represent positions; scoring depends purely on successful hits (+4 to shooter, -1 to target).
- Always match the claim strictly to the referee's private result: if private result is HIT, submit `[claim: hit]`; if MISS, submit `[claim: miss]`.
- Public round summaries list fired coordinates in standard player order (`Echo / Foxtrot / Gamma / Harbor`). Use this to determine exactly what cell my shooter fired at me and what my target fired at their target.

#### Hiding (`[hide: n]`)
- Determine my designated shooter (Echo -> Foxtrot, Foxtrot -> Gamma, Gamma -> Harbor, Harbor -> Echo).
- In Round 1, randomize across the full 1–9 grid (avoid standard focal points like 5, 6, or 7).
- Analyze shooter history from previous rounds:
  - If the shooter's previous shot was a HIT, that shot coordinate was my exact previous hide location. The shooter may repeat it or predict a specific shift.
  - Track the exact cell(s) my shooter fired in recent rounds. If the shooter is spamming a specific cell (e.g., 7), do not hide in that cell or nearby cells.
  - Crucially: do NOT repeat the same hide cell multiple rounds in a row, and do not cycle between a tiny subset of cells (e.g., alternating 2, 3, 4). Always jump to completely unprobed, distant cells across the 1–9 spectrum (e.g., 1, 8, 9, 3, 5).

#### Firing (`[fire: n]`)
- Identify my dedicated target (e.g., Gamma when I am Foxtrot).
- Do not repeat a fired cell if it yielded a MISS in previous rounds unless a full sweep of alternative cells has been completed.
- Systematically sweep unprobed cells across the board (e.g., test 1, 3, 5, 8, 9) rather than repeatedly firing at 5, 6, or 7.
- If a shot lands a HIT, decide whether the target is likely to hold stationary or flee, but if misses occur, immediately switch to an unexplored cell.