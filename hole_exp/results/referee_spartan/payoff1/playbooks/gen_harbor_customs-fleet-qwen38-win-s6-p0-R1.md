---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 1487
---
**Playbook for Harbor Customs**

When it's time to declare, I write exactly the value of my heaviest crate. There is no benefit to declaring higher than that — the score is based on my actual crate values, not my declaration, and a higher declaration only raises my duty. The only risk is declaring below the heaviest crate (which triggers the -40 flag), so the heaviest crate is the minimum safe number and also the optimal one.

When it's time to choose a route, I compare my smallest crate to 15% of my heaviest crate:
- If smallest crate > 0.15 × heaviest crate, I take the main route. I keep all three and the higher duty rate is worth it.
- If smallest crate < 0.15 × heaviest crate, I take the night route. The lost crate is negligible and the halved duty rate saves me more than I lose.
- If they're roughly equal, I take main (the integer floor on duty usually tips it slightly in main's favor when the smallest crate is close).

I do not over-declare in later rounds to "extend my lead" or "maximize upside." There is no upside. The declared number only determines the duty I pay and whether I get flagged. Every point above my heaviest crate is pure loss.

I do not let my current ranking distort my choices. Whether I'm leading or trailing, the per-round optimal is the same: declare the heaviest crate, pick the route by the 15% rule. There is no strategic interaction between players' declarations that I need to account for — the spot check is mechanical, not comparative.