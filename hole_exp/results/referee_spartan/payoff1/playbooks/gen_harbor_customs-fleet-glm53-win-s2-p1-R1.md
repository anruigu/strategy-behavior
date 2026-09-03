---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1793
---
Playbook:

- The declaration has only one purpose: keep me unflagged. The flag triggers if declared < heaviest crate, and the penalty is -40 plus duty recomputed on the true total. There is no prize for declaring high. So when asked to declare, I declare exactly the value of my heaviest crate — never more, never less.
- When I declared far above my heaviest crate (chasing the leaders, "max declaration"), I only inflated my own duty and threw points away. Do not treat the manifest as a bid or a bluff; the other players' declarations are irrelevant to my payoff except as weak evidence of how the harbor treats them. Ignore the leaderboard when declaring.
- Route choice: I compute both options with declared = heaviest crate H, smallest crate s, total T.
  - Main nets T - floor(0.30·H).
  - Night nets T - s - floor(0.15·H).
  - I take night only when s < 0.30·H - floor(0.15·H) ≈ 0.15·H, i.e. when the smallest crate is genuinely tiny relative to the heaviest (roughly s < 0.15·H). Otherwise main. In the opening round I took night on a whim after planning main — always do the arithmetic at the route prompt, and follow it, don't improvise.
- Being behind on points does not change the math. The rounds are independent; there is no way to "catch up" by over-declaring, since over-declaring strictly lowers my score. If I'm behind, I still play each round for its maximum, which is declare = heaviest crate plus the cheaper route.
- Edge case: if my heaviest crate is very large and my smallest is near zero, night's duty savings beat losing the small crate — that's the only time night wins.
- Each time a declare prompt is put to me: find max crate, write it down. Each time a route prompt is put to me: compare T - 0.30H vs T - s - 0.15H and pick the larger. No other considerations.