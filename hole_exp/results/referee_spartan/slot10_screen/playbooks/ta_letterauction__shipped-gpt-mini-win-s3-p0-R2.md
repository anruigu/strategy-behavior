---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 4490
---
When a letter is presented, I first ask: can this letter plausibly help me form any lexicon word given letters already owned and remaining auctions? If no, bid 0.

When a letter is required to complete at least one plausible target word (considering remaining letters), I bid up to the marginal value: estimate benefit = 2 * letter value if it lets me make the word (or contributes to a plan to make a higher‑value word); compare that benefit to keeping the coin as 1 point. Only bid more than 1 coin when the expected incremental increase in my final score exceeds the extra coins spent.

When a letter has value 3 (or is unusually high relative to others), treat it as premium: be willing to spend several coins because it can be worth double (e.g., 6 points) in a completed word. However, do not overpay beyond the marginal gain relative to my alternate plan of keeping the coins. If an opponent contests a premium aggressively, re-evaluate whether I can assemble a valid word around it; if not, concede rather than burn coins chasing it.

When multiple cheap vowels/consonants are needed to form a realistic word, spend small amounts (1–2 coins) to accumulate them early, but cap cumulative spend so it does not exceed the increase in expected final word score. If I find myself owning only a singleton low‑value letter near the end, I prefer keeping coins to having that singleton.

When trailing on coins late in the auction, avoid throwing coins at singletons that don't complete a word; conserve to score coins directly.

When a tie will leave a letter unsold and I don't need it badly, prefer a low bid that risks a tie rather than overpaying to win; sometimes letting a letter go unsold is better than overpaying for a marginal improvement. Conversely, when winning the letter directly blocks the opponent from completing a high-value word, invest up to the marginal gain to prevent them.

When bids so far are uniformly tiny, assume opponents are conserving; don't reflexively bid 1 on every letter—choose only those that fit a plan. Bidding 1 on many letters without a coherent plan wastes opportunities to contest critical letters.

After the last auction, I only submit a word if I can legally spell something in the lexicon. Calculate final score as 2 * sum(letter values used in the submitted word) + remaining coins. Only buy letters if they increase this final total compared to leaving them as coins.

When I have a near-complete set for a high-scoring word, be more aggressive: outbid modestly to secure missing letters because completing the word often outperforms holding coins. But before committing, confirm I have enough coins and upcoming auctions (or current letters) to realistically complete that target.

When uncertain between two possible target words, prioritize the one requiring fewer additional buys, the one that uses high-value letters I already own, or the one with a higher expected marginal gain per coin spent.

When an opponent consistently bids slightly more than me, re-evaluate whether they are assembling a word; avoid matching small raises unless it blocks them from completing a high-value word or gives me a clear path to a better final score.

Always keep a running count: coins remaining versus number of letters still coming and letters needed to complete any target word; if coins are insufficient to buy required letters, abandon that plan and conserve.

Revise plans dynamically based on revealed opponent behavior in the same auction: if the opponent buys a letter pattern (vowel/consonant mix) that signals a specific target, shift to blocking or to an alternate target that is still viable and affordable.

Practical heuristics reinforced by play:
- Low-value vowels (1) are worth small early bids (1) only if they clearly enable a plan; otherwise leave them.
- Premium letters (3) merit larger bids but cap at the marginal score gain (e.g., if a 3 is necessary to complete a 6‑point word, spending more than 5 coins is rarely justified).
- Avoid buying a single 1‑value letter late unless it completes a legal word; the coin kept is often more valuable.
- If I repeatedly end up with only one small letter, prefer bidding 0 on marginal auctions and secure coin points; buying opportunistically without a plan loses value.

I will use these rules to guide sealed bids: default 0 unless the letter is part of a concrete plan in which case bid the minimum needed to make its marginal expected payoff positive versus keeping the coin.