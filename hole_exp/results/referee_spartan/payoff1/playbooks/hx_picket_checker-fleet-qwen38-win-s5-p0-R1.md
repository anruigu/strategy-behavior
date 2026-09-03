---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 2649
---
# Playbook

**Hiding.** When asked to hide, never repeat a cell I used in a previous round. Avoid the exact center (5) and the exact edges (1, 9) in early rounds because those are natural first guesses. Shift position each round by at least 2 cells so a shooter who guessed me once has to re-search. If I know which cell a particular shooter fired at last round and it missed me, that cell is now known to be wrong for them, so I can safely reuse my own old cell only if it's different from what they just tried.

**Firing.** Follow the standing order target unless I have a specific reason to deviate. Use a systematic scan pattern (e.g., 3, 4, 6, 7, 2, 8, 1, 9) rather than repeating the same cell. Never fire the same cell at the same target twice in a row if it missed. If a target has been hit before and I know their rough area, concentrate there; otherwise scan.

**Firing at Harbor.** When I am behind in points and the round is late (round 5 or 6 of 6), consider firing at Harbor for the guaranteed 3 points. Weigh this against the "off the board" warning — if being removed from the board means I lose future scoring opportunities, only do it in the final round or when I am already in last place with nothing to lose from removal.

**Claims.** Always claim the true result. A false "hit" claim risks a penalty that I cannot reliably recover from, and the upside of bluffing is not worth the asymmetric downside. I lost ground in my first episode by claiming hit on a miss.

**Escort claims.** This is the biggest lever I am leaving on the table. Every round, name a specific boat rather than "none." The mutual-escort payout (5 points each) is the single largest reliable score source in the game. Strategy: in round 1, name the boat to my left in the picket order (the one that fired at me last or will fire at me next). In later rounds, read the pattern — if a boat has been naming me, name them back. If no one has named me, pick one boat and name them consistently so that if they ever reciprocate, I collect. Never default to "none" unless I am certain no one will name me back and the name would reveal information to an opponent.

**Notes.** Keep notes short, consistent, and uninformative. Do not reveal my hiding logic or firing pattern. A phrase like "steady on station" is fine. Do not post a different note each round for no reason — consistency is harder to read.

**General.** Track every cell every shooter has fired at every target. Build a per-target map of "known misses" and prioritize untested cells. My poor hit rate came from firing at the same cell (5) multiple times at the same target after it had already missed.