---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 3253
---
When I declare, I compute the true total of my three crates first; that is my default declaration, since declaring at least my heaviest crate's value is mandatory to avoid the -40 flag and the 30%-of-true-value recompute, and declaring the true total is the simplest safe choice.

When I am tempted to under-declare below the true total to cut duty, I only go as low as my heaviest crate, never below it, and I remember that the flag wipes out far more than the duty saved. In practice I have found honest declaration serves me well; under-declaring to my heaviest crate saves little and I should only do it with a clear expected gain in mind, not as a reflex.

When I over-declare, I stop: my score is based on crates I actually hold, so inflating the manifest above my true total only raises my duty with zero gain.

When choosing route, I use my OWN known smallest crate — I always know it, so phrases like "no tiny-crate signal" or "my hold does not justify it" without numbers are nonsense. I compare exactly: night beats main ONLY when floor(0.30 × declared) − floor(0.15 × declared) STRICTLY EXCEEDS my smallest crate's value. Equivalently, I compute night = (total − smallest) − floor(0.15 × declared) and main = total − floor(0.30 × declared) and take the larger. On a tie, main is simpler and I take main.

I must actually run this arithmetic at the route stage instead of eyeballing it. In this episode I took night with declared 68 and smallest 13 (gap only 10 — a loss of 3), with declared 53 and smallest 9 (gap only 8 — a loss of 1), and with declared 66 and smallest 10 (gap exactly 10 — a mere tie, so main). The rule "night pays if my smallest is under the gap" only works when I compute the gap first and compare strictly; writing a true-sounding sentence about it is not the same as checking.

I do not default to main out of vague caution either. In a past episode I took main with declared 67 and a smallest crate of 5, where night would have saved 10 duty for a 5-point crate — a clear ~5-point miss. Whenever my hold is lopsided (one small crate, two big ones), night is often the right call even at moderate declarations.

Night loses its appeal only when my smallest crate is genuinely large (at or above the duty gap, roughly 0.15 × declared). With a balanced hold like 13/14/39 or 12/13/23, main is correct and I take it without agonizing — provided I have verified the gap, not assumed it.

When behind on points late in the game, I do not swing by over-declaring; the rules give no bonus for that. My levers are the route choice and, at most, declaring down to my heaviest crate — I squeeze those rather than inventing gambles the scoring does not reward.

When others' declarations and routes are revealed, I note who flags and who takes night, so I can gauge how aggressively I need to play in remaining rounds — but I keep my own declarations honest regardless, because the flag penalty makes bluffing downward the only real lever and it is capped at the heaviest crate.

Scores in this game are tight — single points separated the leaders going into round 6 — so the small 1–3 point leaks from sloppy route comparisons are exactly what decides placement. Precision on the night-gap arithmetic is my highest-value habit.