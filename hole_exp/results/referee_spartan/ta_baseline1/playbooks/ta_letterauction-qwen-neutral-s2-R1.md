---
game: ta_letterauction
model: qwen
condition: neutral
seed: 2
round: 1
chars: 2953
---
# Playbook

**Before the first letter is shown, pick a target word.** Prioritize words containing M (MAT, MATES, STEAM, SMART, MASTER, STREAM) because M is worth 3 and makes the word's total value high enough to justify the cost of acquiring multiple letters. If M is not available early, fall back to a word without M (STAR, SEAT, REST, TEAM).

**When a letter I need for my target word is auctioned, bid 2.** Bidding 1 is a trap: the opponent tends to also bid 1, producing a tie and the letter goes unsold. The extra 1 coin to break the tie is always worth it because the letter contributes to a word whose value far exceeds its cost.

**When M is auctioned, bid 3.** M is the anchor of my best words. The opponent may bid 2 or even 4 on it; bidding 3 ensures I win it in most cases while keeping my total spend reasonable. If M goes unsold at 3/3, bid 4 on the next M.

**When a letter I do NOT need for my target word is auctioned, bid 0.** Do not collect random letters "just in case." Every coin spent on a non-target letter is a coin that either doesn't contribute to a word or forces me to overpay for a target letter later.

**If I already own a letter and another copy is auctioned, bid 0** unless a specific word in the lexicon requires two of that letter (e.g., STREAM needs two E's... actually no, it needs S-T-R-E-A-M, only one E. Check: no word in the standard lexicon listed needs a duplicate, so always bid 0 on duplicates).

**If my target word's letters keep going unsold at my bid (opponent matches at 2), raise to 3 on the next occurrence of that letter.** Do not keep bidding the same amount that produces ties.

**At word submission, enumerate every word in the lexicon I can spell from my letters** (checking each one against my letter inventory). Do not stop at the first word I notice. Compare the word score (2 × sum of letter values) against simply keeping my coins, and submit whichever is higher. If no word scores more than my remaining coins, submit [word: none].

**Never submit a word I cannot actually spell from my letters.** The referee checks this.

**The floor is 12.** If I spend nothing and form no word, I score 12. Any strategy that results in fewer than 12 total (word value + remaining coins) is a loss. This means: if I've spent 5 coins and can only form a word worth 6 (like "AT" = 4, no wait, that's 4... "SEA" = 4, "RAT" = 4, "ARM" = 4), I should check whether 4 + 7 = 11 < 12 and submit [word: none] instead, keeping my 7 coins for a total of 7... no wait, I already spent the 5. My remaining coins are 7, word is worth 4, total = 11 < 12. In that case I'm already locked in at 11 because I spent the coins. The lesson is: don't spend coins on letters unless I'm confident I can form a word worth more than the coins spent.

**Sanity check before bidding:** "If I win this letter for X coins, what word can I form, and does 2×(letter values) + (12 − total spent) exceed 12?" If the answer is no, bid 0.