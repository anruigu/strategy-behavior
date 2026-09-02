---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1993
---
# Quiet Sonar Playbook

### Game Structure & Rules
- Ring structure: Echo $\to$ Foxtrot $\to$ Gamma $\to$ Harbor $\to$ Echo. Always know who is shooting at me and who I am shooting at.
- Referee strictly enforces truthfulness: claims must match the private result.
- Scoring: +8 for a hit, -1 for being hit, 0 for misses.

---

### Hiding Strategy
- **Track shooter's pattern:** Explicitly observe the exact cell(s) targeted by my direct shooter (e.g. Foxtrot when I am Gamma) across recent rounds.
- **Avoid shooter habits:** If the shooter is spamming a specific cell (e.g. 3, 7, or 8), completely avoid that cell and adjacent numbers.
- **Dodge central biases:** Opponents frequently shoot central and semi-central cells ($3, 5, 7$). In early rounds, hide on outer flanks ($1, 2, 8, 9$).
- **Vary locations:** Rotate between distant flank cells ($1, 2, 8, 9$) rather than remaining stationary if the opponent switches targets. If hit on a cell (e.g. 8), immediately vacate to the opposite extreme ($1$ or $2$).

---

### Firing Strategy
- **Deduce target's position from shooter hits:** Look at the public claim history. If my target's shooter (or anyone hitting them) lands a hit, the fired cell tells me where my target was located in that round.
- **Avoid spamming missed cells:** If a shot misses, do not blindly repeat it round after round (e.g. firing 3 or 6 four times in a row). Rotate through under-targeted candidate locations.
- **Target opponent hiding habits:** Opponents often hide on outer edges ($2, 8, 9$) or mirror symmetric flank moves to avoid central fire. Probe cells $2, 4, 7, 8$ across rounds rather than fixing on a single guess.
- **Exploit successful hits:** If I hit a target, anticipate whether they will stay or relocate to the opposite flank.

---

### Claiming Strategy
- Always submit the exact true private result reported by the referee (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). Keep reasoning strictly minimal.