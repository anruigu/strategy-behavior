---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1667
---
Playbook:

- The spot check only compares my declared value against my single heaviest crate, not the whole hold. So the cheapest safe declare is exactly my largest crate value — never more.
- When the declare stage is put to me, I declare exactly the value of my biggest crate. Anything above that just inflates my duty; anything below risks the -40 flag plus duty at 0.30 × the true total. My earlier over-declaring (declaring near my full total) was pure loss — it bought nothing in safety and cost extra duty.
- When the route stage is put to me, I take main, always. Night's duty saving (0.15 vs 0.30) on a minimal declare of my biggest crate is almost always smaller than the crate I forfeit. Losing my smallest crate to save floor(0.15 × largest) only wins when the smallest crate is worth less than that — rare, and it never paid off for me. Only consider night if my smallest crate is tiny (roughly under half my largest) and even then it's marginal.
- Ignore the scoreboard when choosing declare and route. Position does not change the arithmetic — the leading/trailing considerations that pushed me into aggressive declares were noise. Score maximization each round is the same regardless of standing.
- Ignore rivals' declarations too. They carry no information that changes my own optimal play.
- Per-round expectation under this policy: I keep all three crates, pay duty of floor(0.30 × largest crate). That is the floor strategy; do not deviate.
- If the rules ever differ from this setup (different confiscation, different check), re-derive: minimize declare subject to passing the check, then compare routes by arithmetic, not by feel or by "upside."