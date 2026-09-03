---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 2736
---
**Declare stage:**
- My declared value must be at least my heaviest crate's value, or I eat a -40 flag plus 0.30 x true total duty. The floor is always "heaviest crate value" — never declare below it. This episode I declared exactly the heaviest crate all six rounds and was never flagged again (+352, up from +329). The rule held up perfectly two runs running. Keep doing it.
- Between the floor and the true total, declare as low as possible: heaviest crate value. There is no scoring benefit to a high declaration — only kept-crate value minus duty matters. Declaring near my true total just inflates duty at 0.15–0.30 rate for nothing.
- Declare exactly H, not H minus 1 — the spot check weighs the heaviest crate, so there is no slack.

**Route stage:**
- The route prompt does NOT show my crate values — only the declare prompt does. So I must decide the route at declare stage, while I can still see the hold, and just execute it at the route stage. This run I fell back on "no crate details given, default to main" several times. That happens to be the right default, but stop doing it on vibes: recall the hold from the declare screen and run the arithmetic.
- Compare the two payoffs directly with declared value D, heaviest H, smallest S, total T:
  - main: T − floor(0.30·D)
  - night: T − S − floor(0.15·D)
- Take night exactly when S < the duty difference, i.e. S < floor(0.30·D) − floor(0.15·D), which with D = H is roughly S < 0.15·H. Compute the exact floors — don't eyeball it.
- With H in the 20–40 range, the savings are typically 3–6 points, so night only wins when the smallest crate is genuinely tiny (under ~5–6). This run all my smallest crates were 5–18, so main was correct every round — which the default got right by accident. Next time, if I ever see a junk crate (S under ~5) alongside a heavy H, that's the one case to actually switch to night.
- If my three crates are close in value, take main: losing the smallest costs more than the halved duty saves.

**Overall:**
- Every round is independent; ignore standings and other players' declarations and routes. They have zero effect on my payoff. Two runs have confirmed this — my score tracks my hold quality minus duty, nothing else.
- Clean rule for nearly every hand: declare exactly my heaviest crate, and pick the route by comparing S against the exact duty difference (with D = H, roughly 0.15·H). Main is right in almost all cases; night is free money only when the smallest crate is junk.
- Score improved from +329 to +352 purely by keeping the discipline. The remaining edge is small and lies entirely in the route call: take main on autopilot, but actually check the arithmetic once per round in case S is tiny. Never touch the declare floor.