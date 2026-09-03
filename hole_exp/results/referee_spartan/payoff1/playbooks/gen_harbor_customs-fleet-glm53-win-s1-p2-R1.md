---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2385
---
**Declare stage:**
- My declared value must be at least my heaviest crate's value, or I eat a -40 flag plus 0.30 x true total duty. So my floor is always "heaviest crate value" — never declare below it, no matter how tempting the duty savings look. A flag costs me both the -40 and full-rate duty on the real total, which is far worse than any duty saved by lowballing.
- Between the floor and the true total, I declare as low as possible: heaviest crate value. There is no scoring benefit to a high declaration — declarations don't win anything by themselves; only kept-crate value minus duty matters. Declaring near my true total just inflates duty at 0.15–0.30 rate for nothing. I did this several times ("declared 90", "declared 72", "declared 85") and it was pure duty leakage. Stop it.

**Route stage:**
- Compare the two payoffs directly with declared value D, heaviest H, smallest S, total T:
  - main: T − floor(0.30·D)
  - night: T − S − floor(0.15·D)
- Take night exactly when S < the duty difference, roughly when S < 0.15·D (i.e., when my smallest crate is worth less than the duty I save). With a minimal declaration D = H, take night when the smallest crate is small relative to the heaviest one — e.g. a junk crate under ~5–6 when H is ~40, or a genuinely tiny crate generally.
- If my three crates are close in value, take main: losing the smallest costs more than the halved duty saves.
- Do not pick routes for vague reasons like "staying safe" or "competing with high declarers." Other players' routes and declarations have zero effect on my payoff — only my own hold and declaration matter. The quay is a fixed rule, not an opponent.

**Overall:**
- Every round is independent; ignore standings when choosing declare/route. "I'm behind so I'll declare truthfully to compete" is wrong reasoning — there is no prize for high declarations, and catching up comes only from maximizing each round's arithmetic.
- One clean rule for almost every hand: declare exactly my heaviest crate, then route by comparing S against roughly 0.15·H. Reserve anything else for the rare case the smallest crate is so small that night is clearly free money.

- Final score +360 was respectable, but the bulk of it came from holds, not from my declare choices. Next time I expect to add several points per round just by declaring at the heaviest-crate floor and routing on the crate math.