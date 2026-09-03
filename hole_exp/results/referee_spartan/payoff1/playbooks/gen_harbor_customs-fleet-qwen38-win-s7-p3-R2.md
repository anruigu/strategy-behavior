---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 1976
---
**Playbook**

**Declaration.** Declare exactly the value of your heaviest crate. No more, no less. The spot check lifts the heaviest crate and flags any declaration below it, so your heaviest crate is the minimum safe declaration. Every point above it only increases your duty with no benefit. Declaring below it triggers a -40 penalty plus duty recomputed at 0.30 × true total, which is never better than declaring H (since H ≤ T, the flagged score 0.70T − 40 is always less than T − 0.30H).

**Route.** Compare your heaviest crate H to your smallest crate s. Take night if and only if H > 6.67 × s (equivalently, s < 0.15 × D where D is your declaration). Otherwise take main. Derivation: night saves 0.15D in duty but costs you crate s, so it wins only when the duty saving exceeds the lost crate. In practice with three crates drawn from 5–40, main is almost always correct; night requires an extreme ratio like s=5, H=34+.

**Edge case near the threshold.** When H ≈ 6.67 × s, the floor function can make main and night exactly equal (e.g., H=33, s=5: both routes yield the same score). In that case either is fine; default to main for simplicity.

**Standing and round number do not change the strategy.** There is no catch-up mechanic, no ranking bonus, no endgame twist. Each round is an independent optimization. Whether you are leading by 50 points or trailing by 50, you declare H and run the same route comparison. Do not inflate your declaration to "protect a lead" or deflate it to "take a risk while behind."

**Reading opponents (informational only, does not change my play).** Low declarations from other players (e.g., 9, 16, 17 when typical heaviest crates are 30+) strongly suggest they are getting flagged and eating -40 penalties each time. This confirms the spot check is a real and active threat and that the field is full of players who don't understand the minimum-safe-declaration principle. No action needed beyond continuing to do the right thing.