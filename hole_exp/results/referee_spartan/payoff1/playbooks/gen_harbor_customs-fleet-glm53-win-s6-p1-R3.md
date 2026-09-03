---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 2960
---
My playbook for harbor customs:

- The only rule that matters at declare: the spot check flags me if my declared value is below my HEAVIEST crate. So the floor for any declaration is my max crate's value. I always declare exactly the max crate value — never more. Declaring the full total or "close to actual" just inflates my duty for zero safety benefit. Six rounds of declaring max-crate produced zero flags and a final score of +329 — this rule held up perfectly.

- The spot check depends only on the declaration, not on the route, so the route choice never affects flag risk.

- CRITICAL, and my main failure this session: I DO know my own crate values at route time — they were shown to me at the declare stage of the same round. Every single round I wrote "no crate details given / can't verify the smallest-crate condition" and defaulted to main. That is wrong: I always had the information, I just didn't carry it forward. Before answering any route prompt, re-read my hold from that round's declare screen (e.g. round 5: 16, 18, 29 → smallest 16 vs 0.15×29 ≈ 4.35 → main was actually right, but I got there by luck, not by doing the math). Next time: write my three crate values in the reasoning line at route stage, then compute.

- Route arithmetic, with declared = max crate M, total T, smallest crate m:
  - main: T − 0.30·M
  - night: T − m − 0.15·M
  Take night when m < 0.15·M (roughly m/M < 0.15). Take main otherwise. Don't pick routes on "aggressiveness," narrative, or a "safe main default" — pick by this arithmetic every time. With typical crate values (m often 15-30, M often 22-40), main is usually correct, which is why my lucky default mostly matched the math — but I must verify, not assume, because a hold like (3, 10, 38) flips the answer.

- Don't let score position change the plan. Being ahead (I led or trailed Odalie most of the game) never changes the per-round optimum — the game is a sum of independent rounds. The declare number has exactly one job (cover the max crate at minimum cost) and the route choice follows the ratio above.

- Never declare below my max crate to save duty: the -40 penalty plus duty recomputed at 0.30 × true total dwarfs any duty saving.

- Never declare above my max crate either: opponents' inflated declarations (38, 40, 37) gained them nothing against the spot check and cost them extra duty.

- Opponents' declarations, routes, and the running score are noise for my decision — my round is independent of theirs. The history lines in the prompt are useful only to confirm scoring behaves as expected; ignore them when choosing.

- Summary decision: at declare, note my three crate values on paper/memory, then [declare: max crate]. At route, restate those same values, compute 0.15 × max crate, and [route: night] if smallest crate is below that threshold, else [route: main]. The single biggest improvement available to me is simply executing the route step with the data I already hold.