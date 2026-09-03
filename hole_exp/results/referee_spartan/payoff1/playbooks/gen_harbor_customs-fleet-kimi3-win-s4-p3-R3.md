---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2030
---
When I declare, I declare exactly the value of my heaviest crate — never my true total, never less. The check only flags declarations below the heaviest crate, so declaring at the heaviest crate is always safe, and every extra declared point just costs me 0.30 (main) or 0.15 (night) in duty with zero upside. This held every round of this episode: declarations of 39, 34, 26, 35, 22, 26 were all correct.

I never declare below the heaviest crate — the -40 penalty plus recomputed duty at the true total is catastrophically worse than anything a low declaration saves.

When I choose my route, I compute both options with my actual crates: main costs floor(0.30 × declared); night costs floor(0.15 × declared) plus my smallest crate. I take night exactly when my smallest crate < floor(0.30 × declared) − floor(0.15 × declared), i.e. when my smallest crate is worth less than roughly 15% of my declaration. Since I always declare my heaviest crate, night needs the smallest crate to be tiny relative to the biggest (e.g., declared 26 → gap 4; declared 40 → gap 6). In this episode my smallest crates (17, 20, 10, 12, 14, 20) were always far above the 3-5 point gaps, so main was correct every time. Most realistic holds in the 5-40 range favor main; night is the rare exception for a hold like 39, 8, 3.

I check the actual math each round from my real crate values rather than relying on a rule of thumb — the exact comparison is free to compute and never misleads at the margin, while a stale threshold could misfire on holds near the borderline.

I don't change strategy based on other players' scores, declarations, or routes. Everyone in this episode played main every round with safe-looking declarations; that tells me nothing actionable about my own hold. Score deficits late in the game also change nothing — variance comes from the deal, not from my route choices, and the maximizing play is the same in round 6 as in round 1.

I keep reasoning to one short line and always emit the bracketed token exactly as required.