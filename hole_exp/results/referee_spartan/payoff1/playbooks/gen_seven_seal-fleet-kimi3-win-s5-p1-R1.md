---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1666
---
- I always compute my allowed residue-preserving reports first: my draw d permits reports d and d+7 (where valid). The seal only cares about each report's value mod 7, so the largest safe report is d+7.
- When my draw is 0 I report 7, when 1 I report 8, when 2 I report 9 — this maximizes my points subject to never breaking the seal through my own action.
- I never report a value that isn't congruent to my draw mod 7. Any such report makes the seal depend purely on luck of others' draws, and a failure wipes everyone's points including mine.
- I apply the deviation arithmetic before choosing: the seal passes iff 3(A−a)+5(B−b)+6(C−c) ≡ 0 mod 7. My own deviation contributes a known term; if I deviate by k, the others' combined deviations must exactly cancel my weighted k mod 7, which I cannot count on.
- If the seal repeatedly fails because others overreport off-residue, I do not join them. Inflating my own report off-residue does not fix the seal and only drops my score when it would have passed.
- I don't downgrade to reporting my raw draw out of caution — honest-but-maximal (d+7) is equally seal-safe and strictly better paid. Reporting d itself was a wasted opportunity unless the seal was already passing.
- When coordinating implicitly with strangers, I keep reporting d+7 every round regardless of past failures; it's the only strategy that lets the whole table score if anyone else also plays residue-honest, and it costs me nothing when they don't.
- I ignore scoreboard gaps as a reason to gamble. I cannot overtake a leader by breaking the seal I need to pass to score at all; the only way to gain is for the seal to pass while I report high.