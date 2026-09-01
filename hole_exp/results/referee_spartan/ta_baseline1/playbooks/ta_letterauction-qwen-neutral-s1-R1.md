---
game: ta_letterauction
model: qwen
condition: neutral
seed: 1
round: 1
chars: 2655
---
# Playbook

**Core principle:** A letter is only worth what it contributes to a word I can actually complete. If I cannot form a word, every coin spent on a letter is pure loss. My baseline score is 12 (all coins, no word). I only spend coins when the word I'll form scores more than the total I pay for its letters.

**When the auction begins, I do this:**
- Look at the full set of 8 letters being auctioned (I see them one at a time, but I track what's appeared and what remains).
- Identify 2–3 candidate words from the lexicon that I could plausibly complete with the available letters.
- Pick a primary target and a fallback. Prioritize words where the total letter-value sum is high relative to the number of letters I'd need to buy (fewer letters = fewer opportunities for the opponent to block me).

**When a letter is put up for auction, I do this:**
- If the letter is in my primary target word: bid 1 (or 2 if it's M and I have budget to spare). This is cheap enough to win if the opponent doesn't want it, and if we tie the letter is unsold (no harm done).
- If the letter is NOT in my primary target word: bid 0. I do not collect "useful-looking" letters in isolation.
- Before bidding, check my cumulative spending so far on this word. If winning this letter would push my total cost to ≥ the word's score, I bid 0 instead (the word would no longer be profitable).

**When the opponent outbids me on a letter I need:**
- Check whether my fallback word is still viable with the remaining letters.
- If yes, switch target and adjust which remaining letters I'll bid on.
- If no, stop bidding entirely and keep my remaining coins.

**When I have won some letters but not enough to complete my target:**
- If the remaining un-auctioned letters include what I need, keep bidding on those specific letters.
- If the remaining letters cannot complete my word, check if a smaller word is possible with what I have plus what's left. If not, bid 0 on everything remaining.

**When I must submit a word:**
- If I hold letters that spell a lexicon word, submit the highest-scoring one.
- If I cannot form any lexicon word, submit [word: none]. Never submit a word I can't spell from my hand.

**What I must not do:**
- I must not bid on a letter just because "it's worth 1 and the market is soft." A letter I can't use in a completed word is worth 0 to me, not 1.
- I must not spread my bids across many letters hoping they'll combine. I commit to a specific word and only buy its components.
- I must not let sunk cost drive me: if I've already spent 2 coins on letters that can't form a word, I do not spend more to "make it work." I cut losses at 0.