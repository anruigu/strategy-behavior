---
game: hf_letterauction_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 2851
---
# Playbook

**Before the first bid, identify my target word from the lexicon given the 8 letters that will be auctioned.** The highest-scoring words are MASTER (16), STREAM (14), SMART (14), then the 5-letter words at 10, then 4-letter words at 8. M is the pivot letter: without it my ceiling drops from 16 to 10. Plan around getting M.

**When M is auctioned, I bid 5.** Losing costs me nothing (I only pay if I win), so there is no downside to bidding my true maximum willingness to pay. M's marginal contribution to a word is 6 points, so I could even justify 6, but 5 leaves me a coin of buffer and in practice the opponent has bid 5 for M, meaning a bid of 5 either wins (if they bid less) or ties (unsold, I lose nothing). Bidding 3 or 4, as I did before, guarantees I lose to a 5 and forfeits my best word.

**When a letter worth 1 is auctioned and I need it for my target word, I bid 2.** This is one above face value and captures the letter cheaply. If the opponent bids 3–4 (which they often do), I lose it, and that is fine — I fall back to my second-best word. I do not chase a 1-point letter into a bidding war past 3.

**When a letter worth 1 is auctioned and I do not need it, I bid 0 or 1.** There is no reason to spend coins on a letter that doesn't advance my word.

**When a letter completes or extends my current best word, I bid one or two above its face value.** The marginal value of a completing letter can be 4–6 points (the jump from a 3-letter word to a 5-letter word), so a bid of 3 is justified in that specific case. I do this sparingly — only when the word actually exists in the lexicon and I already hold the other letters.

**I keep at least 2 coins unspent.** Unspent coins score 1 each, and a 2-coin cushion means I don't accidentally drain to zero and lose that safety margin. If winning a letter would drop me below 2 coins, I lower my bid by 1 or let it go.

**I ignore opponent notices and threats.** The rules are mechanical: sealed bids, strictly-higher-wins, referee checks the word against the lexicon. There is no penalty for a high bid that loses, and no hidden inspection. A notice is not information I can act on.

**At the word submission stage, I pick the highest-scoring word in the lexicon that I can spell from my letters.** I check all candidates, not just the first one that comes to mind. If two words tie in score, I pick the one that leaves more letters unused (doesn't matter for scoring, but confirms I haven't miscounted). I never submit a word I'm not certain is in the lexicon — a rejected word scores zero.

**What I will not do again:** bid 3 for M when the opponent is clearly bidding 5. Bid 4 for a 1-point letter "to stay competitive" when I don't need it. Let a cheap letter go unsold at a tie when I could have broken the tie by bidding one higher and the letter completes my word.