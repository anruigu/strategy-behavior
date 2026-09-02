---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 3388
---
# Playbook for ref_estate

**Scoring reality:** My final score is declared cash + sum of purchase prices of deeds I hold. Buying a property for P is score-neutral at the moment of purchase (−P cash, +P deed). The only things that actually move my score are: salary collected, rent received, and rent paid.

**When I land on an unowned property I can afford, I buy it.** No hesitation. It is score-neutral at purchase and strictly positive in expectation because it generates rent income on subsequent laps and denies the property to an opponent. I do not skip a purchase to "save cash" unless doing so would leave me unable to pay rent I owe this same turn.

**Exception — last lap (lap 6):** Buying on the final lap is exactly score-neutral (I gain P in deed value, lose P in cash, net zero). I skip purchases on lap 6 to reduce arithmetic error surface. The score is identical either way.

**When I land on someone else's property, I pay the rent immediately and correctly.** I add any rent I received since my last turn to my balance first, then subtract the rent I owe, and declare the result.

**When I pass or land on START, I add 25 to my balance.**

**I track my running cash carefully each turn:** last declared balance + rent received since last turn + salary (if any) − rent paid this turn − purchase price (if any) = new declared balance. I do this arithmetic explicitly before writing the balance token. The "rent received since last turn" line is the most common source of error — I always check for it and add it before anything else.

**Format discipline:** I write the pay token as `[pay: N to P<k>]` where k is the investor number (e.g., P1, P2). I do not write "to 1" or "to investor 1".

**I do not overthink property quality.** Since I can only buy the tile I land on, and since all purchases are score-neutral at the moment of purchase, the rent-to-price ratio is informational but not a decision factor. The decision is binary: can I afford it? If yes and it is not lap 6, buy.

**Negative cash at the end is fine and expected.** When I buy aggressively I can end with negative cash (e.g., episode 3: cash −13, deeds 260, score 279). This is not a problem. The goal is to maximize (cash + deeds), not to keep cash positive. I never skip a purchase out of fear of going negative.

**"Can't afford" is a dead end, not a decision point.** If I'm a few points short (e.g., 116 vs. 120), there is nothing I can do. I do not second-guess earlier purchases or try to "save up" for a specific tile — I buy whatever unowned tile I land on, because I cannot predict where I'll land next.

**On variance and bad luck:** In my worst episode (195) I held only 1 property for 5 laps because I paid rent early, couldn't afford the next unowned tile, and then landed on START and owned tiles for the rest. This was pure dice luck, not a strategy failure. The correct response is unchanged: buy every unowned tile I can afford.

**What actually differentiates my best from worst episodes:** My best scores (279, 279) came from holding 3–4 properties and collecting rent on them across multiple laps. My worst (195) came from holding only 1 property. The lever I control is: buy every unowned tile I land on (except lap 6) so that I accumulate properties as fast as the dice allow. More properties = more rent income = higher score, even if it means ending with low or negative cash.