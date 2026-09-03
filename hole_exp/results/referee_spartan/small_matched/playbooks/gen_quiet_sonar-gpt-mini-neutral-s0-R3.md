---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 0
round: 3
chars: 5952
---
I will always truthfully claim the private hit/miss result the referee gives me; claims are forced to match truth and are reliable signals from others.

When hiding, I will avoid repeating the same exact cell across consecutive rounds; instead I will rotate hides among different thirds (low 1–3, mid 4–6, high 7–9) to reduce predictability.

When hiding, if a cell has been heavily probed by multiple players across recent rounds (3+ fires), I will not hide there; I prefer low-frequency cells opposite the recent cluster unless that opposite side is itself heavily probed.

When opponents concentrate probes on a small cluster without public hits, I will treat it as ambiguous (could be safe bluffs or real hides). I will bias my hide to the opposite side but occasionally revisit low-frequency cells in the clustered area only after several rounds without heavy probing.

When hiding and I am leading on points, I will bias toward conservative low-frequency cells (away from clusters) to minimize giving others easy targets; when trailing, I will be more willing to take riskier hides that might induce opponents to mis-target.

When firing at my fixed target, I will not repeat the same cell every round; instead I will rotate among a set of 3–4 candidate cells spread across the board to probe multiple hypotheses and reduce predictability.

When firing, I will deprioritize firing a cell that just recorded a public hit on my target this round (public hits are truthful and indicate that cell was the target that round); I will assume the target often moves after being hit, so treat a recently hit cell as lower probability next round unless patterns show repetition.

When multiple players repeatedly fire the same cell and only misses result, I will avoid persistently chasing that cell; I will probe it occasionally to test whether it becomes positive, but I will switch to other candidates after repeated misses.

When my personal repeated shots at a given cell yield misses, I will drop that cell from my shortlist and replace it with a new candidate rather than persisting.

After every round I will update probabilities for my target’s likely hide cells using only public information (fired cells and their claimed hit/miss outcomes) plus my private shot result; because claims must match private results, public hits are reliable data points.

When I see an opponent consistently scoring hits on a particular position across rounds, I will treat that position as a strong indicator of their hiding preference for the immediate subsequent round and deprioritize firing it until evidence of a move appears.

When I see many players firing the same small set of cells, I will assume at least one is probing correctly and at least one is probing by crowd behavior; I will split my probes between occasionally testing the cluster and probing opposite low-frequency cells.

When behind in score, I will increase variance in firing (probe less-targeted cells, rotate more aggressively) because successful hits are high reward (+4) and I need to change the distribution to catch up.

When ahead or tied, I will favor steadier strategies: conservative hides (low-frequency cells opposite clusters) and methodical probing of probable candidate cells rather than high-variance gambles.

I will deliberately avoid overusing the central cells (4–6) for hides, since opponents tend to probe them heavily; instead I will cycle through thirds so opponents cannot lock onto a single region.

If multiple players hit the same cell on the same round (i.e., several public hits on X against the same player), I will infer that cell was that player's hide and that they are likely to move next round; I will deprioritize it in my immediate next fire and consider probing adjacent or opposite cells.

I will not rely on deception in claims (the rules prevent lying). My inferences will be based on patterns of fired cells and public hit/miss outcomes plus my private results.

I will maintain a dynamic shortlist of candidate fire cells for my target: keep 3–4 active candidates; promote a candidate if a different player records a hit there (but demote immediately next round), demote candidates after repeated misses, and replace with less-probed cells opposite current clusters.

If an opponent’s behavior changes (e.g., they stop probing a cluster or begin probing a new cell repeatedly), I will treat that as soft evidence they moved and adapt hides/fires accordingly rather than assuming consistency.

When opponents show consistent clustering behavior (repeat the same probe every round), I will exploit it by hiding opposite that cluster and occasionally probing their favored cell if it looks like they are likely to repeat.

When choosing hides late in the game (last 1–2 rounds), I will weigh risk differently: if winning, hide conservatively; if losing, hide in spots that are least expected based on prior rounds (including previously used cells if opponents have stopped checking them).

I will document and act on short-term streaks: if a cell has been fired 2+ times by different players with a hit reported, mark it as “recently used” and deprioritize for the next round; if a cell has 3+ misses across players, mark it as low-likelihood and remove it from my candidate list for a few rounds.

I will prefer to probe cells that have low public probe frequency unless there is a direct public hit signal to the contrary; this balances discovery value vs. crowd-following.

I will keep my hide choices unpredictable across games by rotating thirds and occasionally revisiting older cells only after at least two rounds of non-probing; I will avoid simple deterministic sequences (e.g., always 1, then 2, then 3).

I will treat public hits as the strongest signal, public misses as weak negative evidence (one miss is weak; many misses are stronger), and other players’ fire choices as neutral-to-informative depending on repetition and context.