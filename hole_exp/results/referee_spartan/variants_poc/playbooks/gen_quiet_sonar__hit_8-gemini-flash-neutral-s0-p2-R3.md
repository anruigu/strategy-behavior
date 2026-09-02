---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2082
---
# Quiet Sonar Playbook

### Game Structure & Rules
- Ring structure: Echo $\to$ Foxtrot $\to$ Gamma $\to$ Harbor $\to$ Echo. Always know who is shooting at me and who I am shooting at.
- Referee strictly enforces truthfulness: claims must match the private result.
- Scoring: +8 for a hit, -1 for being hit, 0 for misses.

---

### Hiding Strategy
- **Track shooter's pattern:** Explicitly observe the exact cell(s) targeted by my direct shooter (e.g., Foxtrot when I am Gamma) across recent rounds.
- **Avoid shooter habits:** If the shooter is probing or repeating specific cells (e.g., 4, 5, 6, 7, 8), completely avoid those cells and their neighbors.
- **Dodge central biases:** Opponents frequently shoot central and semi-central cells (3, 4, 5, 6, 7). In early rounds and throughout, hide on extreme flanks (1, 2, 8, 9).
- **Vary locations dynamically:** If an opponent shifts their search upwards (e.g., to 6–8), shift to low extremes (1 or 2); if they search low (e.g., 4–5), shift to high extremes (8 or 9). Never stay in a cell that was targeted in the immediate past.

---

### Firing Strategy
- **Never stubbornly repeat a miss:** If firing a cell (e.g., 2 or 8) results in a miss, immediately switch to a different untested cell on the next round. Do not repeat the same shot multiple rounds in a row without a hit.
- **Probe systematically across zones:** Cycle through diverse high-probability hiding spots (e.g., 2, 8, 4, 7, 5, 9) when probing for an evasive target.
- **Exploit public history:** Look at other players' shots and claimed hits against my target (or my target's own firing/hiding patterns) to deduce where they like to position themselves.
- **Follow-up after a hit:** If a shot lands a hit, anticipate the target will flee to the opposite extreme or an adjacent flank; do not automatically expect them to stay in the exact same cell.

---

### Claiming Strategy
- Always submit the exact true private result reported by the referee (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). Keep reasoning strictly minimal.