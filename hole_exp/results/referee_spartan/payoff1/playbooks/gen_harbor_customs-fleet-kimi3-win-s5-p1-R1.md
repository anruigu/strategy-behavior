---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 2355
---
When I'm dealt my hold, I first sort the crates and compute three numbers: the true total T, the value of my heaviest crate (the floor of any legal flag-free declaration), and my smallest crate (what night costs me).

When choosing my declaration, I never go below my heaviest crate — the spot check is guaranteed to weigh it, so underdeclaring below it pays -40 and a recomputed full duty, which is always worse than just declaring more. My default declaration is the true total or a slight underdeclare down to the heaviest crate, never below it.

When deciding between declaring low and declaring honestly, I do the math: shaving the declaration by D saves 0.30·D on main or 0.15·D on night — small beans compared to the -40 risk, so I keep declarations close to true value rather than gambling for single-digit duty savings.

When choosing a route, I compare by arithmetic, not by feel: main costs floor(0.30·d); night costs floor(0.15·d) plus losing my smallest crate. I take night only when 0.15·d exceeds my smallest crate's value — i.e., roughly when my declared value is more than about 7× my smallest crate. Small-crate-heavy holds with a fat top crate (like 5/33/34) are night candidates; balanced holds almost always favor main.

When my smallest crate is above ~20, I essentially never take night — losing a 19+ crate to save ~11 duty is a straight loss. That was my clear mistake: taking night with a high declaration on a balanced hold (19/23/32). Don't repeat it.

When I declare truthfully at full value, main is nearly always correct, since the whole point of honesty was avoiding the flag, and night just throws away a good crate.

When I'm trailing late in the match, I don't chase with wild underdeclarations — the leaderboard only tells me others' points, not their hands, and a flag costs me 40+. Instead I keep declaring at least the heaviest crate and squeeze value through the route choice, which is the only lever that reliably moves my score.

When everyone else is also declaring near full value, I do the same; the game has no bluffing payoff that survives the mandatory heaviest-crate weigh-in, so consistent honest-plus-main lines beat cleverness over six rounds.

Before locking each route, I run one line of arithmetic: night wins only if smallest crate < declared × 0.15. If the numbers don't clear that bar, I say main.