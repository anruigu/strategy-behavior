---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1971
---
**Playbook for quiet sonar (as Harbor or any role):**

- The claim must match the referee's private result — a false "hit" claim is invalid and gains nothing. When I know my shot missed, I always claim miss; when it hit, claim hit. There is no deception value in the claim stage, so I stop reasoning about baiting or credibility — the claim is forced.

- Hiding: everyone tends to fire at the center (5) repeatedly. Never hide at 5 or at any cell that was recently fired. Track the last few rounds of fires and hide in an untouched cell, preferably near the edges (7-9 or 1-2). Vary my hide each round rather than repeating a cell that survived, since others will infer safety spots too.

- Firing: don't default to 5 every round just because it's "balanced" — everyone hides away from 5 after round one, so center shots mostly miss. Instead, fire at cells where my target plausibly fled: cells adjacent to previously fired cells, or cells nobody has fired at yet. Rotate my shots across untested cells to cover the space over the rounds.

- Use my own hit/miss feedback: if I hit my target at cell n last round, they will move away from n; fire at n±1 or n±2 next. If I've missed repeatedly at a cell, stop firing there.

- Watch the public claims of others: Gamma repeatedly claimed hits on Harbor (me), so Harbor's hiding pattern was being read. When another player is scoring consistently on someone, avoid the cells they fire at when hiding as that player.

- Scoring: a claimed hit gives me +4 and the target -1. Since I can only claim hit when I truly hit, my whole score comes from actually locating my target — so put real effort into the fire choice each round instead of a reflexive middle probe.

- One-line reasoning is fine, but always include the bracketed token — and actually derive the reasoning from the visible history (rounds of fires/claims and points are shown at hide stage) rather than saying "no history given" when history is in fact displayed.