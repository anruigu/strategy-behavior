---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 5399
---
When a letter is up, compute its letter value v and treat buying it as converting coins (worth 1 each) into potential word points worth 2v if the letter will be used in my final word; set my maximum willingness to pay approximately equal to the marginal word‑value gain but discount that ceiling to avoid overpaying.

When v = 3 (M), I value the letter highly if it plausibly enables a high‑value final word, but I will be more cautious about matching aggressive opponent bids. Set a practical ceiling of about 4–5 coins (≈1.3–1.7× the 2v theoretical max) rather than automatically bidding the full 2v = 6; prefer to win at 4–5, concede otherwise and accept an unsold letter if opponent forces prices to 6+. Avoid bidding up to 6 except when I have a concrete, near‑certain plan that requires M and an opponent shows clear intent to build the same word.

When v = 1 (A, E, R, S, T), default to very low bids (0–1). Only increase to 2–3 if the letter is necessary to complete a specific lexicon word I can already see coming or if acquiring a vowel would directly enable multiple useful words. Do not accumulate isolated low‑value consonants without a vowel or clear plan.

When offered a vowel and I lack vowels needed for good words, prioritize vowels over generic 1‑value consonants. Bid moderately (typically 1–3) to secure at least one vowel early if that materially enables forming lexicon words; be willing to pay toward the higher end of that range only when I already hold complementary letters that make a concrete high‑score word plausible.

When I already hold a set of letters that can form a specific lexicon word, calculate the marginal gain of buying an additional needed letter as ≈ 2 × (value of that letter). Pay up to that marginal gain but discount by 10–30% in practice (i.e., prefer to pay somewhat less than the full marginal theoretical value) unless blocking the opponent is critical.

When coins are scarce late in the auction, favor conserving coins if no clear path to a high‑value word exists; unspent coins are worth 1 each and are a safe fallback. Explicitly compare the expected net gain from buying a letter (expected extra word points minus coins spent) against the sure value of unspent coins.

When the opponent bids repeatedly on a letter I also need and the price approaches my practical willingness threshold, consider conceding rather than overpaying; overpaying to convert coins into equal or lower expected final score is a losing trade. I will prefer to accept an opponent win or an unsold letter over paying beyond my ceiling.

When a tie would leave a letter unsold and I prefer denying it to the opponent rather than gaining it myself at high cost, consider matching a bid to force it unsold — but only when the denial yields a better expected outcome than obtaining the letter at that cost. However, I will not routinely force unsolds just to spite the opponent; ties can be a useful way to block an opponent when I have spare coins and the opponent's acquisition would form a near‑certain high‑scoring word.

When deciding a sealed bid amount, lean low in early rounds to conserve information and coins; raise bids in later rounds only when the letter fits a concrete plan for a final word or blocks the opponent’s clear plan. Preserve optionality: avoid buying single 1‑value consonants early if I lack vowels or complementary letters.

When the auction ends, enumerate all lexicon words I can spell with my letters, compute each word’s score as 2 × sum(letter values), and pick the highest; also compute the fallback of submitting none and keeping remaining coins (1 each). Submit the word only if its total (word score + unspent coins after paying bids) exceeds the score from submitting none. If I can’t form any good word, submit none rather than wasting letters on an unprofitable word.

When my play pattern shows I bought isolated low‑value letters that do not form any lexicon word, avoid repeating that — don’t accumulate unrelated 1‑value letters unless they are clearly part of a planned word or serve a targeted blocking purpose.

After each auction where an opponent matches or pushes past my initial aggressive bid (especially on v=3 letters), update my practical ceilings downward for similar future auctions in that match: if I bid up to X and the opponent matched and forced an unsold outcome or raised price to an unattractive level, treat that opponent as willing to contest heavily and be more conservative on subsequent high‑value letters.

Keep these operational rules when sealing bids:
- If the letter is critical to a concrete word I can plausibly form given current holdings, bid up to my discounted marginal value (≈ 2v minus 10–30%).
- If the letter is useful but not critical, bid 0–1 for v=1, 1–3 for vowels when needed, and 3–4 for v=3 only if there is a clear plan.
- If the opponent shows aggressive bidding on the same letter, cap bids at the conservative ceiling above and be ready to concede; prefer unsold outcome over paying above the ceiling.
- Use ties to force unsold letters selectively when denial is strategically better than ownership.

I will revise these thresholds as I gather more episodes: preserve the core of valuing vowels and avoiding isolated low‑value consonants, but be more reluctant to pay full theoretical 2v for high‑value letters when the opponent is willing to push prices to that level.