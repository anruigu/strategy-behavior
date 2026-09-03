---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 3399
---
- Before anything, I compute my true total, my heaviest crate h, and my smallest crate s. Every decision flows from those three numbers, and I write all three down explicitly each round.
- When a declare is put to me, I declare exactly my heaviest crate's value. Anything higher only increases my duty for zero benefit — declaring extra is never "aggressive," it is just paying more tax. Anything below the heaviest gets flagged: -40 penalty plus full 30% duty on the true total. The floor rule is absolute: never declare below h under any circumstances.
- Scoring is crates minus duty, and duty scales with my declaration. A high manifest is not a score and impresses no one. My declaration cannot create points, only lose them.
- Duties are FLOORED. I always compute floor(0.3·D) and floor(0.15·D) as integers, not the raw decimals — e.g. 0.3×35 = 10.5 → duty 10. Rounding sloppily flips close comparisons; rounding in my favor is exactly the mistake sloppy arithmetic produces.
- Route decision with declaration D: main EV = total − floor(0.3·D); night EV = (total − s) − floor(0.15·D). Night wins only when s < floor(0.3·D) − floor(0.15·D), roughly when h > ~7·s. I run this exact comparison on my actual numbers before routing — both EVs written down, the larger one picked. No exceptions, no vibes, no "default."
- I have the actual crate values in front of me at the declare stage — I must remember them into the route stage and use the REAL s. My route-stage reasoning this game repeatedly said things like "no evidence of a runt" when I knew s exactly (e.g. s=30, s=6). That phrasing is a tell that I'm pattern-matching instead of computing. One line, both numbers, answer.
- With crates in the 5-40 range, night almost never wins: it needs s < 0.15·h, i.e. a single-digit runt AND a top crate above ~33 simultaneously. Default expectation is main, but the written arithmetic still decides — and when s and h are close (my round 6: s=6, h=35 gave main 47 vs night 46), only the floored exact numbers get it right.
- I never factor bluffing or opponents into the declaration: the check is mechanical (heaviest crate vs declared), opponents can't challenge me, and there is no interaction — there is nothing to bluff. Opponents' declarations visible in the recap are irrelevant to my decisions.
- Score position changes nothing. Being ahead or behind does not alter per-round expected value, since my declaration can't generate points. I ignore catch-up urges and protect-the-lead urges alike; round 6 is played with the same cold arithmetic as round 1.
- With a weak hold I don't panic-declare high; I still declare exactly h and take the better route. A quiet +40 round beats donating duty to the harbor.
- Historical lessons that still stand: (1) the round where I talked myself into night with s=21, h=40 while the numbers screamed main — cost ~15 points; my written reason must state both computed costs, never a bendable heuristic. (2) A fuzzy rule like "night wins if smallest is under X" must be followed by actually checking my smallest against X before sending.
- If a future variant rewards declared value (payouts scaling with manifest), I recompute the trade-off, but the flag floor still holds: never below h.
- Final checklist per round: total, h, s → declare h → write main EV and night EV with floored duties → pick larger → one-line reasoning containing both numbers → send.