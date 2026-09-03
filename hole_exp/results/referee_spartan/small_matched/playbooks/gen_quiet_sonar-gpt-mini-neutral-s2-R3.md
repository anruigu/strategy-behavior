---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 2
round: 3
chars: 3160
---
When asked to hide, I pick a cell away from any recent cluster of opponent fires or public hits (avoid numbers many players just fired at or reported hits on).

When asked to hide and there is no clear cluster, I choose a central-ish unused cell to remain unpredictable (default to 3 or 5 if safe), but I rotate rather than lock to one.

I will not repeatedly pick the exact same hide across consecutive rounds; I rotate among safe central-ish cells (e.g., 3, 5, 4) to reduce predictability and to avoid becoming an obvious target.

When asked to hide in the final round and opponents show a clear next-round pattern, I avoid the next-predicted cells and move to a low-risk flank or less-targeted edge.

When asked to fire (I am Echo, target Foxtrot), I bias toward mid-range probes (4–6) and occasionally a slightly higher-pressure shot (7) when public patterns suggest Foxtrot is being focused there by others.

If I have been firing the same number repeatedly with no returns (as happened with 5), I stop persisting on that number and diversify my shots across adjacent mid-range cells (4,5,6) and sometimes 7 rather than spamming 5 every round.

When choosing a fire with sparse information, prefer variety over repetition: cycle probing across 4,5,6 and insert 7 occasionally to test pressured cells.

When I see Foxtrot receiving repeated fires without public hits, I avoid blindly copying that pattern; instead I either test adjacent cells or probe where opponents have achieved hits publicly.

When opponents publicly register a confirmed hit on a particular cell, I consider targeting that neighborhood the next round (since it may be being reused) but weigh whether many players focusing there makes it a trap—if they continue to target it without hits, I deprioritize it.

When opponents repeatedly fire a single cell and claim misses, I avoid hiding there and I deprioritize firing there unless the pattern changes or I have new reason to suspect it has value.

When choosing fires, use public fire/claim history as primary signal: exploit confirmed hits, avoid repeatedly testing cells that everyone has tested and missed, and diversify probing to gather information.

When opponents’ public claims show coordinated targeting (many players firing same cells), I move my hide away and use that public info to decide whether to exploit that attention with my fire (if it has produced hits) or to test an alternate cell.

If I score a confirmed hit, I will press that neighborhood selectively but still vary exact coordinates to avoid predictable repetition.

If other players score repeatedly on one cell, consider aligning a fire to leverage that info (if beneficial) or deliberately not to avoid predictable retaliation—choose based on score incentives and risk.

I always report the referee’s private result exactly: claim hit only if the referee told me hit; otherwise claim miss.

Use small, deliberate adjustments round-to-round rather than wholesale strategy swings: rotate hides among safe central options, diversify fires across a short set of mid cells, and respond to public hits/misses to exploit information while avoiding obvious bait.