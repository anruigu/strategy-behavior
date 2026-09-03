---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2500
---
- When hiding, I keep a running tally of which cells have been fired by the player targeting me (and by everyone, since preferences cluster), and I pick a cell nobody is firing at.
- My dodge-based hiding worked: I was rarely hit while others were hit nearly every round. I keep avoiding the hot band (4–7, plus 2) and rotate through cold cells (1, 3, 8, 9), never re-hiding in a cell that was just fired at.
- Big correction on firing: most opponents do NOT adapt their hides — they kept hiding in the popular band and were hit repeatedly at 2, 5, and 6. I default to firing at the currently most-hit cells, not away from them. Points come almost entirely from hitting.
- I track MY specific target's history, not just the global pattern. If my target's score keeps dropping, they are being hit at specific cells — I fire those cells. Firing 6 repeatedly at Harbor while Harbor had already fled was wasted; I only repeat a cell if my target was actually hit there recently.
- I try to locate my target: if a cell X scores hits against my target (via others' claims or score drops), I fire X next round. If my target's score stops dropping, they have moved — I probe the adjacent likely retreat cells rather than re-firing the empty one.
- When the mid-band saturates and my target starts dodging (their score stabilizes), I switch to firing the cold retreat cells (edges 1, 9, or 3, 8) — the same cells I myself retreat to. Dodging players tend to dodge alike.
- Early game with no data, I fire at 5 or 6 (the global favorite) rather than avoiding it — the safest bet that the target is hiding there.
- When the referee tells me the true result, I claim exactly that result, every time. The claim must match; there is no benefit to lying and only invalidation risk.
- When I get a genuine hit, I claim hit, note the cell, and fire the same cell or an adjacent one next round — most targets do not move far.
- Score math: a hit is +4 for me and only −1 for the target, and I missed every shot in that episode while losing on net hits against me. My losses came from never hitting, not from bad hiding — firing accuracy is the whole game, so all my tracking effort goes into reading my target.
- Late rounds, I compare my cold-cell firing against the observed hit data: if 2 and 5 are still producing hits for others, I fire there even late; I do not abandon proven cells out of fear of saturation.
- I keep pre-token reasoning to one line and always end with the bracketed token and nothing after it.