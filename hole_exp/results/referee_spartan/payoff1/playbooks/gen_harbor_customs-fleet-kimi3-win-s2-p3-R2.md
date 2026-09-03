---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 3200
---
- Before anything, I compute my true total, my heaviest crate, and my smallest crate. Every decision flows from those three numbers.
- When a declare is put to me, I declare exactly my heaviest crate's value. Anything higher than the heaviest only increases my duty for zero benefit — declaring extra is never "aggressive," it is just paying more tax. Anything below the heaviest gets flagged: -40 penalty plus full 30% duty on the true total, which is catastrophic.
- Scoring is crates minus duty, and duty scales with my declaration. I never declare above my heaviest crate unless the format explicitly rewards declared value. A high manifest is not a score and impresses no one.
- Route decision with declaration D = heaviest crate h: main costs 0.3·h; night costs my smallest crate s plus 0.15·h. Night wins only when s < 0.15·h, i.e. h > about 6.7·s. I ALWAYS run this comparison on the actual numbers before routing — no exceptions, no vibes.
- Hard lesson from round 6: I went night with s = 21 and h = 40, rationalizing it in my text while the arithmetic screamed main (night cost 27 vs main 12 — I threw away ~15 points). My one-line reasoning must state the actual computed costs of both routes, not a fuzzy rule I can bend. If my written reason says "night is better when smallest is under X," I verify my smallest actually is under X before sending.
- With crates in the 5-40 range, night is very rarely correct: since s ≥ 5, night only wins when h > ~33 AND s < 0.15·h simultaneously — a heavily lopsided hold with a cheap runt and a huge top crate. My default route is main; I need concrete arithmetic to talk me into night.
- Quick heuristic after verifying the math: lopsided hold with a runt crate (single digits) and a big heaviest → night might win. Anything resembling even values → main, automatically.
- I never factor splashing or bluffing into the declaration: the check is mechanical (heaviest crate vs declared), opponents can't challenge me, and there's no interaction — so there's nothing to bluff.
- With a weak hold (low total), I don't panic-declare high; I still declare exactly the heaviest value and take the better route. A low-variance 30-50 point round beats donating duty to the harbor.
- Behavior around score position: being behind does not change optimal play, because my declaration can't create points, only lose them. I ignore the urge to "catch up" via bigger declarations; I just maximize each round's expected value. I fell behind this game and the standings never once changed what the right move was.
- Full arithmetic check I run every round: main = total − floor(0.3·D); night = total − s − floor(0.15·D) − s... written properly: main EV = total − floor(0.3·D); night EV = (total − s) − floor(0.15·D). Both with D = heaviest. I write both numbers down and pick the larger.
- Last round of the match changes nothing: no endgame bonus for declaration, no elimination, no interaction. Round 6 is played with the same cold arithmetic as round 1.
- If a future variant ever rewards declared value (e.g., payouts scale with the manifest), I recompute, but the flag rule still sets the floor: never declare below the heaviest crate under any circumstances.