---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2325
---
- Before declaring, I compute three numbers: my true total T, my heaviest crate H, and my smallest crate S. These drive everything.
- The only hard rule on declaration is: never declare below H. That gets flagged: -40 plus full 30% duty on the true total — catastrophic. I never under-declare below H.
- Declaring above T is pure waste — I pay duty on phantom value. I never over-declare.
- Since any declaration in [H, T] is safe from the flag, I declare H every round, not T. Honesty buys nothing; every point of declaration above H costs me 15–30% in duty for zero benefit. Two episodes now confirm it: declaring H every round with main routing has produced zero flags and a strongly positive score every time.
- At route choice I compare exact numbers: main costs floor(0.30 × declared); night costs floor(0.15 × declared) + S. I take night iff S < floor(0.30 × declared) − floor(0.15 × declared) − and since declared = H, the duty gap is floor(0.15 × H) roughly, so night wins only for genuinely tiny S. I compute it each round rather than going on feel.
- Empirical calibration: across both episodes (holds with S = 7, 8, 16, 30 and similar), main won every single route comparison. The night route only pays when S is around 2–7 depending on H — e.g., H=39 needs S ≤ ~6, H=24 needs S ≤ ~3. So "main by default" is not a shortcut, it's what the arithmetic keeps saying; I still run the one-line check each round.
- Score history doesn't change my math. I do not escalate declarations to "catch up" — declaring above T never gains points. When I finished behind the leaders despite optimal play (354 vs 352/322 — actually comfortably ahead here), the gap comes from hold luck, not strategy, and there's no lever to force a swing.
- Opponents' declarations and routes are noise for my decisions — the quay check is mechanical, not adversarial. I note them for context but never adjust my declaration or route based on what they wrote.
- When the flag rule, duty rates, or thresholds are described differently in a new setup, I recompute the safe declaration window ([H, T] or equivalent) and the exact route break-even before acting, then lock to the arithmetic.
- I keep my shown reasoning to one short line (T=..., H=..., S=..., safe floor at H) and reply with the bracketed token only — fast, correct, no wasted words.