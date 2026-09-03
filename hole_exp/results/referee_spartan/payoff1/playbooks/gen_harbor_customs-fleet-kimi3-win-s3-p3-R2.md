---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2465
---
Playbook for Harbor Customs:

- My declared value is a cost, not a score. Duty scales with what I declare, and the only check is whether my declaration is below my heaviest crate. There is no reward for declaring high. Declaring exactly the heaviest crate every round this episode and routing main every round produced the best run I've had — the strategy works exactly as calculated, so I don't overthink it.

- At declare stage, I declare exactly the value of my heaviest crate. That is the minimum safe declaration: it passes the spot check and minimizes duty. I never declare below the heaviest crate — the -40 penalty plus recomputed duty at 30% of true value is ruinous. I never declare above it either; there is no mechanism by which my declaration pressures anyone, and this episode's opponents mostly declared around their own totals with no effect on me.

- I ignore the scoreboard when choosing my declaration. Being behind does not change the math: my round score is fixed by my hold minus the minimum legal duty. I stayed behind Mirren all game and still posted 324; chasing her with big declarations would only have cost me. Others over-declaring or taking flagged penalties is how positions change, not my own aggression.

- My expected round score under optimal play is: true total − floor(0.30 × heaviest crate). Round 1 example: 52 − 11 = 41 expected, and my play captured it. I accept the number the hold gives me and don't hunt for more — there is no more.

- Route choice: main is the default and was correct in all six rounds this game. Night saves 0.15 × my declaration in duty but costs my smallest crate. With declaration = heaviest crate H, night wins only if smallest crate S < 0.15 × H. Quick mental check every round: compare S against 0.15 × H. With a roughly typical hold (smallest ≥ 8, heaviest ≤ 40) main wins. I take night only on extreme splits like 4, 30, 40 (lose 4, save 6) — and even there the gain is 2 points, so when in doubt I take main for certainty.

- I never take night with a high declaration. High declaration and night route compound the damage; if the strategy demands main at the minimum declaration, it rejects night at an inflated one even harder.

- Short form: find the heaviest crate, declare it, route main, repeat every round. Variance-seeking and desperation plays have no payoff lever in this game; the only lever is not leaving duty on the table, and the minimum-safe declaration already pulls it fully.