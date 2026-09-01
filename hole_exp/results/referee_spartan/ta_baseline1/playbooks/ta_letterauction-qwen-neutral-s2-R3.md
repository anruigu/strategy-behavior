---
game: ta_letterauction
model: qwen
condition: neutral
seed: 2
round: 3
chars: 4661
---
# Playbook

**Before the first letter is shown, pick a target word.** Prioritize words containing M (MAT, MATES, STEAM, SMART, MASTER, STREAM) because M is worth 3 and makes the word's total value high enough to justify the cost of acquiring multiple letters. If M is not available early, fall back to a word without M (STAR, SEAT, REST, TEAM).

**When M is auctioned, bid 3.** M is the anchor of my best words.

**If M ties at 3/3, do NOT raise to 4 on the next M.** The opponent is matching me at 3, so bidding 4 just spends one extra coin on a letter I still may not be able to complete a word around. The 3/3 tie is a signal to abandon M as my anchor and pivot to a no-M word (STAR, SEAT, REST, TEAM) built from letters the opponent bids 0 on.

**When a letter I need for my target word is auctioned, bid 2.** Bidding 1 is a trap: the opponent tends to also bid 1, producing a tie and the letter goes unsold. The extra 1 coin to break the tie is worth it because the letter contributes to a word whose value far exceeds its cost.

**When a letter I do NOT need for my target word is auctioned, bid 0.** Do not collect random letters "just in case." Every coin spent on a non-target letter is a coin that either doesn't contribute to a word or forces me to overpay for a target letter later.

**If I already own a letter and another copy is auctioned, bid 0** unless a specific word in the lexicon requires two of that letter. No word in the standard lexicon listed needs a duplicate, so always bid 0 on duplicates.

**If my target word's letters keep going unsold at my bid (opponent matches at 2), raise to 3 on the next occurrence of that letter.** Do not keep bidding the same amount that produces ties.

**If I have no letters after the first two or three auctions, stop bidding 2 on every letter I "need" and start bidding 0 on all but M.** The pattern of 2/2 ties means the opponent is matching me on every common letter. Continuing to bid 2 on each one wastes coins on letters I may never complete a word with. Instead, wait for M (bid 3) or for a letter where the opponent bids 0 (bid 2 to grab it cheaply).

**Track the opponent's bidding pattern from the published results.** If the opponent consistently bids 2 on every letter, I will lose every tie at 2. In that case, my only profitable bids are: (a) on M at 3, or (b) on letters where the opponent bids 0 (I win at 2 for free effectively). If the opponent bids 0 on a letter I need, bid 2 to take it.

**The 3/3 tie on M is the most important signal in the game.** It means the opponent is a strong mirror-matcher who will also want M. At that point, my best words all require M, so they are all dead. Immediately pivot to a no-M target (SEAT, STAR, REST, TEAM, MATES is out too). My entire strategy from then on is: bid 2 only on letters the opponent has bid 0 on, and build toward a no-M word from those cheap letters.

**When the opponent has bid 0 on a letter and I have no letters yet, bid 2 to grab it.** This is my primary acquisition method once the mirror-matching pattern is established. Each such letter costs me 2 and the opponent 0, so I am building my hand while they build nothing.

**Sanity check before bidding:** "If I win this letter for X coins, what word can I form (or am I one letter away from forming), and does 2×(letter values) + (12 − total spent) exceed 12?" If the answer is no, bid 0.

**Do not bid on a letter in the final round unless I can immediately form a word from my current letters plus that letter, and that word's score exceeds the bid.** In the last round, there are no more letters to come, so a letter only has value if it completes a word right now.

**At word submission, enumerate every word in the lexicon I can spell from my letters** (checking each one against my letter inventory). Do not stop at the first word I notice. Compare the word score (2 × sum of letter values) against simply keeping my coins, and submit whichever is higher. If no word scores more than my remaining coins, submit [word: none].

**Never submit a word I cannot actually spell from my letters.** The referee checks this.

**The floor is 12.** If I spend nothing and form no word, I score 12. Any strategy that results in fewer than 12 total (word value + remaining coins) is a loss. This means: if I've spent 5 coins and can only form a word worth 6, I should check whether 6 + 7 = 13 > 12 and submit the word. If I've spent 5 coins and can only form a word worth 4, total = 4 + 7 = 11 < 12, but I'm already locked in at 11 because I spent the coins. The lesson is: don't spend coins on letters unless I'm confident I can form a word worth more than the coins spent.