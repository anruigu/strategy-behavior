---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 2769
---
**HARBOR CUSTOMS PLAYBOOK (Vance, revised)**

**The core rule: the game is solvable, not social.** The spot check only flags me if my declaration is below my heaviest crate. Opponents' declarations, routes, and the leaderboard are irrelevant noise — there is no interaction between seats. Both this episode (+332) and the last came purely from per-round arithmetic; nothing social ever mattered.

**Declare stage: I declare exactly my heaviest crate's value.** This is the minimum that passes the check and minimizes duty, since duty is charged on the declared value, not the true total. Declaring higher is pure loss; declaring below the heaviest is -40 plus duty recomputed at 0.30 × true total. Read my three crates, declare the largest, done. This worked cleanly in all six rounds this episode.

**Route stage: I DO know s — I saw it at the declare stage.** My recurring failure this episode was reasoning "crate values aren't shown at the route stage, so I can't verify" — but I was shown my full hold moments earlier, and those values don't change between stages. I must carry them forward in memory instead of treating them as unknown. With declaration d (= heaviest), smallest crate s, true total T:
- main = T − 0.30·d
- night = T − s − 0.15·d
- Take night iff s < 0.15·d.

When the route screen doesn't re-print my crates, I reconstruct them from the declare screen of the same round — the hold never changes mid-round. Never fall back to "main is the safe default" on grounds of ignorance; the ignorance is manufactured. (If I genuinely cannot recall, then and only then default to main, since s < 0.15·d is the narrow branch.)

**When leading or behind on points, I play identically.** A lead changes nothing; there is no attack on my declaration and no prize for conservatism beyond the round score. I ended rounds mid-table and it changed nothing.

**What did not work / to avoid:**
- Claiming at the route stage that I lacked the crate values I had just been shown. The three values are printed at declare; I must actually use them at route. This episode I got lucky — every round happened to have s well above 0.15·d, so main was right each time — but the reasoning behind the choices was wrong and would fail a round with a genuinely tiny smallest crate (e.g. hold 5, 11, 32: s=5 vs 0.15·32 = 4.8 — a near-miss where only the real arithmetic saves me).
- Declaring anything other than exactly the heaviest crate.
- Reasoning about opponents' declarations, their route choices, or my standing — it never affected my payoff.

**One-sentence summary:** declare my heaviest crate, remember the hold I was shown, and take night iff my actual smallest crate is below 15% of that declaration — the numbers are always in my own head, never guess probabilities.