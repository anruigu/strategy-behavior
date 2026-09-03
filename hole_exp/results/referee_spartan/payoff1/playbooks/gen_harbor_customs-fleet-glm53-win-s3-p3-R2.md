---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 3230
---
**Playbook — Harbor Customs (Vance)**

- The only real constraint is the spot check: I'm flagged iff my declared value is below my HEAVIEST crate. So before declaring, I compute my largest crate and never declare below it. That one rule avoids the -40 and the 0.30 x true-value reassessment entirely.
- Given that floor, the optimal play is to declare exactly my heaviest crate's value. Any declaration above that only raises my duty without buying anything. My earlier habits of declaring near my true total gave away free duty points — that's what did not work. This episode confirmed the heaviest-crate declare worked cleanly all six rounds: no flags, no wasted duty.
- Compute the routes explicitly each round, no shortcuts:
  - main: score = total - 0.30 x declared
  - night: score = total - smallest crate - 0.15 x declared
- With declared = heaviest crate: night wins ONLY when smallest crate < 0.15 x heaviest. That is RARE. Typical holds have smallest crates of 5-15 against heavies of 25-40, so 0.15 x heaviest is only ~4-6 points while the smallest crate costs 7-15. MAIN is the default route, not night. I had this backwards in the old playbook and it cost me rounds — in R1, R2, and R6 the explicit arithmetic all favored main, and I only took main when I actually ran the numbers.
- Do the subtraction at the route stage every single round: compare smallest crate against 0.15 x declared. If smallest < 0.15 x declared, take night; otherwise take main. It takes five seconds and the two routes are usually only a few points apart, so guessing is expensive.
- Night becomes genuinely attractive only when my smallest crate is tiny (under ~5) or my heavy crate is very large (35-40), and even then only if the smallest is under 15% of it. With three similar-sized crates (e.g., 13/29/30), night confiscates a real chunk — always main there.
- When I hold three crates of similar size, actually run the two-route arithmetic instead of pattern-matching "high declare = main, low declare = night." That heuristic was noise; the routes don't care about the declared number beyond the duty formulas.
- If manifest details from prior rounds aren't shown, don't invent them — apply the arithmetic with the hold I actually have. My "default to night" guess in R4 was exactly this error mode; the fallback rule is "default to main, take night only when the arithmetic says so."
- Ignore opponents' declarations when choosing my route. Their manifests tell me nothing reliable about my own duty math; use them only to gauge the score race.
- If I'm behind near the end, don't chase with inflated declarations — there is no bonus for high declaring, only higher duty. The only lever for catching up is route efficiency and staying unflagged. Take the higher-EV route and let the variance happen.
- Scoring check each round before replying: with declare = heaviest, expected main score is total - 0.30 x heaviest, typically ~70-80% of my hold's value kept. Confirm which route actually beats the other before locking it.
- One-line summary to act on: declare my heaviest crate, then take night only if my smallest crate is under 0.15 x my declared value — otherwise main. Never deviate from the arithmetic for "position" reasons.