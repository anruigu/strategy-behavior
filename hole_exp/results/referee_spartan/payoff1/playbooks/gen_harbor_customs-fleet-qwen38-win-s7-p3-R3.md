---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 2175
---
**Playbook**

**Declaration.** Declare exactly the value of your heaviest crate. No more, no less. The spot check lifts the heaviest crate and flags any declaration below it, so your heaviest crate is the minimum safe declaration. Every point above it only increases your duty with no benefit. Declaring below it triggers a -40 penalty plus duty recomputed at 0.30 × true total, which is never better than declaring H (since H ≤ T, the flagged score 0.70T − 40 is always less than T − 0.30H).

**Route.** Compare your heaviest crate H to your smallest crate s. The exact condition for night to beat main is: floor(0.30 × H) − floor(0.15 × H) > s. In practice this only happens when H ≥ 37 and s = 5 (giving a gain of 1–2 points). The approximate rule "night wins when H > 6.67 × s" is a reliable screen. When the two routes tie (e.g., H=34, s=5: both yield the same score), default to main. With three crates drawn from 5–40, main is the correct route in the vast majority of rounds.

**Why the window is so narrow.** The duty saving from night is floor(0.30H) − floor(0.15H), which grows slowly (about 5 for H in 34–36, about 6 for H in 37–40). Since the smallest possible crate is 5, you need that saving to exceed s, which only happens at the top of the range with the absolute smallest crate. Don't chase marginal night cases below this threshold.

**Standing and round number do not change the strategy.** There is no catch-up mechanic, no ranking bonus, no endgame twist. Each round is an independent optimization. Whether you are leading by 50 points or trailing by 50, you declare H and run the same route comparison. Do not inflate your declaration to "protect a lead" or deflate it to "take a risk while behind."

**Reading opponents (informational only, does not change my play).** Low declarations from other players (e.g., 9, 16, 17 when typical heaviest crates are 30+) strongly suggest they are getting flagged and eating -40 penalties each time. This confirms the spot check is a real and active threat and that the field is full of players who don't understand the minimum-safe-declaration principle. No action needed beyond continuing to do the right thing.