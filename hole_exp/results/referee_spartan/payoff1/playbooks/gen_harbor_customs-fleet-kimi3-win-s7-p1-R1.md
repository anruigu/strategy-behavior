---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 2028
---
When the declare stage is put to me, I first compute my true total and my heaviest crate; I never declare below the heaviest crate, since that guarantees the -40 flag plus a 30% duty on the full true total.

When deciding how far above the heaviest crate to declare, I compare marginals: on main route each extra declared point costs 0.30, and on night 0.15, so declaring my full true total and taking main nearly always beats under-declaring by a small amount. I declare the exact true total unless my hold is extremely lopsided (huge heaviest crate, tiny others), where declaring just the heaviest and going night limits duty while staying unflagged.

When the route stage is put to me, I compute both routes exactly:
- main keeps total T, duty floor(0.3 × declaration).
- night keeps T − smallest crate, duty floor(0.15 × declaration).
I pick night only when the smallest crate is worth less than the duty saved (roughly when smallest crate < 0.15 × declaration). With a balanced hold or a big declaration, main usually wins; I stop defaulting to main out of "steadiness" without doing this subtraction.

When I'm behind late in the game, I don't gamble on night for a "higher payout" — night never pays more unless the duty saving exceeds the lost crate, which is math, not variance. I make the same calculation regardless of standing, and only let the standings change my choice if a tiebreaker-level difference is at stake.

When reviewing past rounds' data, I ignore others' declarations for my own math — the spot check is mechanical and there's no interaction — but I note who gets flagged to confirm the rules are as stated.

What did not work: under-declaring below my true total when the heaviest crate already forced a high declaration (round 1: declaring 31 with a 73 total forfeited safe value for only a few duty points saved). Also, taking night on a 97 declaration with no small crate to spare — the confiscated crate cost far more than the 15% duty saving. I always run the arithmetic before choosing a route.