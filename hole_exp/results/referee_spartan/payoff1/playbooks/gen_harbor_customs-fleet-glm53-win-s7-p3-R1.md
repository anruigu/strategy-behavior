---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 2004
---
# Playbook: Harbor Customs (Vance)

## Core mechanic (the only rule that matters)
- The spot check compares my declared value against my **heaviest single crate**. So my declaration only needs to be ≥ my largest crate to be safe. Anything declared above the largest crate buys zero additional safety, only extra duty.
- When declaring, I always set the number equal to my heaviest crate. That is the minimum safe declaration and the minimum duty. Do not declare the true total, and do not declare a "plausible mid-range" number — round 2's declare of 37 with a 39-crate aboard was pure luck not to be flagged; a 39 was in my hold and I was under it.

## Route choice
- Compute both payoffs explicitly each round:
  - main: (total) − floor(0.30 × declared)
  - night: (total − smallest crate) − floor(0.15 × declared)
- Since I declare = heaviest crate, night's saving is roughly half the heaviest crate minus the smallest crate. Night wins when smallest crate < ~0.15 × heaviest. Otherwise main wins.
- Stop choosing night "for variance" or "to protect a lead" — those were vibes, not math. The route decision is arithmetic; do the arithmetic every time.

## Penalties
- Being flagged costs −40 plus recomputed duty at 0.30 of the true total. That's catastrophic. Never declare below the heaviest crate. There is no reason ever to take that risk since declaring exactly the heaviest crate is both safe and duty-minimal.

## Opponent behavior / final standing
- This appears scored on my own points, not relative rank — my final +254 came from consistent per-round payoffs. So I ignore leaderboards and just maximize expected score each round. Don't "protect a lead" with conservative or aggressive plays; protect it by playing the same optimal line every round.

## Summary of the standing line
- Declare stage: I write down my heaviest crate's value, exactly.
- Route stage: I compute both payoffs and pick the larger. Default to main unless the smallest crate is clearly small relative to the heaviest.