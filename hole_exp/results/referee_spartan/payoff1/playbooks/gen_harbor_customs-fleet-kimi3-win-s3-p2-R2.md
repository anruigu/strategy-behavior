---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 1988
---
My playbook for Harbor Customs:

- At declare, always declare exactly the value of my heaviest crate — the minimum safe number. The flag only checks against the heaviest single crate, and every point of declaration above that costs 30% in duty (main) for zero benefit. Never declare the honest total; never declare below the heaviest crate (the -40 penalty plus recomputed duty is strictly worse than any saving).

- I know my exact hold, so the night decision is pure arithmetic, not a guess: night beats main only when my smallest crate is strictly less than the duty saved, which is 0.15 × my declared value (main duty 0.30d vs night duty 0.15d). Since I declare my heaviest crate h, take night only when smallest < 0.15h. This episode I broke this rule in round 2: hold {11,13,29}, I took night saving ~4.4 in duty while sacrificing an 11-point crate — a straight loss. Never "assume" the hold is lopsided; the numbers are on the manifest.

- Quick formula per round: main score = total − 0.3h; night score = (total − smallest) − 0.15h. Pick whichever is bigger. Night needs a very lopsided hold (h more than ~6.7× the smallest crate), which is rare, so default main.

- Do this arithmetic every round and act on it immediately — when a truly lopsided hold appears (one big crate, two near-worthless ones), that is my night round: declare the big crate, pay the tiny duty, dump the junk crate. Don't wait for it while it costs me.

- Ignore others' scores when declaring. Declaration is pure cost; being behind is fixed by minimizing my own duty, not by matching anyone's numbers. The check is mechanical, so no bluffing, camouflage, or "modesty" around the minimum safe value — declare h exactly, every round.

- Verify my rival-reading priors: this episode, rivals declaring 34-45 were likely doing the same minimum-safe play, and them occasionally flagging (e.g., a 17 flag) shows others sometimes gamble below the floor — it punished them, confirming the rule, not challenging it.