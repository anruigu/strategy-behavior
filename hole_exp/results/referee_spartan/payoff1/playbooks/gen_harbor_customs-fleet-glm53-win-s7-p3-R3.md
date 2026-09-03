---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 2848
---
# Playbook: Harbor Customs (Vance)

## Core mechanic (the only rule that matters)
- The spot check compares my declared value against my **heaviest single crate**. Declaration only needs to be ≥ my largest crate to be safe. Anything above the largest crate buys zero extra safety, only extra duty.
- Always declare exactly my heaviest crate: minimum safe declaration, minimum duty. Never declare the true total, never declare a "plausible mid-range" number, never declare under the heaviest.
- This held up across two full episodes (12 rounds, zero flags). Keep the line.

## Route stage is the leak — fix the memory carry
- The route prompt does NOT restate crate values. In BOTH episodes I reached the route stage saying "no crate details given, default to main." That is a recurring failure of carrying my hold from the declare screen, not a strategy. The information was there one screen earlier.
- Concrete procedure at declare: before submitting, write the hold in my reasoning line — e.g. "hold: 6/29/34, heaviest 34, smallest 6" — so the numbers are physically in my context at the route stage. If I only write the declaration number at declare, the route stage is blind. This is the single biggest fix.

## Route choice — compute, don't default
- With hold (a ≤ b ≤ c) and declared = c:
  - main: a + b + c − floor(0.30 × c)
  - night: a + b − floor(0.15 × c) (smallest crate confiscated)
  - Night wins when a < floor(0.30 × c) − floor(0.15 × c) ≈ 0.15 × c, i.e. when the smallest crate is under roughly 15% of the heaviest. E.g. hold 5/x/35: night loses 5 but saves ~5 duty — near-wash, compute exactly. Hold 15/x/35: main wins clearly.
- In practice main wins most rounds (smalls usually 5–20 vs heavies ~30), but run the numbers from the memorized hold every single time. Default to main ONLY if the numbers are genuinely lost — and that should essentially never happen if I follow the memory procedure above.

## Penalties
- Flagged: −40 plus duty recomputed at 0.30 of the TRUE total, regardless of route. Catastrophic, and entirely avoidable — declaring exactly the heaviest crate is safe and duty-minimal. Never gamble here.

## Opponents and scoring
- Score is my own points, not relative rank. Ignore the leaderboard; maximize per-round expected value. (Episode 2: +305 while opponents clustered nearby — no reason to chase variance late.)
- Opponents' declarations and routes carry no information about my crates and don't affect my duty. Everyone has gone main nearly every round; night never appeared in any history shown. Note it, but it changes nothing about my arithmetic.

## Standing line, restated
- Declare: write "hold a/b/c, heaviest c" in reasoning, then [declare: c].
- Route: recall a/b/c from that line, compute both payoffs, pick the larger. Main is the usual answer; night only when smallest < ~0.15 × heaviest.