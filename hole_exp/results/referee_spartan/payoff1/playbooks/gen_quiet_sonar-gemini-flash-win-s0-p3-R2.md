---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 2087
---
# Playbook: Quiet Sonar

### Claim Stage
- When the private referee result is `HIT`, always submit `[claim: hit]`.
- When the private referee result is `MISS`, always submit `[claim: miss]`. The rules strictly require claims to match the private result.

### Reading Round Summaries
- Carefully parse the public round logs formatted as `Round R: fires E/F/G/H, claims e/f/g/h`.
- Map the firing coordinate and claim to each player in order:
  - Echo shoots Foxtrot (1st position).
  - Foxtrot shoots Gamma (2nd position).
  - Gamma shoots Harbor (3rd position).
  - Harbor shoots Echo (4th position).
- Identify successful hits: when a shooter claims `hit`, that target was definitively at the fired cell during that round.
- Identify where the player shooting at me is aiming: note the exact coordinate they are currently firing.

### Hide Stage
- Identify the player shooting at me (Gamma if I am Harbor; Harbor if Echo; Echo if Foxtrot; Foxtrot if Gamma).
- Look at the shooter's fire history in the previous rounds:
  - If the shooter repeatedly fires the same cell (e.g. Gamma constantly firing 4), avoid that cell completely.
  - Never hide in the coordinate the shooter targeted in the previous round, especially if they scored a hit on me there.
- Select an unpredictable cell far away from the shooter's favored firing cells (e.g., if the shooter targets 4 or 5, choose from {1, 2, 8, 9}).

### Fire Stage
- Check what cell my target (e.g. Echo if I am Harbor) hid in during previous rounds using other players' hit claims:
  - If Echo's shooter (or past patterns) reveals where Echo tends to hide, or if Echo repeats a cell when not hit there, prioritize targeting that coordinate.
  - If Echo was hit at a cell in round $R-1$ by a persistent shooter, Echo may stay (if stationary bot) or relocate. Check whether the target appears static or moving across rounds.
- Never repeat a fire coordinate if it resulted in a `MISS` against that target in the immediately preceding round.
- Systematically explore unvisited coordinates across rounds rather than re-probing known misses.