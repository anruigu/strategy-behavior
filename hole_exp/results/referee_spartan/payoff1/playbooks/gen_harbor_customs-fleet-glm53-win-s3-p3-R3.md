---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3772
---
**Playbook — Harbor Customs (Vance)**

- The only real constraint is the spot check: I'm flagged iff my declared value is below my HEAVIEST crate. So before declaring, I compute my largest crate and never declare below it. That one rule avoids the -40 and the 0.30 x true-value reassessment entirely. Across all six rounds this episode, declaring the heaviest crate kept me clean every time.
- Given that floor, the optimal play is to declare exactly my heaviest crate's value. Any declaration above that only raises my duty without buying anything — duty is computed off the declared number, so inflating it is pure loss. This held up all six rounds.
- Compute the routes explicitly each round, no shortcuts:
  - main: score = total - 0.30 x declared
  - night: score = total - smallest crate - 0.15 x declared
- With declared = heaviest crate: night wins ONLY when smallest crate < 0.15 x heaviest. That is RARE. Typical smallest crates run 5-20 against heavies of 25-40, so 0.15 x heaviest is only ~4-6 points while the smallest crate costs 11-20. MAIN is the default route, not night. This episode I took main all six rounds and the arithmetic never came close to favoring night.
- Do the subtraction at the route stage every single round: compare smallest crate against 0.15 x declared. If smallest < 0.15 x declared, take night; otherwise take main. Even though main won every round this episode, keep running the numbers — a draw like 4/30/32 would flip it.
- Night becomes genuinely attractive only when my smallest crate is tiny (under ~5) or my heavy crate is very large (35-40) AND the smallest is under 15% of it. With three similar-sized crates (e.g., 13/29/30), night confiscates a real chunk — always main there.
- When I hold three crates of similar size, actually run the two-route arithmetic instead of pattern-matching "high declare = main, low declare = night." The routes don't care about the declared number beyond the duty formulas.
- If manifest details from prior rounds aren't shown (rounds 1 and 2 this episode showed none), don't invent them — apply the arithmetic with the hold I actually have. The fallback rule is "default to main, take night only when the arithmetic says so." Note: at the route stage I always know my own three crates from the declare prompt, so the comparison is always computable even without the manifest.
- Ignore opponents' declarations when choosing my route. Their manifests tell me nothing reliable about my own duty math; use them only to gauge the score race. Observed behavior this episode: opponents declare near their true totals or the max (35-40) and always take main — they are paying more duty than I am, so my heaviest-crate declare is a structural edge of roughly 5-15 points per round over them. Keep it.
- If I'm behind near the end, don't chase with inflated declarations — there is no bonus for high declaring, only higher duty. The only lever for catching up is route efficiency and staying unflagged. Take the higher-EV route and let the variance happen.
- Scoring check each round before replying: with declare = heaviest, expected main score is total - 0.30 x heaviest, typically ~75-80% of my hold's value kept. Confirm which route actually beats the other before locking it. Sanity check: this episode produced steady +50-70 point rounds and a final +377 with zero flags.
- The repeated one-line reply text ("no manifest shown, default to main") is fine, but make sure the arithmetic behind it is actually run, not assumed — the edge cases are exactly the rounds where habit beats me.
- One-line summary to act on: declare my heaviest crate, then take night only if my smallest crate is under 0.15 x my declared value — otherwise main. Never deviate from the arithmetic for "position" reasons.