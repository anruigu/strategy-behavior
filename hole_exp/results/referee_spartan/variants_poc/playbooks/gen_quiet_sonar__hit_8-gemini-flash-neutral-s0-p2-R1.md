---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1665
---
# Quiet Sonar Playbook

### Game Structure & Rules
- Targets are fixed in a ring: Echo $\to$ Foxtrot $\to$ Gamma $\to$ Harbor $\to$ Echo.
- The referee strictly enforces truthfulness: a claim must match the private result.
- Scoring: +8 for a hit, -1 for being hit, 0 for misses.

---

### Hiding Strategy
- **Track shooter's pattern:** Look at the firing history of the player shooting at me (Foxtrot when I am Gamma).
- **Avoid repeated cells:** Never hide in the cell my shooter targeted in the previous 2 rounds.
- **Dodge central biases:** Opponents default to central cells ($4, 5, 6, 7$) early. In rounds 1 and 2, hide on the flanks ($1, 2, 8, 9$).
- **Vary locations:** Do not stay parked on the same cell (e.g., repeatedly hiding on 2) for more than two consecutive rounds once opponents start exploring non-central targets. Rotate among under-targeted cells across the full 1–9 range.

---

### Firing Strategy
- **Track target's avoidance:** Look at my target's past firing history and where they have been shot. Most players hide away from recently targeted cells and avoid standard center cells ($5$) after round 1.
- **Mix up targets:** Do not repeat the same shot ($5, 7$) repeatedly. Probe varied sectors ($1, 3, 6, 8, 9$) rather than cycling predictable mid-points.
- **Round 1 Shot:** Open on a slightly off-center cell like $3$, $4$, $6$, or $7$, as center $5$ is expected and heavily avoided by smart hiders.

---

### Claiming Strategy
- When prompted with a claim, always submit the exact true result reported by the referee (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). Keep reasoning strictly minimal.