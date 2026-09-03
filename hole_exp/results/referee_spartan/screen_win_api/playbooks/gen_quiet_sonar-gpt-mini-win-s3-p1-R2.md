---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 2362
---
When asked to hide, I pick a cell among those with the lowest recent public fire frequency (count every player's fired cells from completed rounds) — hide at one of those lowest-frequency cells.

When multiple cells tie for lowest recent fire frequency, I choose one uniformly at random among them.

I avoid repeatedly hiding in the same cell across rounds (if the same cell remains lowest-frequency, I will still occasionally rotate among tied lowest cells) to reduce predictability.

When deciding hides, I use only public information (other players' fired cells and their claims); true hides are private and not available. I treat claimed results as factual because the rules require claims to match the private result.

When behind on points versus my immediate attacker (the player who fires at me), I bias my hide selection toward cells that that attacker has fired at less frequently; when ahead, I bias hides away from cells that the lowest-scoring players fire at more often. These biases are mild and apply only when frequencies give a clear preference.

When asked to fire at my fixed target, I use public fire-frequency data as a proxy for that player's likely hides: if a specific cell has been fired at by others and shows a nonzero elevated frequency as a likely hide spot for my target, I prioritize firing that cell. If there is no informative frequency (all cells similar or no relevant data), I choose uniformly at random among 1–9 to avoid predictable patterns.

If I am far behind on score (target advantage ≥ 4 points), I switch to high-aggression: concentrate more on the single most-likely cell for the target (highest estimated frequency) rather than randomizing.

If I am comfortably ahead (my lead ≥ 4), I diversify my fires — avoid repeatedly firing the exact same cell — to conserve uncertainty and avoid creating obvious countermoves.

When frequencies are inconclusive or noisy, prefer a uniform fallback to avoid exploitable patterns.

I continuously update frequency estimates after every public-fire event and use those updated estimates for the next hide and fire decisions.

Always claim exactly the referee’s private result; claims are constrained by the rules and therefore truthful.

Do not assume opponents will voluntarily deviate from rule-mandated truthful claims; use claims and public fires as the only reliable data.