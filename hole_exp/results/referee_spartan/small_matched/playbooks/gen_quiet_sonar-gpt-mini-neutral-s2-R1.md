---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 2
round: 1
chars: 2214
---
When asked to hide, I pick a cell away from any recent cluster of opponent fires (avoid numbers that many players just fired at or reported hits on).

When asked to hide and there is no clear cluster, I choose a central-ish unused cell to remain unpredictable (default to 3 or 5 if safe).

When asked to hide in the final round and opponents show a clear next-round pattern, I avoid the next-predicted cells and move to a low-risk flank.

When asked to fire (I am Echo, target Foxtrot), I bias toward values opponents have targeted successfully against others (press where they look vulnerable), alternating between a mid (5–6) and a slightly higher pressure shot (7) rather than repeating the exact same number every round.

When I see Foxtrot receiving repeated fires without many hits, I increase pressure by choosing the higher-pressure shot (7) that has sometimes produced a decisive hit.

When I see Foxtrot being hit on a particular cell in public claims, I target that cell the next round only if the pattern suggests players will repeat it; otherwise I avoid overfiring a cell that already attracted attention.

When opponents repeatedly fire a single cell and claim misses, I avoid hiding there and I deprioritize firing there unless the pattern changes.

When I must claim, I always report the referee’s private result exactly (claim hit only if I was told hit; claim miss otherwise).

When hiding, I do not repeatedly pick the exact same cell across rounds (that proved predictable and can be exploited).

When choosing a fire number, I prefer balance over extremes if information is sparse (choose 5–6); if I detect an opening or precedent of hits at a particular value, I switch to the pressure shot.

When opponents’ public claims show coordinated targeting (many players firing same cells), I move my hide away and use that public info to choose my next fire to exploit likely evasive patterns.

If my repeated strategy of firing the same number produces no hits, I stop repeating that number and diversify my shots instead of persisting.

When points are positive and I have demonstrated a successful hit pattern, I conserve that pattern but still vary numbers slightly to avoid being predictable.