---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2654
---
When I declare, I ignore table talk, history, and "signals." Duty is computed only from my declared number, so the smallest legal declaration is weakly best. I declare exactly the value of my heaviest crate: that is the floor of the safe range, it can never be flagged, and it minimizes my duty no matter which route I take. Declaring my true total just raises my duty with zero upside. Declaring below my heaviest crate risks the -40 penalty plus a recomputed 0.30 duty on the true total, so I never do it unless I am desperate far behind in the final round — and even then I remember the expected cost is steep: penalty plus recomputed duty versus a duty saving of only 0.30 × (heaviest − declared).

I never copy the declaration range of the table or try to "look normal." Other players' numbers do not enter my score at all — the last episode confirmed this again: everyone declared 24-40, nobody was flagged, and my scores came purely from my own crate arithmetic. Each round is solved on my own three crates alone.

When I choose a route, I do arithmetic, not mood. Night beats main exactly when my smallest crate is worth less than 15% of my declared value (night saves 15% of the declaration in duty but forfeits the smallest crate, and my safe declaration keeps the audit out of it). Concretely: I compute 0.15 × my declared value; if my smallest crate is below that number, I take night, otherwise main. Since I declare minimally at my heaviest crate, the test is smallest < 0.15 × heaviest, which requires an unusually tiny crate, so main is almost always the right pairing — that was true in every round of the last episode and the formula told me so each time. If my smallest crate is exactly near the threshold, floor ties matter little; I still follow the formula.

When I am behind near the end and need a swing, my lever is route choice (night with a small enough sacrifice) rather than over-declaring, which only burns points. Over-declaring is never a comeback tool; I stopped using it as one and dropped 19 points behind Odalie in the final round doing nothing wrong — variance, not a mistake to fix.

When I am ahead near the end, I change nothing: the same minimal declaration and the same arithmetic route choice are already the maximum-expected-value play, so I do not get conservative or fancy based on standings. I ignore my past "steadier/riskier" impulses entirely — the formula replaces all of them.

One extra discipline I now keep: on the route stage I always recompute the threshold against the number I actually declared this round, not a remembered default, so a fatigued "same as usual" never replaces fresh arithmetic.