---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2490
---
When the declare stage is put to me, I compute the true total of my three crates first, then set my declaration.

The spot check only compares my declaration against my single heaviest crate, so I never declare below my heaviest crate's value. That is the hard floor, non-negotiable every round: dipping under it costs -40 plus a full 30% duty on the true total, which drowns any possible duty saving. There is no desperate-trailing exception.

My declaration is always exactly my heaviest crate's value. It is flag-safe by construction, it minimizes the duty base on either route, and nothing in the scoring rewards declaring more — score is crates kept minus duty, so a smaller legal declaration is strictly better. This episode confirmed it: six floor declarations, correct routes, no penalties, and I finished joint-best at +344. Declaring anything above the floor (the old round-1 mistake of declaring the true total) is pure waste.

Before sending, I check the bracketed number equals the heaviest crate value I computed — token must match reasoning, every time.

For routing, the comparison direction, fixed once and for all: night saves 0.15 × declared in duty but forfeits my SMALLEST crate. So: if smallest crate > 0.15 × declared, take MAIN; if smallest crate < 0.15 × declared, take NIGHT. A valuable smallest crate is a reason to keep it (main), never a reason to take night. I state this in the reasoning line in checkable form: "smallest X vs saving 0.15 × declared = Y; night only if X < Y."

Since I declare the heaviest crate, 0.15 × declared is typically 3-7 points, so main wins the overwhelming majority of the time — every route this episode was main and every one was correct. Night only becomes live when my smallest crate is a genuine 5-ish dud sitting next to a 35+ heaviest crate (saving around 6+), i.e. smallest < 0.15 × heaviest. I run the arithmetic anyway rather than assuming; the formula takes one line.

Opponents at the table also declare near their floors (their declarations consistently sit in one-crate range of plausible heaviest values), so nobody is gifting edges through truthful declaring — I win by never paying extra duty and never taking penalties, not by out-guessing anyone.

Late in the match, leading or trailing, the plan does not change: floor declaration, computed route. The maximum squeeze is already in those two lines; there is no riskier play that pays. Standing pat means not blundering — clean arithmetic in, matching token out.