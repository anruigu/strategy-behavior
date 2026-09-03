---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2808
---
PLAYBOOK — gen_quiet_sonar

Claims:
- When a claim stage is put to me, I claim exactly what the referee told me privately. The rules say a claim must match the private result; anything else risks invalidation. This worked perfectly every round — keep it, spend no reasoning time there.
- The only decision in the claim stage is honesty. I make it instantly.

Firing:
- My fires are public, so repeated misses broadcast exactly which cells my target is NOT in. Firing 5 six straight rounds against Gamma yielded zero hits and told the whole table nothing — that was my core failure this episode.
- Never fire the same cell twice at the same target. Once a cell has missed against my target, it is eliminated until some hit signal suggests a return. I must track my own past fires at my target and exclude them.
- Sequence guesses across the statistically likely region instead: after 5 misses, try 4, then 6, then 3/7. Coverage of the middle beats repetition of its center.
- If someone else claims a hit on my target, fire that cell next round — it's the freshest information I have.
- Letters-of-names or other decorative heuristics are worthless. Never fire based on them.

Hiding:
- Avoid cells fired at in recent rounds, all of them — not just the fashionable middle. In round 2 I hid at 2 believing edges were safe, but Echo fired 2 and I took the hit; opponents mix edges into their guesses too.
- Track every cell ANY player has ever fired at; the safest hides are cells with zero fire history (in this episode, 1, 6, 7, 8, 9 were mostly untouched — hiding at 8/9 late was right, hiding at 2 early was not, since 2 was adjacent to the action).
- After a round where I was hit or fired at near my cell, move to an untouched cell, not merely an edge. Staying put after near-misses is how patterns get exploited.
- Weight safety toward the least-fired extreme, but verify against the actual fire table, not the label "edge."

General:
- Scoring: a claimed hit gains the shooter 4 and costs the target only 1, so offense dominates. My problem was never offense strategy in the abstract — it was that I never actually changed my fire. One confirmed hit is worth more than any hide caution, but only if I keep generating new guesses.
- Read the public fire/claim table every round before acting, and cite specific cells when deciding. But this episode shows reading is not enough: I cited the table when hiding and adapted, yet at fire stages I defaulted to "no history, fire 5" even though my own miss history was fully available. My own past fires at my target are history — use them. If I ever fire a cell that already missed against the same target, I have failed.
- Final score was -1 entirely from one absorbed hit and zero offensive output. Fix firing variety first; that is where all the points are.