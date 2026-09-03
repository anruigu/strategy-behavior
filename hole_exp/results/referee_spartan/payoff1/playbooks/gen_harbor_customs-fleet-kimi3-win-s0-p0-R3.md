---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 3257
---
When I declare, I ignore table talk, history, and "signals." Duty is computed only from my declared number, so the smallest legal declaration is weakly best. I declare exactly the value of my heaviest crate: that is the floor of the safe range, it can never be flagged, and it minimizes my duty no matter which route I take. Declaring my true total just raises my duty with zero upside. Declaring below my heaviest crate risks the -40 penalty plus a recomputed 0.30 duty on the true total, so I never do it unless I am desperate far behind in the final round — and even then I remember the expected cost is steep: penalty plus recomputed duty versus a duty saving of only 0.30 × (heaviest − declared).

I never copy the declaration range of the table or try to "look normal." Other players' numbers do not enter my score at all. Each round is solved on my own three crates alone.

When I choose a route, I do arithmetic on my actual crates, not vibes about "typical" holds. Night beats main exactly when my smallest crate is worth less than 15% of my declared value: night saves 0.15 × declared in duty but forfeits the smallest crate. The exact test: compute 0.15 × declared; if smallest < that number, take night; otherwise main. I always know my own three crates, so there is NO guessing step — the formula is fully determined.

The critical discipline I now enforce: I plug my ACTUAL smallest crate into the formula every single round, and I never amortize the route decision with lines like "no indication of a tiny crate" or "that's nearly always the case." In my last episode I broke this rule in the final round: my smallest crate was 5, the threshold was 5.55, night was strictly better by about half a point, I even computed the correct answer at the declare stage in parentheses — and then at the route stage I wrote my boilerplate "main is correct" reasoning and took main anyway, throwing points away. The route stage gets fresh arithmetic with the real numbers every time, and if I computed the answer at the declare stage, I carry it forward instead of re-deriving garbage. Two steps I do mechanically at route time: (1) write down smallest crate value, (2) write down 0.15 × my actual declaration this round, (3) compare and report. Never skip to the conclusion.

When I am behind near the end and need a swing, my levers are minimal (route choice with small sacrifices) and the play I dislike (sub-safe declaration) is expensive; over-declaring is never a comeback tool. Mostly I accept variance — minimal declaration plus formula route is already maximum EV across all rounds, so "needing to catch up" rarely justifies deviation. If I do gamble in the final round, it is under-declaring despite the -40, never anything else, and only when the points gap is large relative to one round's swing.

When I am ahead near the end, I change nothing: the same minimal declaration and the same arithmetic route choice are already the maximum-expected-value play, so I do not get conservative or fancy based on standings.

Final-score sanity check I keep: each round's minimal safe play yields roughly (total − smallest-if-night-or-nothing) − 0.30 × heaviest; I do the sum once per round quietly so arithmetic slips, not strategy, are what I police.