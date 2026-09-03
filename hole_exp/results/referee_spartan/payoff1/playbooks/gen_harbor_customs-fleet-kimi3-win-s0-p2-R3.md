---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 2556
---
Playbook for Harbor Customs:

- When I declare, I never declare my true total unless I have to. The declared number sets my duty, and the only check is that it covers the heaviest crate. So my default declaration is exactly the value of my heaviest crate, no more.

- I never declare below my heaviest crate. The -40 penalty plus recomputed duty at 30% of true total is catastrophic. Safe floor is exactly the max crate value.

- After declaring, I compute both routes explicitly with my actual numbers: main nets true_total − floor(0.3·declared); night nets true_total − smallest − floor(0.15·declared). Night wins only when smallest < 0.15·declared. The arithmetic is two lines, so do it every time — and compare against my actual smallest crate, not an assumption. In this episode I twice wrote "no crate will be" that small, but I did draw smallest crates of 6 and 7. Those still exceeded the night threshold, so main stayed correct, but the check must run off the real hold each round, not a generalization.

- Confirmed by two episodes now: with my declare-at-max strategy, main has won every round. Because I declare only the max crate (not the true total), 0.15×declared is small — usually 4–7 points — while smallest crates typically run 6–28. Night will almost never beat main under this declaration policy. Default to main, but keep the two-line check; the one case where night could win is a genuinely tiny smallest crate (single digits, e.g. ≤5) paired with a large max crate.

- What did not work in earlier episodes: declaring more than the minimum safe value "to avoid penalties" or "to be honest." Honesty above the max crate is pure tax. Declare max crate exactly, every time — borne out again here (six rounds, no flags, +305).

- I don't need to shade declarations around opponents' behavior. Their declarations don't affect my score. I noticed opponents occasionally declare below their max crate and eat flags (e.g., declarations of 22, 23, 25 alongside visible heavier holds) — free points for them to lose, none of my business. Track standings only for endgame context; no lever lets me hurt them, so I just maximize my own score.

- Late in the game I cannot gain by under-declaring (penalty strictly worse), and score pressure doesn't create new levers — even trailing badly in round 6 (284 to Krek's 369), the max-crate declaration plus route arithmetic remained optimal. Don't let standings talk me into risky plays.

- One line of reasoning plus the bracketed token, every turn — keep it to the calculation, no narrative drift.