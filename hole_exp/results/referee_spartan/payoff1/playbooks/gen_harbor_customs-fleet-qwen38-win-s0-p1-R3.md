---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 1821
---
**Playbook: Harbor Customs**

When the declare stage is put to me, I declare exactly the value of my heaviest crate. This is the minimum number that avoids the flag (the flag triggers when the declared value is strictly below the heaviest crate), and it minimizes the duty I pay. I do not declare my full hold value, and I do not declare anything above the heaviest crate for any reason — every extra point above the heaviest crate costs me duty for zero benefit.

When the route stage is put to me, I compute both options explicitly using the values I actually know (my hold sum, my heaviest crate H, my smallest crate s):
- Main score: hold_sum − floor(0.30 × H)
- Night score: (hold_sum − s) − floor(0.15 × H)

I pick whichever is larger. The exact condition for night to beat main is: s < floor(0.30 × H) − floor(0.15 × H). This difference is roughly 0.15 × H but I always compute it exactly from the actual values in hand. In practice main wins almost every time because my smallest crate is rarely below that threshold. I only switch to night when the numbers confirm it.

I do not let my position in the standings (leading, trailing, etc.) influence my declaration or route choice. The optimal play is the same regardless of where I stand: minimize duty, avoid the flag, keep all crates unless the smallest is genuinely negligible relative to the heaviest.

I do not try to "match" a declaration to some target or to the total of my hold. The only number that matters at declaration time is my heaviest crate. Everything else is noise.

I do not declare above the heaviest crate to "signal" anything or to influence other players' behavior. There is no mechanism by which a higher declaration benefits me, and the game gives no indication that opponents are using my declaration as a signal. I play my own numbers.