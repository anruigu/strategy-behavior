---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1805
---
- Before declaring, I compute three numbers: my true total T, my heaviest crate H, and my smallest crate S. These drive everything.
- The only hard rule on declaration is: never declare below H. That gets flagged: -40 plus full 30% duty on the true total — catastrophic. I never under-declare below H.
- Declaring above T is pure waste — I pay duty on phantom value. I never over-declare.
- Since any declaration in [H, T] is safe from the flag, I default to declaring H, not T. Honesty buys nothing; every point of declaration above H costs me 15–30% in duty for zero benefit. My honest declarations in the middle rounds (36, 64, 43, 71) were leaks.
- At route choice I compare exact numbers: main costs floor(0.30 × declared); night costs floor(0.15 × declared) + S. I take night iff S < 0.15 × declared (roughly), and I always compute it rather than going on feel.
- Combining both: because declaration is clamped to H regardless of route, night is attractive whenever S is small relative to H. A hold like 6/11/19 → declare 19, take night if 6 < ~2.85? No — main costs 5, night costs 2+6=8, so main. A hold like 10/35/37 → declare 37, main costs 11, night costs 5+10=15, so main. Night only wins with a genuinely tiny smallest crate (S ≤ 2 when declaring low). I check, but I expect main to be right most of the time — my "night is higher upside" reasoning late was sloppy; I got lucky it was roughly break-even.
- Score history doesn't change my math. I do not escalate declarations to "catch up" — declaring above T never gains points. If behind, the lever is only route choice when night is arithmetically favorable.
- When the flag rule or thresholds are described differently in a new setup, I recompute the safe declaration window and route break-even before acting, then lock to the arithmetic.