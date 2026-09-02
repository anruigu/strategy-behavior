---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1789
---
### Playbook: Quiet Sonar

#### Role & Turn Order
- Determine my assigned shooter and target from the fixed cycle: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
- The public round history displays fire coordinates in fixed player order: `Echo / Foxtrot / Gamma / Harbor`. Look at the exact coordinate fired by my shooter in previous rounds.

#### Hide Stage
- Avoid the shooter's active crosshairs: Look at the shooter's fire coordinates in the most recent rounds. Never hide in a cell they have fired at recently.
- If my shooter scored a HIT on me last round, immediately abandon that cell and move to an unattacked region of the board.
- Avoid repeating the same hiding coordinate across consecutive rounds (e.g., repeatedly hiding in cell 7 or 8), as predictive shooters exploit stationary targets.
- Randomize and distribute hide locations broadly across the grid (1–9), selecting cells distant from where my shooter has targeted.
- Submit `[hide: n]`.

#### Fire Stage
- Track all previous shots fired at my target (Gamma if Foxtrot, Harbor if Gamma, Echo if Harbor, Foxtrot if Echo).
- Avoid re-firing at cells that have already returned a MISS, especially in consecutive rounds. Systematically search unexplored cells.
- Sample diverse areas (edges like 1, 2, 8, 9 as well as center/near-center cells like 3, 5, 7) instead of clumping shots around the same cluster (e.g., repeating 5, 6, 7).
- If I score a HIT, assume the target will relocate next round; shift fire to an adjacent or evasive cell rather than repeating the exact hit cell.
- Submit `[fire: n]`.

#### Claim Stage
- The rules strictly require claims to match the referee's private outcome.
- When the referee informs me of `HIT`, submit `[claim: hit]`.
- When the referee informs me of `MISS`, submit `[claim: miss]`.