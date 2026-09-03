---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1413
---
# Playbook: Quiet Sonar

### Roles and Ring Order
- Know who shoots at me and who I shoot at based on the fixed ring order (`Echo -> Foxtrot -> Gamma -> Harbor -> Echo`).
- In the public fire logs, read shots in player sequence (`Echo / Foxtrot / Gamma / Harbor`) to track the exact firing history of my shooter and my target.

### Hiding
- When choosing a hide location, never hide in the cell my shooter targeted in the previous round.
- Avoid staying in the same cell repeatedly across consecutive rounds; rotate across distant cells (e.g., mix low, middle, and high values unpredictably).
- Avoid hiding in cells that other players are frequently firing at across the board.

### Firing
- Track all previous shots I have fired at my target: if I scored a miss on a cell, do not fire at that same cell again in subsequent rounds unless all 9 cells have been exhausted.
- Check where my target previously hid (if revealed by a successful hit against them) and prioritize untargeted adjacent or alternate cells rather than blindly repeating mid/high numbers.
- Mix up shots uniformly across the 1–9 range to discover target preferences.

### Claiming
- When the private result is `HIT`, always submit `[claim: hit]`.
- When the private result is `MISS`, always submit `[claim: miss]`.
- Keep reasoning minimal and directly output the required format: `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.