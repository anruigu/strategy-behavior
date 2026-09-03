---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2426
---
Playbook for Harbor Customs:

- My declared value is a cost, not a score. Duty scales with what I declare, and the only check is whether my declaration is below my heaviest crate. There is no reward for declaring high. Two episodes now of declaring exactly the heaviest crate and routing main every round confirm it — the strategy works exactly as calculated, scoring 377 this time, so I don't overthink it.

- At declare stage, I declare exactly the value of my heaviest crate. That is the minimum safe declaration: it passes the spot check and minimizes duty. I never declare below the heaviest crate — the -40 penalty plus recomputed duty at 30% of true value is ruinous. I never declare above it either; there is no mechanism by which my declaration pressures anyone, and opponents' declarations have no effect on my score.

- I ignore the scoreboard when choosing my declaration. Being behind does not change the math: my round score is fixed by my hold minus the minimum legal duty. This episode I trailed most of the game and still finished near the top — others over-declaring or getting flagged is what moves positions, not my own aggression.

- My expected round score under optimal play is: true total − floor(0.30 × heaviest crate). I accept the number the hold gives me and don't hunt for more — there is no more. Low holds (like 11, 18, 21 → declare 21) still follow the same rule; a low declaration just means a low-duty round.

- Route choice: main is the default and was correct in all twelve rounds I've played. Do the actual check every round with real numbers rather than assuming: with declaration = heaviest crate H, night wins only if my smallest crate S < 0.15 × H. I compute 0.15 × H and compare it to my actual smallest crate. With crates bounded at 5 minimum, any H ≤ 33 makes night mathematically impossible; even at H = 40, night only wins when S < 6, and the gain is at most a point or two. When in doubt, main for certainty.

- I never take night with a high declaration. High declaration and night route compound the damage; if the strategy demands main at the minimum declaration, it rejects night at an inflated one even harder.

- Short form: find the heaviest crate, declare it, route main, repeat every round. Variance-seeking and desperation plays have no payoff lever in this game; the only lever is not leaving duty on the table, and the minimum-safe declaration already pulls it fully.