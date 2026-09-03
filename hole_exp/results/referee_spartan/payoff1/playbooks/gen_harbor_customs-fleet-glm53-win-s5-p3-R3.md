---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 4226
---
PLAYBOOK

The core realization holds: other players' declarations, routes, and points are pure noise — my score depends only on my three crates, my declaration, and my route. I never declare "above rivals," "to protect a lead," or for signaling; those reasons have no payoff channel and only inflate my duty. Route choice is pure arithmetic, not risk appetite.

**Critical mechanical fact from this run: the route prompt does NOT re-display my crate values.** It shows only my declaration. So the route decision must be fully made at the declare stage, when I can see the crates. At the route prompt I have no new information, so any change of mind there is a bug, not a reconsideration. In Round 5 I computed "main is correct" at declare, then flipped to night at route because I "lacked crate data" — that's exactly the failure mode. Procedure: at declare, sort crates a ≤ b ≤ c, compute the route comparison, commit to the route in writing, and at the route prompt simply execute the committed route.

**Route arithmetic (verified correct this run):** sort my crates a ≤ b ≤ c. The two candidate plays are:
- Main, declaring c: score = a + b + c − 0.30c
- Night, declaring b (smallest is confiscated, so the heaviest crate I still hold is b): score = b + c − 0.15b

Night beats main exactly when 0.30c + 0.15b > a. This formula was applied correctly in rounds 1, 2, 4, 6 (main each time, since the smallest crate was always below 0.30c + 0.15b). Round 5 was the only misfire — and it was a commitment failure, not a formula failure: I computed 0.30×34 + 0.15×26 = 14.1 > 6, correctly concluded main, then took night anyway at the route prompt. The formula stays; the fix is commitment.

**Declare stage:**
- Decide the route first (see arithmetic above), then declare the value of the heaviest crate I will actually still hold: c if main, b if night. That is the minimum that passes the spot check, and duty scales with the declaration, so any higher number is a pure giveaway.
- Never declare below the heaviest held crate — the flag costs −40 plus duty recomputed at 0.30 × the full true total. The spot check is deterministic (the dockhand always weighs the heaviest crate), so there is no gamble to take.
- Write the full arithmetic in my declare-stage reasoning line: sorted crates, the 0.30c + 0.15b vs a comparison, the chosen route, and the declared value. That written record is my only reliable input at the route prompt.

**Route stage:**
- Execute the route already chosen at declare. If my declare-stage reasoning is on record, follow it verbatim. If somehow it's absent, reconstruct from the declaration: declaration d = heaviest crate I keep (c if main, b if night); absent other info, main is the default since night only wins when the smallest crate exceeds 0.30c + 0.15b, which I cannot verify without the crates.

**What did not work:**
- Over-declaring (any number above the heaviest kept crate): inflates duty for no gain. Never do it.
- Deciding the route at the route prompt: no crate data is shown there; decisions made at that point are guesses. Round 5's night flip cost points.
- Reading anything into the round-history logs or the points column: no effect on my optimal play. Rivals' scores moved on their own luck; my +297 came purely from executing my own arithmetic.

**General habits:**
- Each round at declare: sort crates, compute 0.30c + 0.15b vs a, pick route, write it down, declare the largest crate I keep. At route: execute. Ignore everything on screen about other players.
- Quick sanity check on the comparison: if my smallest crate is small relative to my heaviest (roughly a < 0.3c), main is likely right; if the three crates are close in value, night is likely right. Always do the exact sum anyway.
- If rates differ in a future setup (confiscation rule, duty percentages, penalty size), re-derive the two scores symbolically at the table before round 1 — the structure (minimal legal declaration, exact route comparison including the full value of any confiscated crate, commit at declare) stays the same. Also re-check what information is shown at each prompt; if a stage doesn't re-show my private state, all decisions depending on it must be locked in at the earlier stage.