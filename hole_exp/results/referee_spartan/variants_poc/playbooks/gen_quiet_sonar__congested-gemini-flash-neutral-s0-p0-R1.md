---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1644
---
# Playbook: Quiet Sonar (Congested)

### Rules & Claim Verification
- A claim must strictly match the referee's private outcome. When the referee reports `MISS`, always submit `[claim: miss]`. When the referee reports `HIT`, always submit `[claim: hit]`. Do not attempt to bluff or fake a hit, as the referee requires claims to match the private result.

### Defense (Hiding)
- Identify the shooter targeting me (the player directly upstream in the firing ring, e.g., Harbor if I am Echo).
- Track the recent firing coordinates of my direct attacker. 
- Avoid the central cluster (cells 4, 5, 6, 7) unless my attacker has shown a persistent habit of firing exclusively at the edges.
- Choose hide locations in the unsearched or neglected zones—typically cells 1, 2, 8, or 9—and rotate among these safe cells rather than staying stationary in a cell the shooter has begun probing.

### Offense (Firing)
- Track my target's past behavior and recent hits.
- If my target was just hit at cell $k$, avoid firing at $k$ the immediately following round, as targets almost always relocate after a hit.
- Do not repeatedly hammer the middle focal points (cells 5, 6, 7) round after round if the target is consistently dodging them. 
- Systematically sample across the line (e.g., test lower cells 2–3, center-left 4, center-right 6, and upper cells 7–8) rather than repeating unsuccessful fire coordinates against the same opponent.
- Pay attention to the firing history of my target when they hide: opponents often hide in zones where they themselves do not fire. Use their own firing preferences as negative indicators for their likely hide locations.