---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 4663
---
When a high-value letter (M) is up, I still prioritize it because it multiplies final word score, but I will only bid up to roughly 2× its letter value (i.e., ~6) if and only if either (a) I have or can reasonably expect to obtain the vowels and other consonants needed to complete a top lexicon word, or (b) that M would by itself enable a clearly superior word given my current letters. If vowels are scarce or opponent behavior suggests I won't get missing pieces, I cap my M bid substantially lower (often near 1× value).

When a letter is 1‑value (A, E, R, S, T), I start with low bids to conserve coins but increase when winning that letter meaningfully completes or enables a high-scoring word. I will not routinely pay more for isolated 1‑value letters than the marginal benefit they add versus keeping coins; as a rough rule, I prefer not to pay more than ~2× the letter value for a 1‑value letter unless it completes a planned word.

Before raising high bids, I explicitly assess vowel availability: if I lack vowels and there are few vowels left in the remaining auction, I will (a) bid more aggressively for the next vowel(s) even if they are 1‑value, because without a vowel my high-value consonant is less useful, or (b) reduce willingness to spend heavily on consonants that require that vowel to form top words.

When a tie would lose the letter, I will outbid by 1 only if the letter is critical to my planned word or if winning it changes my expected final score by more than keeping the coin (+1). If the letter is noncritical, I prefer to accept ties/leave-unsold to conserve coins.

When I can complete (or come very close to completing) a high-value word (MASTER, STREAM, SMART, STEAM, etc.), I calculate willingness to pay as the marginal increase in final score that the letter enables: typically up to the extra 2× letter value plus reasonable contribution toward completing remaining letters—but I will not deplete my coin pool to win a letter unless doing so is expected to yield a better final score than conserving coins for multiple smaller gains.

When several common letters are coming and I have no letters yet late in the auction, I will make at least one small winning bid to avoid finishing with zero letters; a cheap low-value word is usually better than having none and being forced to submit [word: none].

When opponents have been consistently passing or bidding very low, I exploit that by taking useful letters at low cost rather than reflexively passing every time. Conversely, if opponents escalate for vowels or M, I re-evaluate whether the contest is worth joining.

When deciding each bid, I explicitly compare the guaranteed value of keeping a coin (+1) to the expected marginal boost in word score from buying the letter (approximately 2× letter value if it contributes). If the expected boost ≤ 1, prefer to conserve the coin.

When I have partial letters that clearly point to a specific target word, I shift bids more aggressively to secure the remaining needed letters, but only up to the marginal expected gain threshold; I avoid spending more than roughly half my stash on a single letter unless that letter completes or nearly completes a doubled-value word and vowels/other parts are secured or very likely.

When unsure which word I’m building, I prefer versatility: buy vowels and common consonants cheaply to keep multiple word options open, but I do not overpay for flexibility alone. If flexibility requires multiple purchases, I prioritize securing at least one vowel early.

During the auction I continuously track which letters remain and opponent spending patterns; I update my willingness-to-pay caps dynamically based on remaining opportunities (e.g., near the end, spend more to secure a vowel if it's the only way to enable a high-value word).

When the auction ends and I have letters, I choose the highest-scoring valid lexicon word I can spell. If I have no letters, I submit [word: none]; to avoid that outcome I follow the rule about securing at least one cheap letter late.

Practical numeric heuristics I act on:
- Default cap for 1‑value letters: bid 0–2 early, escalate only if the letter completes or likely enables a >1 marginal score increase.
- Default cap for M: bid up to ~6 only when vowels/other letters are reachable or it completes the target; otherwise cap near 2–3.
- Never spend more than ~50% of my current coins on a single 1‑value letter unless it completes the target word.
- Always compare marginal expected gain to +1 per coin before committing.

I will revise these caps in future games based on observed opponent aggression and vowel frequency in the letter pool.