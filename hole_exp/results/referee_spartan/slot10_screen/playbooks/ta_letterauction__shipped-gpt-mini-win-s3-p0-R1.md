---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 2765
---
When a letter is presented, I first ask: can this letter plausibly help me form any lexicon word given letters already owned and remaining auctions? If no, bid 0.

When a letter is required to complete at least one plausible target word (considering remaining letters), I bid up to the marginal value: estimate benefit = 2 * letter value if it lets me make the word (or contributes to a plan to make a higher‑value word); compare to keeping coins as 1 point each. Only bid more than 1 coin when the expected incremental increase in final score exceeds 1 coin.

When a letter has value 3 (or unusually high relative to others), treat it as premium: be willing to outbid by several coins because it can double to 6 points in a word. If an opponent shows willingness to contest premium letters, prioritize winning at least one premium if it enables a real word.

When multiple cheap vowels/consonants are needed to form a realistic word, spend small amounts (1–2 coins) to accumulate them, but stop if cumulative spend approaches the value of coins-as-points (i.e., don't spend more than the increase in final word score you'd gain).

When trailing on coins late in the auction, avoid throwing coins at singletons that don't complete a word; conserve to score coins directly. I learned that buying a single low‑value letter without the rest yields worse outcomes than keeping coins.

When tie will leave a letter unsold and I don't need it badly, prefer a low bid that risks a tie rather than overpaying to win.

When I have a near-complete set for a high-scoring word, be aggressive: outbid modestly to secure missing letters because completing the word doubles the letters' value and often beats holding coins.

When bids so far have been uniformly tiny, assume opponents are conserving; don't reflexively bid 1 on every letter—choose only those that fit a plan. Bidding 1 on many letters without a plan wastes opportunities to contest critical letters.

After the last auction, I only submit a word if I can legally spell something from the lexicon. Calculate final score: 2 * sum(letter values used) + remaining coins. Only buy letters if they increase this final total compared to leaving them as coins.

When uncertain between two possible target words, prioritize the one requiring fewer additional buys or one that uses high-value letters already owned.

When an opponent consistently bids slightly more than me, re-evaluate whether they are assembling a word; avoid matching small raises unless it blocks them from completing a high-value word.

Always keep a running count: coins remaining versus number of letters still coming and letters needed to complete any target word; if coins are insufficient to buy required letters, abandon that plan and conserve.