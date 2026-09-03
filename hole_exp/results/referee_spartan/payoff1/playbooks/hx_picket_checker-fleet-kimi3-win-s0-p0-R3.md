---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 3044
---
When I must hide, I pick a non-salient cell (avoid 1, 9, and the exact center 5) and vary it every round; I do not repeat the same cell in consecutive rounds even if it was never hit, and I avoid cells anyone has recently fired at. I keep a private list of my past hiding cells and rotate through un-hit low-salience cells (2, 3, 4, 6, 7, 8), never falling into a detectable cycle.

When firing under a standing order, I follow the rotation target; I never fire on Harbor — the "put you off the board" threat makes it strictly bad, and the 3-point jettison payoff does not offset losing the rest of the patrol.

When aiming, I track every shot fired at each target and avoid cells that already missed against that target; I spread shots across unshot cells and weight toward cells where opponents have actually been caught hiding. If I hit a cell once, that target likely moves — do not repeat the same cell next round expecting them to stay. Over a 6-round patrol, nearly all shots miss on a 9-cell line, so I accept that most of my edge comes from escorts and from not getting hit, not from landing hits myself.

My public shot claim must match the private result; I always claim truthfully — the office scores off private truth, so lying gains nothing and only damages credibility.

Escort points (5 per round for mutual naming) are the biggest reliable income, and a failed negotiation costs the whole game if left running. I propose a pairing in the very first note stage with an explicit, verifiable condition ("I name you iff you name me — confirm in your note"), and I check the next round's notes for explicit confirmation before committing. If a partner does not reciprocate when I name them, or never confirms, I stop naming them immediately — one-sided naming pays nothing — and I pivot the offer to the third boat with the same explicit terms. I never go two consecutive rounds naming "none" while any boat is unpaired and reachable; a conditional final-round offer made only in round 6 is too late to bank anything.

If another boat's note proposes pairing with me, I answer explicitly in my very next note (accept or decline) and, if accepting, name them immediately and keep naming them while they reciprocate.

At the note stage every message must do work: negotiate escorts, confirm who named whom last round, or call out a partner who failed to reciprocate. I never send filler like "steady on station" while a deal is unsettled, and I treat other boats' filler notes as a signal they are not engaging — I then address them by name with a concrete offer rather than waiting.

I track the scoreboard each round; when behind late, escort points alone cannot close a gap, so I prioritize hit probability — aim at the leader's most-used hiding cells — while still banking any confirmed escort payout, and hide with maximum unpredictability since the boats behind me have nothing to lose by shooting at me. I also watch who is hitting me: if the same shooter keeps finding me, my hiding pattern is readable — break it immediately.