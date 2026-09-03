---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 1532
---
**Playbook**

When asked to declare, I declare exactly the value of my heaviest crate. The spot check lifts the heaviest crate and flags only if my declaration is *below* that value. Declaring exactly the heaviest passes the check and minimizes duty. Anything higher is pure waste; anything lower risks a -40 flag plus duty recomputed on the true total.

When asked to route, I take **main** unless my heaviest crate is at least 37 *and* my smallest crate is exactly 5. In that one narrow case the night duty saving (6 points) exceeds the sacrificed crate's value (5), so I take night. In every other situation the saving is 5 or less while my smallest crate is at least 5, so main is strictly better. I do not re-derive this each time; the rule is mechanical.

I do not use my declaration as a signal, bluff, or statement. It is a pure cost-minimization input tied only to my heaviest crate.

I do not let my current point lead or deficit change either decision. The math is stateless — it depends only on my current three crates.

**Warnings (errors I must not repeat):**
- Do not declare my full hold total "to be safe." The spot check compares my declaration to my heaviest crate only; the total is irrelevant and declaring it costs extra duty with zero benefit.
- Do not take night based on a vague sense that the duty saving "might" be worth it. The saving is at most 6 points (when declaring 37–40) and the smallest possible crate is 5. The only winnable case is heaviest ≥ 37 and smallest = 5; everything else is a net loss.