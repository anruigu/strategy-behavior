---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 3667
---
When asked to hide, pick a cell that has been targeted least often in recent rounds (prefer cells with few or no recent fires).

When asked to hide early in the match, randomize among a small set (center + two off-center) rather than always the same cell.

When historical firing shows clustering on a few cells, avoid those clustered cells for my hide.

When opponents' claims and public fires imply some cells are popular for claimed hits, treat those cells as riskier to hide in (they either are real targets or deliberate decoys).

When my assigned target is fixed, vary my fire choices instead of repeating the same coordinate after misses; do not persistently fire the same cell after repeated misses.

When choosing a fire coordinate against my target, mix between:
- cells that have been targeted at the target the most (if I infer they tend to hide where others search),
- and low-frequency cells (to exploit predictable patterns),
using a randomized schedule so my shots are not trivially predictable.

When my target has high score and I need points, bias my fire selection slightly toward the most-likely inferred hide (based on others' shot/claim history) while still randomizing some fraction of the time.

When I am privately told the true result of my shot, always submit the claim that matches the private result (truthful claim) — the rules require exact matching, so do not attempt dishonesty.

When validating a choice, ensure all hides and fires are integers 1–9 and claims are exactly "hit" or "miss".

When I see opponents repeatedly claim hits on the same coordinates, treat those coordinates as suspect (either actually strong choices or signals to avoid when hiding).

When the game is short (few rounds left) and I need to change my standing quickly, concentrate fires to a small set of inferred likely cells rather than wide randomization, but if that concentrated plan yields repeated misses, switch to exploiting low-frequency cells.

If repeated strategy (e.g., always firing the same cell) produced no hits in prior play, stop that repetitive choice and shift to a mixed strategy that balances most-likely and under-targeted cells.

Track per-player fire histories and per-cell frequencies separately: record who fires where and who claims hit/miss to better infer each player's hiding bias.

Favor hiding on cells that have been targeted little by the specific players who tend to hit or be truthful, and avoid cells targeted often by players who claim hits (since those cells are likely real or strategically signaled).

Do not assume claims are lies — claims must match private result; instead infer opponents' hiding tendencies from where they and others actually fire and the distribution of confirmed hits.

If I fall behind in score, increase my willingness to concentrate fires on inferred likely cells for a few rounds (accepting variance) while still mixing occasionally to avoid being predictable.

Periodically reassess the small set I randomize among for hides (center + two off-center) using updated recent-fire frequencies; rotate which off-center cells I include to avoid exploitability.

When opponents' patterns show clear clustering on a small set of cells, bias my fires slightly toward those cells (to take advantage of higher hit probability) but avoid committing to a single cell after a sequence of misses.

Keep all decision rules actionable and bounded: choose deterministic frequency thresholds (e.g., avoid cells with ≥2 recent fires in last 3 rounds unless I need to gamble) and a baseline randomization rate (at least 25% of actions randomized among my chosen small set) so behavior remains unpredictable.