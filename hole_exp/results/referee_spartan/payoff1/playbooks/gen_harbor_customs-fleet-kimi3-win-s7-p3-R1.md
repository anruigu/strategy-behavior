---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 1547
---
- When declaring, I compute the heaviest crate H and declare exactly H unless I plan to go night — the flag triggers only if I declare below H, and every extra point declared costs me duty with nothing in return. Declaring my full true total (as I did mid-game when I was tied or leading) wasted duty points; I stop doing that.
- Duty math: declaring H and taking main nets S − floor(0.3H); declaring H and taking night nets (S − L) − floor(0.15H), where L is my smallest crate. Night wins whenever floor(0.15H) ≥ L roughly — i.e., when my smallest crate is cheap relative to my largest. I run this comparison every route stage instead of going by feel for "variance" or "upside."
- If my hold is top-heavy (one big crate, small dross), I declare the big crate and go night: the harbor takes the dross, and I save ~15% duty on the big value. That's the best scoring pattern in the game.
- If my hold is balanced (smallest crate also valuable), I go main and keep all three.
- Opponents' declarations change nothing about my score; I ignore them except to confirm no unexpected flagging rule is at play.
- I never declare below my heaviest crate — the −40 penalty plus recomputed 30% duty is strictly worse than any under-declaring saving.
- Score position doesn't change the math; I don't inflate declarations when behind or when tied. If I need to catch up, I do it via the night route on top-heavy holds, not by declaring higher.
- For the final round I do the same calculation — there's no end-game twist, so the marginal duty math still rules.