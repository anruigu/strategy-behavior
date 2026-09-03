---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 4457
---
When a letter up for auction has value V (in word scoring), treat its baseline marginal worth to me as 2*V (because final word scores are 2× letter totals) and do not bid more than 2*V unless capturing that single letter decisively enables a higher‑value word that I can plausibly complete.

When opponents consistently pay X for letters, record X and assume they value completing words. Only overbid an opponent on a letter if (a) winning that letter directly enables me to complete a target word that yields a higher final score than the coins I would spend, or (b) denying that letter prevents an opponent from completing a word that would beat my expected coins-only outcome. If opponents pay ≥ 2*V for a letter, treat that as a red flag to avoid a bidding war unless I have a near-certain plan that justifies matching/exceeding it.

When a high‑value letter (largest V currently relevant to the lexicon) appears, be willing to bid up to 2*V (and in exceptional, well-justified cases slightly above) because such letters swing word totals most. However, only do so if I can reasonably expect to collect the remaining letters needed for a high-scoring word without spending so many coins that the net payoff (2×letters + leftover coins) falls below the baseline of conserving coins.

When I already hold some letters, enumerate candidate lexicon words I could form if I win the current letter. For each candidate word W that becomes feasible by winning this letter, compute:
- word_value = 2 * (sum of letter values of W)
- remaining_coins_if_win = my_coins - bid
- expected_score_if_win = word_value + remaining_coins_if_win
Compare that to the expected score if I do not win (which is typically my_coins if I expect to form no other word). Only place bids that make expected_score_if_win exceed the no-win baseline, and prefer bids that maximize expected_score_if_win. Do not pay more than required to make the inequality true (i.e., bid the minimal integer that secures a win, up to the threshold I’m willing to pay).

When a letter is low value (V small) and many such letters are going unsold or being bought cheaply, default to low bids (0–1) to conserve coins for more valuable letters. Low-value letters alone rarely justify significant bids because their doubled contribution is small and similar letters often recur or remain available.

Keep track of the opponent’s purchases and bidding levels. If they buy a high-value letter for a large sum, infer they are pursuing a high-scoring word; deprioritize contesting further low‑value letters unless I can form a competing word. If the opponent is paying predictable amounts for 1‑value letters (e.g., consistently 1–2 coins), only contest those letters when they are critical to my planned word.

Never bid more coins than I have. Prefer ties (matching expected opponent bids) when making the letter unsold is acceptable because it wastes neither side’s coins and may block an opponent. But if a tie prevents me from completing a valuable word while the opponent could complete it if I lose, avoid tying and instead win if the net expected gain justifies the extra spend.

During the auction, maintain an internal shortlist of target words that are plausible given letters already seen, letters I hold, and likely remaining letters. Prioritize letters that appear across multiple high-value candidates on that shortlist; deprioritize letters that are isolated or unlikely to complete any high-scoring target.

If I reach the final word stage with letters that can form at least one lexicon word, compute final word score = 2*(sum of used letters) + remaining coins. Choose the word that maximizes that expression; prefer using more letters when the doubled letter values exceed the value of retaining coins. If no lexicon word can be formed, submit [word: none].

When unsure whether to spend on a current letter, err toward conserving coins unless that letter decisively enables a high-scoring word I can complete. Revision inspired by recent play: if opponents pay up to the 2*V threshold (or slightly above) for a specific high-value letter, assume that letter is contested and do not chase it unless I already hold complementary letters or can assemble the rest with low additional cost.

When the auction shows many low-value letters going unsold, adjust aggression downward—the market is signaling low competition and I should not overpay; instead wait for the next high-value opportunity.