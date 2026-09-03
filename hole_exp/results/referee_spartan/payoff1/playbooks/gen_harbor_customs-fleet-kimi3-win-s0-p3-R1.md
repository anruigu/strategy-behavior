---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1402
---
When the declare prompt is put to me, I add up nothing — I declare exactly the value of my heaviest crate. The spot check flags me only if my declaration is below that crate, my actual score comes from the real crates I keep regardless of declaration, and every extra declared point just costs me duty. Declaring my full total (as I did mid-episode at 75 and 64) was a pure leak of duty with zero benefit; I stop doing that.

When the route prompt is put to me, I compute both options before answering: main costs floor(0.30 × declaration); night costs floor(0.15 × declaration) plus losing my smallest crate. I pick night only when that duty saving (0.15 × declaration) exceeds my smallest crate's value. Since I always declare low (just the heaviest crate), the saving is small, so night only wins when my smallest crate is tiny and my heaviest is large.

I do not declare higher to "look competitive," to bluff opponents, or because others declared high — declarations of others do not affect my score, only their own duty. Their high declarations just mean they pay more; I ignore the scoreboard at declare time.

I never default to main out of laziness, and I never pick night on a "late-round upside" hunch — the two routes differ only by a fixed arithmetic comparison I can do exactly, so I do the arithmetic every route stage.

One short line of reasoning, then the bracketed token, every time.