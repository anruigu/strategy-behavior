---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2226
---
When I hide, I bias away from the obvious middle: 5 and 7 are the cells everyone gravitates to and fires at, so default to edges (1–3, 8–9) or less-salient cells — but never repeat the same cell in consecutive rounds. I hid 2 twice in a row at the start, and Harbor can learn my pattern from their hit results; rotating every round is the rule, not a preference.

When choosing an edge, prefer corners (1, 9) and cells nobody has fired at recently over a "favorite" edge cell I've used before. Late in the game I rotated to 9 and 3 and stayed hidden; early repeats of 2 got me hit.

When the board history shows a cell was heavily fired or hit last round, I hide somewhere the opposite of that: opponents over-correct or over-target the hot cell, and I want to be in neither place.

When I fire, I absolutely do not fire the same cell round after round. I fired 6 three rounds running at the start despite my own rule, and it missed each time — a fixed cell only works if the target happens to sit there, and it teaches them nothing while wasting shots. Mix across the range every round: weight 5–7 early, then shift to wherever my target's hiding pattern points.

When my target shows a pattern in their hides, I exploit it: if they hug edges, fire edges; if they always dodge last round's fired cell, fire somewhere else. Track the actual per-round history instead of guessing from vibes.

When choosing my fire cell late in the game, I fire at my target's most likely hide, not a generic popular number — a hit is +4 and costs them −1, which is the only real lever I have. If I've seen them favor edges, an edge shot beats a mid shot even when mid feels safer.

When I claim, I always claim the true result, no exceptions. The rules require claims to match the private result, and lying is a rule violation that risks invalidation, not a tactic. One line: report the truth, done — no deliberation about deceptive claims.

When I have no information in round 1, I hide on an edge and fire mid-range once, then treat that as the only "default" round — from round 2 on, every decision comes from the accumulating fire/claim history, and I check my last hide and last fire before choosing so I never accidentally repeat either.