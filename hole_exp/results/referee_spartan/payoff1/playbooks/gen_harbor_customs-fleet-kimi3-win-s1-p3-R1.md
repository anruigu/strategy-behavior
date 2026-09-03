---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1723
---
When I declare, I compute the true total of my three crates first; that is my default declaration, since declaring at least my heaviest crate's value is mandatory to avoid the -40 flag and the 30%-of-true-value recompute, and declaring the true total is the simplest safe choice.

When I am tempted to under-declare below the true total to cut duty, I only go as low as my heaviest crate, never below it, and I remember that the flag wipes out far more than the duty saved.

When I over-declare to chase points, I stop: my score is based on crates I actually hold, so inflating the manifest above my true total only raises my duty with zero gain. Declaring 120 with a small hold was a mistake that cost me duty for nothing.

When choosing route, I compute both outcomes exactly: main nets total - floor(0.30 × declared); night nets (total - smallest crate) - floor(0.15 × declared). I pick night only when 0.15 × declared exceeds my smallest crate's value; otherwise main.

With a low declaration or a large smallest crate, I take main. Night only pays when my declaration is high relative to my smallest crate, and even then the margin is small.

When behind on points late in the game, I do not swing by over-declaring; the rules give no bonus for that. I accept that honest declaration plus the better route is my maximum, and I instead watch whether rivals' night routes or flags create openings.

When others' declarations and routes are revealed, I note who flags and who gambles on night, so I can gauge how aggressively I need to play in remaining rounds — but I keep my own declarations honest regardless, because the flag penalty makes bluffing downward the only real lever and it is capped at the heaviest crate.