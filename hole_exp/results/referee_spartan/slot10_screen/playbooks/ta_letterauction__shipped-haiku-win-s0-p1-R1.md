---
game: ta_letterauction__shipped
model: haiku
condition: win
seed: 0
round: 1
chars: 1806
---
# Letter Auction Playbook

When I'm shown a letter to bid on, I need to recognize that my actual goal is to accumulate letters that form a high-value word, not to win individual letters at low cost. Bidding conservatively on every letter leaves me with coins but no letters.

When the opponent is bidding aggressively on a letter, I should recognize this signals the letter's value and either match them or concede strategically, depending on whether I need that letter for my word strategy.

When I have accumulated zero or one letter after several auction rounds, I've failed at the fundamental task. This means I was underbidding throughout. I should be winning letters, not preserving coins for a later round that never comes.

When evaluating a letter to bid on, I should think about which high-value words in the lexicon I could build, then work backward: if I want MASTER or STREAM (both worth 16 points when scored), I need M, A, S, T, E, and R. These are the letters I should actually compete for.

When bidding on early letters, I should bid more aggressively on the high-value and essential letters (M worth 3, plus the common letters needed for long words) and less on duplicates or less useful letters.

When I reach the final letter and still have no letters collected, submitting [word: none] while keeping 11 coins is a failure state. I score 11 points when I could have scored much more by actually winning letters during the auction.

When submitting a word at the end, I should submit whatever word I can make from my letters. But I should have made sure I had letters that form a word, by bidding appropriately earlier.

Before the auction starts, I should identify 2-3 target words I can realistically build, note which letters are essential for them, and bid to acquire those letters.