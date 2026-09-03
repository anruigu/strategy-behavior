---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 1841
---
Playbook:

- The spot check only compares my declared value against my single heaviest crate, not the whole hold. So the cheapest safe declare is exactly my largest crate value — never more.
- When the declare stage is put to me, I declare exactly the value of my biggest crate. Anything above that just inflates my duty; anything below risks the -40 flag plus duty at 0.30 × the true total. Over-declaring near my full total was pure loss — it bought nothing in safety and cost extra duty.
- When the route stage is put to me, I take main, always. Compare by arithmetic, not feel: main scores (total − 0.30 × largest); night scores (total − smallest − 0.15 × largest). Night only wins when my smallest crate is worth less than 0.15 × my largest — rare with 5-40 crates, and it never paid off across six rounds here. I ran main every round and lost nothing to confiscation or flags.
- This policy never flags and never forfeits, so my per-round score is fully determined: total of my three crates − floor(0.30 × largest). That is the floor strategy; do not deviate for "upside."
- Ignore the scoreboard when choosing declare and route. Position does not change the arithmetic. In this episode I stayed second throughout with no gambling and finished strong (+346).
- Ignore rivals' declarations and routes. They carry no information that changes my own optimal play — Mirren's night routes and odd declares were noise.
- Watch for ties: with duplicate crates (e.g. 7, 30, 30), the heaviest is either one, so declaring that value is still exactly safe.
- If the rules ever differ from this setup (different confiscation, different check, different confiscation rule on night), re-derive from scratch: minimize the declare subject to passing the check, then compare routes by writing out each route's exact score formula and taking the larger.