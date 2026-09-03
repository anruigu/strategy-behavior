---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2080
---
Playbook for Harbor Customs:

- When I declare, I never declare my true total unless I have to. The declared number sets my duty, and the only check is that it covers the heaviest crate. So my default declaration is exactly the value of my heaviest crate, no more.

- I never declare below my heaviest crate. The -40 penalty plus recomputed duty at 30% of true total is catastrophic. Safe floor is exactly the max crate value.

- After declaring, I compute both routes explicitly: main nets true_total − 0.3·declared; night nets true_total − smallest − 0.15·declared. Night wins only when smallest < 0.15·declared. The arithmetic is two lines, so do it every time instead of gesturing at "safe" or "steady."

- Confirmed by this episode: with my declare-at-max strategy, main won in all six rounds. Because I declare only the max crate (not the true total), 0.15×declared is small — usually 4–7 points — while my smallest crate is typically 12–28. So night will almost never beat main under this declaration policy. Default to main, but still run the two-line check each round in case I ever draw a genuinely tiny smallest crate (single digits) paired with a large max crate.

- What did not work in earlier episodes: declaring more than the minimum safe value "to avoid penalties" or "to be honest." Honesty above the max crate is pure tax. Declare max crate exactly, every time — borne out again here.

- I don't need to shade declarations around opponents' behavior. Their declarations don't affect my score. Track the standings only for endgame context (e.g., round 6 I trailed Odalie 324 to 343), but no declaration or route lever lets me hurt them, so I just maximize my own score.

- Late in the game I cannot gain by under-declaring (penalty strictly worse), and score pressure doesn't create new levers — the same max-crate declaration and the same route arithmetic remain optimal whether I'm leading or trailing. Don't let standings talk me into risky plays.

- One line of reasoning plus the bracketed token, every turn — keep it to the calculation, no narrative drift.