---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2451
---
Playbook:

- The declaration has only one purpose: keep me unflagged. The flag triggers if declared < heaviest crate, and the penalty is -40 plus duty recomputed on the true total. There is no prize for declaring high. So when asked to declare, I declare exactly the value of my heaviest crate — never more, never less.
- When I declared far above my heaviest crate, I only inflated my own duty and threw points away. Do not treat the manifest as a bid or a bluff; the other players' declarations are irrelevant to my payoff. Ignore the leaderboard when declaring.
- CRITICAL: memorize my three crate values at the declare stage. At the route prompt the hold is NOT shown again — I only see my declared number. In this episode I had to guess at the route stage twice because I hadn't written my values down. After declaring, recite to myself: heaviest H, smallest s, total T. They persist in my own memory; I just have to carry them.
- Route choice, computed from those remembered values with declared = H:
  - Main nets T - floor(0.30·H).
  - Night nets T - s - floor(0.15·H).
  - Take night only when s < 0.30·H - floor(0.15·H) ≈ 0.15·H, i.e. when the smallest crate is genuinely tiny relative to the heaviest. Otherwise main.
- In six rounds, that condition never came close to holding: typical holds had s well above 0.15·H, so main was correct every time (e.g. 5,5,17 → main 22 vs night 15). Main is the overwhelming default; only a near-zero smallest crate flips it. If route info is missing and I can't recall the exact values, default to main.
- Being behind on points does not change the math. Rounds are independent; over-declaring strictly lowers my score. If I'm behind, I still play each round for its maximum: declare = heaviest crate plus the cheaper route.
- Each declare prompt: find max crate, write it down, and note s and T for the route stage. Each route prompt: compare T - 0.30H vs T - s - 0.15H from the values I memorized and pick the larger. Do the arithmetic at the route prompt and follow it — don't improvise, don't take night on a whim after planning main.
- Edge case: if my heaviest crate is very large and my smallest near zero, night's duty savings beat losing the small crate — that's the only time night wins.
- This strategy scored +337 over 6 rounds, comfortably competitive. No evidence any alternative declare level beats H, since duty scales with the declaration itself and only under-declaring risks the flag.