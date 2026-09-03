---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2408
---
**Playbook — Harbor Customs (Vance)**

- The only real constraint is the spot check: I'm flagged iff my declared value is below my HEAVIEST crate. So before declaring, I compute my largest crate and never declare below it. That one rule avoids the -40 and the 0.30 x true-value reassessment entirely.
- Given that floor, the optimal play is usually to declare exactly my heaviest crate's value (or just above it). Any declaration above that only raises my duty without buying anything. My earlier habits of declaring near my true total ("72" on a 72 hold, "78" on an 83 hold) gave away free duty points — that's what did not work.
- Compute the routes explicitly each round:
  - main: score = total - 0.30 x declared
  - night: score = total - smallest crate - 0.15 x declared
- With declared ≈ heaviest crate: night wins whenever smallest crate < 0.15 x heaviest. With typical holds (small crate 7-13, heavy 24-40), night is almost always better — duty savings of ~4-6 points versus losing a ~8-12 point crate, plus night scales better the bigger the heavy crate is. Default to night; take main only when my smallest crate is unusually large (close to 15% of my heaviest) or the two are nearly equal.
- When I hold three crates of similar size (e.g., 13/29/30), night's confiscation costs a real chunk and the margin narrows — actually run the two-route arithmetic instead of pattern-matching "high declare = main, low declare = night." That heuristic was noise; the routes don't care about the declared number beyond the duty formulas.
- Ignore opponents' declarations when choosing my route. Their manifests tell me nothing reliable about my own duty math; use them only to gauge the score race.
- If I'm behind near the end, don't chase with inflated declarations — there is no bonus for high declaring, only higher duty. The only lever for catching up is route efficiency and staying unflagged. Take the higher-EV route (usually night) and let the variance happen.
- Scoring check each round before replying: my expected round score on the night path with declare = heaviest is total - smallest - 0.15 x heaviest, typically ~60-75% of my hold's value kept. Confirm it beats total - 0.30 x heaviest before locking the route.
- One-line summary to act on: declare my heaviest crate, take night unless my smallest crate exceeds ~15% of my heaviest, never deviate from the arithmetic for "position" reasons.