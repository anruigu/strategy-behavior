---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2436
---
When deciding where to hide, I never pick the same cell twice in a row early on, and I track the full history of fired cells: I hide in a cell that has never been fired at by the player targeting me, or at least the least-targeted region. Repeating my hide cell round after round made me predictable — I should vary even within "safe" zones, using two or three rotation candidates among the cold cells so I don't become the new pattern.

When choosing where to fire, I read the claims and prior fires of others to infer where my target is hiding. If everyone avoids firing a band, my target likely hides there. I change my fire cell most rounds; firing the same cell (like 7) almost every round was wasted — pure repetition gave no information and near-guaranteed misses. I probe systematically: sample untested cells in the target's plausible range rather than fixating.

When my target has been hit recently by someone else, I note that a claimed hit costs them a point, so players cluster near cells they've been fired at — I use the public fire lists to estimate their fear-driven hiding.

When claiming, I claim the true result almost always. A false hit gives +4 and −1 to the target, which is tempting, but the target knows my claim is false and can adapt; more importantly I noticed I flip-flopped between lying and honesty with no plan, which made my claims useless as misdirection anyway. My rule: claim truthfully by default; only lie about a hit when I'm behind late in the game and the point swing matters more than credibility, never early.

When I'm losing, I become more aggressive: fire at the most-predicted cell of the leader's target chain dynamics and consider a false hit claim in the final round where there's no future to protect.

When it's the last round, nothing carries over, so I fire at my single best guess for where the target hides based on their full history, and claim hit regardless of result only if the swing could change my standing — otherwise truth.

When reasoning about claim patterns, I remember others may lie too, so I don't treat public "hit" claims as certain information about hide positions; I weight honest-looking sequences more heavily and treat convenient claims as noise.

Above all, I keep a written mental model each round: for each player, which cells they've hidden in (inferred), which cells they've fired, and I decide my hide and fire against that model instead of by habit.