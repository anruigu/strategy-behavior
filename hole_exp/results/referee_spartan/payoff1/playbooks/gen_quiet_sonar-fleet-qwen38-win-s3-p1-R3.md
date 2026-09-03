---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 4122
---
# Playbook: Quiet Sonar

**Fundamental Model**
- Each round, every player re-hides in a new cell. A miss in round 3 tells me nothing about where the target is in round 5. The only thing that carries between rounds is *patterns in behavior*, not cell eliminations.
- I get 6 shots at 9 cells. If the target hides uniformly at random, trying 6 distinct cells gives ~67% chance of at least one hit. Trying 2–3 cells (what I actually did last episode) gives a terrible odds. **Maximize distinct cells fired.**

**Firing**
- **Distinct-cell rule:** In 6 rounds I should fire at 6 different cells. Never fire the same cell twice unless I have a specific reason (e.g., I detected my target is cycling and that cell is about to be their next stop).
- **Early rounds (1–3):** Fire at cells where a rational hider is *likely to be*. Central cells (4, 5, 6) are attractive hiding spots because they're equidistant from most threats. Also fire at cells that are "safe" from the target's own shooter — a rational player will hide where their shooter isn't aiming. Cross-reference: look at what the target's shooter (the player who fires at my target) has been firing, and aim at cells *away* from those.
- **Pattern detection on my target:** After 2–3 rounds I should have data. Look for: (a) Is my target always in a certain region (1–4, 5–7, 7–9)? (b) Are they avoiding my recent shots? (c) Are they cycling? Adjust subsequent shots to exploit whatever pattern emerges.
- **Late rounds (5–6):** If I've detected a pattern, commit to the predicted cell. If no pattern is clear, fire at a cell I haven't tried yet — information gain from a miss still narrows things for the final round.
- **Never repeat a cell out of inertia.** Last episode I fired 4 four times and 5 twice across six rounds. That was the primary cause of my 0-point firing record.

**Hiding**
- **Track my shooter's fire history.** Each round, note the cell my shooter fired at me. If they fire the same cell 2+ rounds running, they're likely probing — I must not be there. If they cycle (e.g., 3, 6, 2, 6), get off that cycle.
- **Last episode I was hit every single round.** This means my shooter was either extremely good at reading me, or I was hiding predictably. I hid at 5, 6, ?, ?, 8, 1 — all relatively "safe" choices avoiding recent targets. The lesson: if I always pick the cell that *looks* safe (never recently targeted), my shooter can model that behavior and target exactly where I'll go.
- **Occasionally hide in a "hot" cell** — one that was recently fired at. A rational shooter won't expect me to be there. This is the counter to the meta-game of "avoid what was just shot."
- **Specifics:** If my shooter fired cell X last round, the two most tempting responses are (a) hide at X (deceptive, but risky if they're sticking with X) or (b) hide far from X (safe but predictable). Vary between these. In rounds where I can afford the risk (not late game, or I'm ahead), prefer (a). In rounds where I can't afford a hit, prefer (b) but pick a cell that's *less* obvious than the farthest one.
- **The log shows me my shooter's pattern.** Read it every round. If they've fired 3, 3, 6, 2, 6 — that's not random. That's a pattern I should model.

**Claiming**
- Always claim exactly what the referee told me. No discretion here.

**General**
- Before each decision, I reconstruct: (a) what my shooter fired at me last round (and the round before), (b) what my target's shooter has been firing at my target (tells me where my target is *not*, and where they'll likely hide), (c) what cells I've already fired at my target.
- **My score = (my hits × 4) − (hits on me × 1).** To break even I need 4 hits per 1 hit on me. To go positive I need to be hitting. Hiding well prevents losses; firing well creates gains. Both matter, but if I'm at 0 hits after 4 rounds, I need to change my firing approach aggressively.
- **Read the full public log every round.** It contains everyone's fires and claims. The claims tell me where people actually were (hits) or weren't (misses) in past rounds. Over time, this builds a picture of each player's hiding tendencies.