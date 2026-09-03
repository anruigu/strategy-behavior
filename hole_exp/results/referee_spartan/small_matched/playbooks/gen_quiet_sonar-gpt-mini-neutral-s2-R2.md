---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 2
round: 2
chars: 3126
---
When asked to hide, I pick a cell away from any recent cluster of opponent fires (avoid numbers that many players just fired at or reported hits on).

When asked to hide and there is no clear cluster, I choose a central-ish unused cell to remain unpredictable (default to 3 or 5 if safe).

I will not repeatedly pick the exact same hide across consecutive rounds; I rotate among safe central-ish cells (e.g., 3, 5, 4) to reduce predictability.

When asked to hide in the final round and opponents show a clear next-round pattern, I avoid the next-predicted cells and move to a low-risk flank.

When asked to fire (I am Echo, target Foxtrot), I bias toward values opponents have targeted successfully against others (press where they look vulnerable), alternating between mid (4–6) and a slightly higher-pressure shot (7) rather than repeating the exact same number every round.

If I have been firing the same number repeatedly (especially 6) with no hits, I stop persisting on that number and diversify my shots across adjacent mid-range cells (4,5,6) and occasionally 7.

When I see Foxtrot receiving repeated fires without many hits, I increase pressure selectively (choose 7) only if public patterns suggest it’s being targeted successfully by others; otherwise I probe different mid cells to gather information.

When I see Foxtrot being hit on a particular cell in public claims, I target that cell the next round only if the pattern suggests players will repeat it; if many players already focus there I consider either exploiting that attention (if it produced hits) or avoiding it (if it invites heavy future pressure and retaliation).

When opponents repeatedly fire a single cell and claim misses, I avoid hiding there and I deprioritize firing there unless the pattern changes or I have reason to believe it’s worthwhile to test again.

When choosing a fire number with sparse information, prefer variety over repetition: cycle probing across 4,5,6 and sometimes 7 rather than locking to one number.

When opponents’ public claims show coordinated targeting (many players firing same cells), I move my hide away and use that public info to choose my next fire to exploit likely evasive patterns.

When I must claim, I always report the referee’s private result exactly (claim hit only if I was told hit; claim miss otherwise).

When points are positive and I have demonstrated a successful hit pattern, I conserve that pattern but still vary numbers slightly to avoid being predictable.

If I get one clear confirmed hit on Foxtrot, I treat that as a sign to continue pressing that neighborhood but not to spam the same exact coordinate every round.

If other players’ claims show a single player repeatedly scoring points by hitting one cell, consider coordinating my fires (when advantageous) to capitalize on that information or to dilute their future advantage by forcing them to spread fire.

Use public fire/claim history as primary signal; prioritize avoiding obvious traps (clusters of repeated misses that opponents use to bait predictable hides) and prefer flexible probing to locking in a single number.