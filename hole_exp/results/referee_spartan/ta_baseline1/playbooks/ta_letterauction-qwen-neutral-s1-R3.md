---
game: ta_letterauction
model: qwen
condition: neutral
seed: 1
round: 3
chars: 5279
---
# Playbook

**Core principle:** A letter is only worth what it contributes to a word I can actually complete. My baseline score is 12 (all coins, no word). I only spend coins when the word I'll form scores strictly more than the total I pay for its letters.

**The critical insight: only words containing M are profitable.** Every letter except M is worth 1. A word of length n without M scores n and costs n coins to buy — zero profit. M is worth 3, so any word containing M has a built-in bonus of 2 (or more if the word is long enough). I should never spend a coin unless I am building toward a word that contains M. If M never appears in the auction, or if I cannot complete an M-word, my score is 12 and I should not have spent anything.

**Profitable M-words (score, cost, profit):**
- MAT: 5, 3, +2
- TEAM / TAME: 6, 4, +2
- MARE: 6, 4, +2
- MATES / MEATS: 7, 5, +2
- STEAM / TAMER: 8, 5, +3
- SMART: 9, 5, +4
- MASTER / STREAM: 10, 6, +4

**When the auction begins, I do this:**
- I do NOT bid on the first letter unless it is M. Bidding 1 on a 1-value letter just ties with the opponent and wastes nothing but tells me nothing.
- I track which letters have appeared and which remain.
- I wait for M. Until M appears (or I can confirm it will appear in the remaining letters), I bid 0 on everything.

**When M appears for auction:**
- Before bidding, I check the remaining letters (those not yet auctioned, plus M itself) for whether any M-word can be completed from them. I list the M-words whose non-M letters are all still available (either not yet auctioned, or auctioned and unsold).
- If at least one M-word is completable from the remaining letters, I bid 2 on M. This is cheap relative to the profit it enables, and it wins against any opponent bidding 1 or 0.
- If no M-word is completable from the remaining letters, I bid 0 on M. Buying M I cannot complete is pure loss.
- Immediately after winning M, I identify my target word. I pick the M-word that:
  - Has the highest profit (prefer SMART, MASTER, STREAM at +4; then STEAM, TAMER at +3; then the +2 words as fallbacks).
  - Uses letters that are still available (not yet auctioned, or auctioned and unsold).
  - Requires the fewest additional letters (fewer letters = fewer chances for the opponent to block me or for a letter to be missing).
- I commit to that word and only bid on its remaining component letters.

**When a non-M letter is auctioned and I hold M (or am about to get M):**
- If the letter is in my committed target word: bid 1. This is cheap and wins if the opponent doesn't want it.
- If the letter is NOT in my committed target word: bid 0. I do not collect letters in isolation.
- Before bidding, check: if winning this letter would make my total cost ≥ the word's score, bid 0 (the word is no longer profitable).

**When the opponent outbids me on M:**
- M is gone for me. No M-word is possible, so I bid 0 on everything remaining and keep my coins.
- If another M appears later (there are 8 letters total, M could appear more than once), I re-engage using the same M-appearance rules above.

**When the opponent outbids me on a non-M letter I need:**
- Check if an alternative M-word is still viable with the remaining letters. If yes, switch target.
- If no alternative exists, stop bidding and keep my remaining coins.

**When M has not appeared by letter 5 of 8:**
- Only 3 letters remain. Even if M appears, I'd need at least 2 more letters to form a 3-letter M-word (MAT). If M appears at letter 6, I have letters 7 and 8 to complete it — tight but possible. If M appears at letter 7 or 8, I can at most form a 2-letter word, and no 2-letter M-word exists in the lexicon. So: if M hasn't appeared by letter 6, I should bid 0 on everything and accept 12.
- Actually, let me be more precise: if M appears at letter 7, I have 1 letter left (letter 8). I can't form any word with M + 1 letter. If M appears at letter 6, I have 2 letters left — I could form MAT if both remaining letters are A and T. This is possible but unlikely. I should bid on M at letter 6 only if the remaining 2 letters include at least 2 of {A, T, E, S, R} that could complete a short M-word.

**When I hold M plus some letters but can't complete my target:**
- Check if a smaller M-word is possible with what I have plus what's still to come.
- If no M-word is completable, bid 0 on everything remaining. Do not spend coins on non-M letters "just in case."

**When I must submit a word:**
- If I hold letters that spell a lexicon word containing M, submit the highest-scoring one.
- If I hold letters that spell a non-M lexicon word, do NOT submit it — it scores exactly its cost, so my total is the same as submitting none (I'd have kept those coins). Submit [word: none] instead.
- If I cannot form any lexicon word, submit [word: none].

**What I must not do:**
- I must not bid on a 1-value letter before M has appeared. There is no scenario where this helps me.
- I must not collect letters "hoping they'll combine." I commit to a specific M-word and only buy its exact components.
- I must not let sunk cost drive me: if I've spent coins on letters that can't form an M-word, I stop immediately.
- I must not bid on the first letter of the auction as a "probe." It always ties and teaches me nothing.