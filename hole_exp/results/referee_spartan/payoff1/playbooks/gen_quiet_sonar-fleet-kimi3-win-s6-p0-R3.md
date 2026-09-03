---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 2829
---
When the claim stage is put to me, I claim the true result every time — the rules require claims to match the private result, so there is no real decision here; I answer the truth immediately with no deliberation.

When hiding, I count which cells have been fired publicly so far and hide in a cell from the least-fired region, preferring cold non-edge cells. I rotate among the cold cells rather than repeating one exact number every round — repeating the same hide makes me predictable. This worked: across a full game of cold-cell rotation I was never hit once. Hiding well is worth a lot — every hit on me costs a point and hands the shooter four.

My #1 historical failure: firing the same cell for nearly a whole game and never hitting. Hard rule: I never fire the same cell more than twice in a row against the same target without a hit. After two misses at a cell, that cell is dead — I switch to a different region entirely, not an adjacent cell in the same cluster.

Persistence pays only after a hit. The moment I score a hit, I fire the same cell next round — a hit is evidence of a target's habit, unlike a miss. But I cap it: if the refire after a hit misses twice, the habit has broken and I shift to cells adjacent to the hit cell, then resume sampling. In my episode I hit once, refired correctly, but then kept grinding the same cell after two post-hit misses in the final round instead of stepping adjacent — that cost me a chance at a second hit.

I study my specific target's exposure, not just the aggregate fire map: which cells did the player who shoots at my target hit on? Those reveal my target's hide habits, and my target likely still favors them or nearby cells. I fire into my target's demonstrated habits rather than picking "unglamorous" cells at random — random picks against a clean sheet win nothing.

When no one has yet been hit on my target, I sample across the plausible range systematically (sweep low, then mid, then high, never repeating a missed cell) — each miss eliminates a region. Sweeping broadly is what eventually produced my first hit, so the approach works; I just must convert hits into streaks.

When behind late in the game, I do not play it safe by re-firing familiar cells; I aim where the table's hit history shows players actually hide — the spot that produced repeated hits for the leader — since matching a hidden cell is the only way to score. But I never fire a cell I have already personally missed twice, no matter how hot it looks.

I track the score each round: if I am being outscored by someone farming a predictable target, my priority is finding my own repeatable hit, not defense — I cannot affect who hits others, only where I shoot and hide.

I keep my reasoning notes short and only about hide/fire choices; I never waste deliberation on the claim step.