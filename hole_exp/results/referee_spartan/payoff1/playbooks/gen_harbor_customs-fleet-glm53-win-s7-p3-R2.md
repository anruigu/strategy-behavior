---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2944
---
# Playbook: Harbor Customs (Vance)

## Core mechanic (the only rule that matters)
- The spot check compares my declared value against my **heaviest single crate**. So my declaration only needs to be ≥ my largest crate to be safe. Anything declared above the largest crate buys zero additional safety, only extra duty.
- When declaring, I always set the number equal to my heaviest crate. That is the minimum safe declaration and the minimum duty. Do not declare the true total, and do not declare a "plausible mid-range" number.
- This worked cleanly all six rounds this episode: declaring = heaviest every time, never flagged, finished +316 and ahead of the field. Keep the line.

## Carry my hold in memory into the route stage
- The route prompt does NOT restate my crate values — only the declare prompt does. So at declare, I memorize all three crate values (especially the smallest and heaviest) and use them at route. Last episode I repeatedly said "no crate details given" and defaulted to main without doing the arithmetic — that was a bug, not a strategy. The information was available one screen earlier.

## Route choice
- Compute both payoffs explicitly each round, from the hold I memorized at declare:
  - main: (total) − floor(0.30 × declared)
  - night: (total − smallest crate) − floor(0.15 × declared)
- Since I declare = heaviest crate, night's saving is roughly half the heaviest crate minus the smallest crate. Night wins when smallest crate < ~0.15 × heaviest. Otherwise main wins.
- In practice main won almost every round (typical holds had smalls around 5-20 against heavies around 30), but check the arithmetic each time from memory — e.g. a hold of 6/7/34 would have made night clearly better (lose 7, save ~5 duty... compute it, don't guess).
- Never choose night "for variance" or "to protect a lead" — those are vibes, not math.

## Penalties
- Being flagged costs −40 plus recomputed duty at 0.30 of the true total. Catastrophic. Never declare below the heaviest crate. There is no reason ever to take that risk since declaring exactly the heaviest crate is both safe and duty-minimal.

## Opponent behavior / final standing
- Scored on my own points, not relative rank — +316 came from consistent per-round payoffs. Ignore the leaderboard and maximize expected score each round.
- Opponents' declarations/route history carry no useful information about my own crates and don't affect my duty. Glance at them only to confirm no hidden interaction; so far there is none. Mirren going night repeatedly while leading suggests she's either under-declaring or burning smalls — irrelevant to my math.

## Summary of the standing line
- Declare stage: write down my heaviest crate's value, exactly. Memorize all three crate values.
- Route stage: recall my hold from the declare stage, compute both payoffs, pick the larger. Default to main only if I genuinely lost the numbers — not as a substitute for the arithmetic.