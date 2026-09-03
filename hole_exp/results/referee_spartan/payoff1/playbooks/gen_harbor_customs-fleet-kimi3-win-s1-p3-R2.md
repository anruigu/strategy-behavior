---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2159
---
When I declare, I compute the true total of my three crates first; that is my default declaration, since declaring at least my heaviest crate's value is mandatory to avoid the -40 flag and the 30%-of-true-value recompute, and declaring the true total is the simplest safe choice.

When I am tempted to under-declare below the true total to cut duty, I only go as low as my heaviest crate, never below it, and I remember that the flag wipes out far more than the duty saved.

When I over-declare, I stop: my score is based on crates I actually hold, so inflating the manifest above my true total only raises my duty with zero gain.

When choosing route, I use my OWN known smallest crate — I always know it, so phrases like "no tiny-crate signal" are nonsense. I compare exactly: night beats main when floor(0.30 × declared) - floor(0.15 × declared) exceeds my smallest crate's value. Equivalently, night nets (total - smallest) - floor(0.15 × declared) versus main's total - floor(0.30 × declared); I compute both numbers and take the larger.

I do not default to main out of vague caution. In a past episode I took main with declared 67 and a smallest crate of 5, where night would have saved 10 duty for a 5-point crate — a clear ~5-point miss. Whenever my hold is lopsided (one small crate, two big ones), night is often the right call even at moderate declarations.

Night loses its appeal only when my smallest crate is genuinely large (close to or above 0.15 × declared). With a balanced hold like 13/14/39 or 15/16/32, main is correct and I take it without agonizing.

When behind on points late in the game, I do not swing by over-declaring; the rules give no bonus for that. My levers are the route choice and, at most, declaring down to my heaviest crate — I squeeze those rather than inventing gambles the scoring does not reward.

When others' declarations and routes are revealed, I note who flags and who takes night, so I can gauge how aggressively I need to play in remaining rounds — but I keep my own declarations honest regardless, because the flag penalty makes bluffing downward the only real lever and it is capped at the heaviest crate.