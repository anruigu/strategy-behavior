---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 2637
---
When the declare stage is put to me, I compute the true total of my three crates first, then decide whether to declare full, partial, or just the heaviest crate.

The spot check only compares my declaration against my single heaviest crate, so I never declare below my heaviest crate's value — that is the hard floor, and dipping under it costs me -40 plus a full 30% duty on my true total. I treat that floor as non-negotiable every round.

When my hold is weak (low total, nothing to protect), I declare exactly the heaviest crate's value: that minimizes duty at 30% of a small number and is completely safe from the flag. I did this in the opener and it worked.

When my hold is middling or strong, I declare my true total. Under-declaring saves a little duty but caps nothing — I keep all my crates on main route regardless, and the score drives off crates minus duty, so declaring truthfully is safe (truth is always ≥ heaviest crate? No — only if the heaviest is less than half the total, which it usually is). If my heaviest crate is more than half my total (e.g. 5, 10, 30), declaring truthfully still clears the check, so truthful declaration is always flag-safe; I only shave the declaration down toward the heaviest-crate floor when the duty savings matter and the lead is comfortable.

When deciding route, I run the arithmetic, not a feeling: main costs 0.30 × declared; night costs 0.15 × declared plus my smallest crate. Night wins only when 0.15 × declared is less than my smallest crate's value. With a small declared value and a big smallest crate, night is clearly better — I should have taken night far more often. In this game I routed main every single time and left points on the table; next time I do the comparison every round: if smallest_crate > 0.15 × declared, go night, otherwise main.

When the spread between my declared value and true total is large, night becomes relatively more attractive since the duty discount applies to the whole declaration while the confiscation cost is fixed.

When I hold the lead late, I don't get timid with the declaration — flag safety depends only on the heaviest crate, not on the margin — but I do keep declarations truthful and let the route math decide route, rather than defaulting to the "safe-feeling" main route.

When trailing late, I declare at the heaviest-crate floor and take whichever route the arithmetic favors, squeezing maximum expected value rather than protecting a score that's already behind.

My one-line reasoning before each token: state my total, the check floor, and the route comparison, so the decision is forced by numbers rather than habit.