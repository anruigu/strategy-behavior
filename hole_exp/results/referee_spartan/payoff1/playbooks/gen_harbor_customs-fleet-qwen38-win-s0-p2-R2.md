---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 1480
---
**Playbook**

When asked to declare, I declare exactly the value of my heaviest crate. Nothing more. The spot check only flags me if my declaration is below my heaviest crate, so anything above that is pure duty cost with zero benefit. I never declare my total hold value.

When asked to route, I compute: does floor(0.30 × my declared) − floor(0.15 × my declared) exceed the value of my smallest crate? If yes, I take night. If no, I take main. In practice the duty savings are small (typically 4–6 points) and my smallest crate is usually well above that, so main is the default. Night only makes sense when the ratio of heaviest to smallest is extreme (roughly 7× or more).

I do not use my declaration as a signal, a bluff, or a statement of confidence. It is a pure cost-minimization input. The only number that matters for the declaration is my heaviest crate; everything else is noise.

I do not let my current point lead or deficit change either decision. The math of declaration and route is stateless — it depends only on my current crates, not on where I stand.

**Warnings (errors I have made before and must not repeat):**
- Do not declare my full hold total "to be safe" or "to justify" the number. The spot check compares my declaration to my heaviest crate only; declaring the total is pure waste.
- Do not take night when the duty savings are less than half my smallest crate's value. The sacrificed crate is real points lost; the duty saving is a small fraction.