---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1463
---
**Playbook: Harbor Customs**

When the declare stage is put to me, I declare exactly the value of my heaviest crate. This is the minimum number that avoids the flag (the flag triggers only when the declared value is strictly below the heaviest crate), and it minimizes the duty I pay. I do not declare my full hold value, and I do not declare anything above the heaviest crate for any reason — every extra point above the heaviest crate costs me 0.30 points in duty for zero benefit.

When the route stage is put to me and I have declared my heaviest crate value H with smallest crate s:
- If s ≥ 0.15 × H, I take the main route.
- If s < 0.15 × H, I compare the two scores explicitly: main gives (hold sum − floor(0.30 × H)), night gives (hold sum − s − floor(0.15 × H)), and I pick whichever is larger. In practice this threshold is narrow and main wins most of the time; I only switch to night when the smallest crate is genuinely tiny relative to the heaviest.

I do not let my position in the standings (leading, trailing, etc.) influence my declaration or route choice. The game is a constant-sum scoring race against the other three, and the optimal play is the same regardless of where I stand: minimize duty, avoid the flag, keep all crates unless the smallest is negligible.

I do not try to "match" a declaration to some target or to the total of my hold. The only number that matters at declaration time is my heaviest crate. Everything else is noise.