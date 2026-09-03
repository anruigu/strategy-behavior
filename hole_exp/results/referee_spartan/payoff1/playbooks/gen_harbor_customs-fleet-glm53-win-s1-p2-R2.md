---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2895
---
**Declare stage:**
- My declared value must be at least my heaviest crate's value, or I eat a -40 flag plus 0.30 x true total duty. The floor is always "heaviest crate value" — never declare below it. This episode I declared exactly the heaviest crate all six rounds and was never flagged; the rule held up perfectly. Keep doing it.
- Between the floor and the true total, declare as low as possible: heaviest crate value. There is no scoring benefit to a high declaration — only kept-crate value minus duty matters. Declaring near my true total just inflates duty at 0.15–0.30 rate for nothing.
- One caveat learned this run: with a minimal declaration D = H, the whole payoff hinges on the flag being literal. Declare exactly H, not H minus 1 — the spot check weighs the heaviest crate, so there is no slack.

**Route stage:**
- The route prompt does NOT show my crate values — only the declare prompt does. So I must decide the route at declare stage, while I can still see the hold, and just execute it at the route stage. Twice this run I waffled at the route stage ("no crate details given, default to main") and let vagueness override the math I had already done. Stop that: when the route screen shows no crates, recall the hold from the declare screen and follow the arithmetic.
- Compare the two payoffs directly with declared value D, heaviest H, smallest S, total T:
  - main: T − floor(0.30·D)
  - night: T − S − floor(0.15·D)
- Take night exactly when S < the duty difference, roughly when S < 0.15·D. With the minimal declaration D = H, that's when the smallest crate is small relative to the heaviest one.
- Round 4 is the cautionary example: H = 36, S = 7, so night saved ~5 in duty but forfeited a 7 crate. I took night anyway on a sloppy estimate and lost ~2. Compute the exact duty difference (floor(0.15·D) vs floor(0.30·D)) — don't eyeball it. With H in the 20–40 range, the savings are typically 3–6 points, so night only wins when S is genuinely tiny (under ~5–6). That's rare; main is the correct default.
- If my three crates are close in value, take main: losing the smallest costs more than the halved duty saves.

**Overall:**
- Every round is independent; ignore standings and other players' declarations and routes. They have zero effect on my payoff. This run confirmed it — the players who varied their declarations and routes gained nothing at my expense; my score tracked my hold quality minus duty, nothing else.
- Clean rule for nearly every hand: declare exactly my heaviest crate, and pick the route by comparing S against the exact duty difference (with D = H, roughly 0.15·H). Main is right in almost all cases; night is free money only when the smallest crate is junk.
- Final score +329 came almost entirely from kept crates. Next time the remaining edge is small: avoid one bad route call (~2 points a round at most) and never touch the declare floor.