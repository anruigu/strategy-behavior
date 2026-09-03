---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2229
---
- Before anything, I compute my true total, my heaviest crate, and my smallest crate. Every decision flows from those three numbers.
- When a declare is put to me, I declare exactly my heaviest crate's value. Anything higher than the heaviest only increases my duty for zero benefit — declaring extra is never "aggressive," it is just paying more tax. Anything below the heaviest gets flagged: -40 penalty plus full 30% duty on the true total, which is catastrophic.
- My big misplay was declaring at or near my true total thinking high declarations earn points. They don't — scoring is crates minus duty, and duty scales with my declaration. I never declare above my heaviest crate again unless the format explicitly rewards declared value.
- When a route is put to me with declaration D = heaviest crate h: main costs 0.3·h; night costs my smallest crate s plus 0.15·h. I take night when s < 0.15·h (equivalently when h > ~6.7·s, or when I'm overpaying main duty relative to losing the small crate). I take main otherwise.
- Quick heuristic: if my smallest crate is cheap relative to my heaviest — typical when the hold is lopsided — I go night. If my crates are fairly even in value, I go main.
- I never factor splashing or bluffing into the declaration: the check is mechanical (heaviest crate vs declared), opponents can't challenge me, and there's no interaction — so there's nothing to bluff.
- With a weak hold (low total), I don't panic-declare high; I still declare exactly the heaviest value and take the better route. A low-variance 30-50 point round beats donating duty to the harbor.
- Behavior around score position: being behind does not change optimal play, because my declaration can't create points, only lose them. I ignore the urge to "catch up" via bigger declarations; I just maximize each round's expected value.
- Arithmetic check I run every round before routing: expected main = total − 0.3·D; expected night = total − smallest − 0.15·D. I pick whichever is larger, using D = heaviest in both.
- If a future variant ever rewards declared value (e.g., payouts scale with the manifest), I recompute, but the flag rule still sets the floor: never declare below the heaviest crate under any circumstances.