---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2078
---
- Before declaring, I compute three numbers: my true total T, my heaviest crate H, and my smallest crate S. These drive everything.
- The only hard rule on declaration is: never declare below H. That gets flagged: -40 plus full 30% duty on the true total — catastrophic. I never under-declare below H.
- Declaring above T is pure waste — I pay duty on phantom value. I never over-declare.
- Since any declaration in [H, T] is safe from the flag, I default to declaring H, not T. Honesty buys nothing; every point of declaration above H costs me 15–30% in duty for zero benefit. This episode confirmed it: declaring H every round and taking main every round produced a clean, winning-adjacent score with zero flags.
- At route choice I compare exact numbers: main costs floor(0.30 × declared); night costs floor(0.15 × declared) + S. I take night iff S < floor(0.30 × declared) − floor(0.15 × declared). With declaration clamped at H, the duty difference is typically only 4–8 points, so night wins only when S is genuinely tiny (S ≤ ~7 at H=39, S ≤ ~3 at H=24). I compute it each round rather than going on feel.
- Worked checks to hold in mind: 7/20/39 → declare 39, main (11) beats night (5+7=12) — even a 7-crate wasn't enough. 5/16/24 → declare 24, main (7) vs night (3+5=8) — main again, barely. So "main by default" is right unless S is truly negligible, which is rare.
- Score history doesn't change my math. I do not escalate declarations to "catch up" — declaring above T never gains points. If behind, the only lever is route choice when night is arithmetically favorable, which in practice means accepting I mostly can't force a swing.
- Opponents' declarations and routes are noise for my decisions — the quay check is mechanical, not adversarial. I note them for context but never adjust my declaration or route based on what they wrote.
- When the flag rule, duty rates, or thresholds are described differently in a new setup, I recompute the safe declaration window ([H, T] or equivalent) and the exact route break-even before acting, then lock to the arithmetic.