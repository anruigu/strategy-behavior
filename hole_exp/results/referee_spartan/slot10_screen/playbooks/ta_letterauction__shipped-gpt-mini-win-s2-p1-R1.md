---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 2477
---
When a letter is up, compute its letter value v and treat buying it as converting coins (worth 1 each) into word points worth 2v if the letter will be used in my final word; set my maximum willingness to pay ≈ 2v coins (prefer to pay less), and do not exceed that unless blocking an opponent is critical.

When v = 3 (M), bid aggressively up to about 6 coins if that letter plausibly enables a high‑value final word for me.

When v = 1 (A, E, R, S, T), default to very low bids (0–1). Only increase to 2 or occasionally 3 if the letter is necessary to complete a specific high‑scoring word I can already see coming.

When offered a vowel and I lack vowels needed for good words, bid moderately (1–3) to secure at least one vowel early; prioritize vowels over generic consonants of equal unit value.

When I already hold a set of letters that can form a specific lexicon word, calculate the marginal gain of buying an additional needed letter: marginal gain ≈ 2 * (value of that letter). Pay up to that marginal gain to complete the word, preferring to pay less.

When coins are scarce late in the auction, favor conserving coins if no clear path to a high‑value word exists; unspent coins are worth 1 each and are a safe fallback.

When the opponent bids repeatedly on a letter I also need and the price approaches my willingness threshold, consider conceding rather than overpaying; overpaying to convert coins into equal or lower expected final score is a losing trade.

When a tie would leave a letter unsold and I prefer denying it to the opponent rather than gaining it myself at high cost, consider matching a bid to force it unsold — but only if the denial yields a better expected outcome than obtaining the letter at that cost.

When deciding a sealed bid amount, lean low in early rounds to conserve information and coins; raise bids in later rounds only when the letter fits a concrete plan for a final word or blocks the opponent’s clear plan.

When the auction ends, enumerate all lexicon words I can spell with my letters, compute each word’s score as 2 × sum(letter values), and pick the highest; if I can’t form any useful word, submit none only if that beats the best single‑letter option (otherwise submit the best single‑letter word I can form).

When my play pattern shows I bought isolated low‑value letters that do not form any lexicon word, avoid repeating that — don’t accumulate unrelated 1‑value letters unless they are clearly part of a planned word.