---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2225
---
When the declare stage is put to me, I declare exactly the value of my heaviest crate — never more. The declared number only sets my duty rate; my score comes from crates actually held. There is no opponent to outbid: my rivals' declarations and running totals are noise, and over six rounds I never once gained by declaring above my heaviest. The only constraint is that declaring below my heaviest crate costs -40 plus duty at 0.30 of my true total, so heaviest-crate value is the exact floor. This worked cleanly in every round, including a weak hold like 8/9/9 (declare 9) and a strong one like 17/27/36 (declare 36).

When the route stage is put to me, I compare the two costs:
- main costs 0.30 × heaviest (my declared value).
- night costs smallest + 0.15 × heaviest.
I take night when my smallest crate is worth less than 0.15 × my heaviest; otherwise main. In practice this threshold is low — with heaviest in the 20s and 30s, night only wins if the smallest is under ~4-5, which a uniform 5-40 draw almost never produces. So main is the right default almost every round, and I should not agonize over it: with holds like 5/5/16, 20/24/31, 8/15/17, 17/27/36, 14/26/28, main was correct each time. Night is a genuine option only when the hold is bottom-heavy (e.g. 5/8/38) or the spread is extreme — and even then I should check whether the confiscation of the smallest outweighs the duty savings, since night also forfeits that crate's value.

I never declare a high number on a weak hand "to stay competitive" — that would be paying duty on points I don't hold while still keeping the small crates. Round 5 confirmed the opposite: declaring 9 on 8/9/9 gave a trivial duty and kept all three crates.

Two nuances to remember: the spot check lifts the heaviest crate, so my declaration must cover it before the route is chosen; confiscation on the night route takes the smallest, so the declaration floor doesn't change. And on the last round, or any round where the arithmetic is close, I recompute both route options explicitly from my actual three crate values rather than defaulting to main out of caution — but I should also recognize that "close" is rare, and defaulting to main is usually not a mistake at all.