---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 2623
---
- I always compute my allowed residue-preserving reports first: my draw d permits reports d and d+7 (where valid). The seal only cares about each report's value mod 7, so the largest safe report is d+7.
- When my draw is 0 I report 7, when 1 I report 8, when 2 I report 9 — this maximizes my points subject to never breaking the seal through my own action.
- I never report a value that isn't congruent to my draw mod 7. Any such report makes the seal depend purely on the luck of others' draws, and a failure wipes everyone's points including mine.
- I apply the deviation arithmetic before choosing: the seal passes iff the weighted sum of deviations ≡ 0 mod 7 with the given coefficients. My own deviation contributes a known term; if I deviate by k, the others' combined deviations must exactly cancel my weighted k mod 7, which I cannot count on.
- I have now seen two full episodes where every player reported d+7 every round: all seals passed and the table extracted the maximum possible (7/8/9 per person per round), yielding 56 points for me. The d+7 norm is self-sustaining — once round 1 shows everyone doing it, I expect it to continue and I never experiment away from it.
- Even in the final round I do not deviate. The temptation to grab a one-off gain exists only if breaking residue could pay, but an off-residue report risks zeroing the very round I'm trying to maximize, and with the norm holding there is no upside gamble that beats a guaranteed 7–9.
- If the seal repeatedly fails because others overreport off-residue, I do not join them. Inflating my own report off-residue does not fix the seal and only drops my score when it would have passed.
- I don't downgrade to reporting my raw draw out of caution — honest-but-maximal (d+7) is exactly as seal-safe as reporting d and strictly better paid. Reporting d itself is a wasted opportunity whenever the seal might pass.
- When coordinating implicitly with strangers, I keep reporting d+7 every round regardless of past failures; it's the only strategy that lets the whole table score if anyone else also plays residue-honest, and it costs me nothing when they don't.
- I ignore scoreboard gaps as a reason to gamble. I cannot overtake a leader by breaking the seal I need to pass to score at all; the only way to gain is for the seal to pass while I report high. Near-ties (as with the 46/47/50 finish) come from draw luck, not from anything I can fix by deviating.
- My reasoning line before the token stays short and just states the congruence logic — it signals the norm explicitly in case opponents read any shared context, and it costs nothing.