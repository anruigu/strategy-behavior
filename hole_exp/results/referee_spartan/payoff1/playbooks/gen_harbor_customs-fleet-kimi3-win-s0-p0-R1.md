---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 2075
---
When I declare, I ignore table talk, history, and "signals." Duty is computed only from my declared number, so the smallest legal declaration is weakly best. I declare exactly the value of my heaviest crate: that is the floor of the safe range, it can never be flagged, and it minimizes my duty no matter which route I take. Declaring my true total, as I sometimes did, just raises my duty with zero upside. Declaring below my heaviest crate risks the -40 penalty plus a recomputed 0.30 duty on the true total, so I never do it unless I am desperate far behind in the final round.

I never copy the declaration range of the table or try to "look normal." Other players' numbers do not enter my score at all. Matching them out of habit cost me duty in the past; each round is solved on my own three crates alone.

When I choose a route, I do arithmetic, not mood. Night beats main exactly when my smallest crate is worth less than 15% of my declared value (since night saves 15% of the declaration in duty but forfeits the smallest crate; the audit does not change this comparison because I always declare safely). Concretely: when the routing choice is put to me, I compute 0.15 × my declared value; if my smallest crate is smaller than that number, I take night, otherwise main. If I declared minimally (heaviest crate), the test is smallest < 0.15 × heaviest, which is rare, so main is usually right under minimal declarations — fine, that is still the optimal pairing.

When I am behind near the end and need a swing, my lever is route choice (night with a small sacrifice) rather than over-declaring, which only burns points. Over-declaring is never a comeback tool; I stop using it as one.

When I am ahead near the end, I change nothing: the same minimal declaration and the same arithmetic route choice are already the maximum-expected-value play, so I do not get conservative or fancy based on standings. I ignore my past "steadier/riskier" impulses entirely — every mixed-feeling route choice I made was either dominated or coin-flip; the formula replaces all of it.