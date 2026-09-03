---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1357
---
**Playbook**

When asked to declare, I declare exactly the value of my heaviest crate. Nothing more. The spot check only flags me if my declaration is below my heaviest crate, so anything above that is pure duty cost with zero benefit. I never declare my total hold value.

When asked to route, I compute: does floor(0.30 × my declared) − floor(0.15 × my declared) exceed the value of my smallest crate? If yes, I take night. If no, I take main. In practice this means I take main unless my heaviest crate is roughly 7× or more my smallest crate, which will be rare.

I do not use my declaration as a signal, a bluff, or a statement of confidence. It is a pure cost-minimization input. The only number that matters for the declaration is my heaviest crate; everything else is noise.

I do not let my current point lead or deficit change either decision. The math of declaration and route is stateless — it depends only on my current crates, not on where I stand.

**What did not work:** I repeatedly declared my full hold total (or close to it) when declaring only my heaviest crate would have saved me 7–18 points per round. I also took the night route in my final round when the duty savings were less than half the value of my sacrificed crate. Both errors came from treating the declaration as something to "justify" rather than as a number to minimize.