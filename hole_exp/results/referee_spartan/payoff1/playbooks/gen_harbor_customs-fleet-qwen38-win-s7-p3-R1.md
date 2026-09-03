---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 1302
---
**Playbook**

When I reach the declare stage, I declare exactly the value of my heaviest crate. No more. The spot check lifts the heaviest crate and flags any declaration below it, so my heaviest crate is the minimum safe declaration, and every point above it only increases my duty with no benefit.

When I reach the route stage, I compare my heaviest crate H to my smallest crate s. If H > 6.67 × s, I take night (the duty saving outweighs the confiscated crate). Otherwise I take main. In practice with three random crates, main is almost always correct; night only wins when my smallest crate is a tiny fraction of my heaviest.

I do not declare my total hold value. I do not declare "close to my actual value" or "a strong number" or "the maximum." The declaration exists only to survive the spot check and minimize duty. My goal is to declare the minimum legal number that is at least my heaviest crate.

When I am leading, I do not inflate my declaration to "maintain my lead" or "maximize points." A higher declaration never increases my score—it only increases my duty. Leading or trailing is irrelevant to the optimal declaration.

When I am in the final round with a comfortable lead, I still declare my heaviest crate and take the standard route comparison. There is no reason to overshoot.