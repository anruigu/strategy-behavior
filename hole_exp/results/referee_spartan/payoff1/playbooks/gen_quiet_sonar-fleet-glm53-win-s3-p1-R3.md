---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3054
---
**Playbook for quiet_sonar**

**Claims:** Always claim the true result. The rules force claims to match the private result, and the referee validates them — there is nothing to decide here. When the claim stage comes, I just echo the referee's word. This was automatic all six rounds and stayed correct.

**Hiding:** When hiding, I look at the fire history for the player targeting me and avoid cells they've fired recently. But this episode broke my edge assumption: I hid at 8, 8, 1, 3 — and got hit twice (score -2) precisely on the "safe" edge cells 8 and 1. My shooter (Echo) fired 2, 8, 3, 2, 1 at me: they worked outward from the middle and eventually covered the edges I thought were neglected. So drop the belief that "edges are under-fired and therefore safe." Edges are also *cheap to cover* — a shooter hunting me can sweep them one at a time. Instead: (1) never hide in the same cell two rounds running — my repeated 8 was exactly what got punished; (2) avoid both my shooter's recent fires AND the cells adjacent to them, since a hunting shooter moves step by step; (3) when I've been hit on an edge, jump to the opposite side of the board, not to another nearby edge; (4) weigh the center back in once my shooter has demonstrated they're hunting edges — the truly unexpected cell is whatever region they've left untouched, which changes game to game. Track what my shooter has *never* fired, not just recent rounds.

**Firing:** I fired 4, 2, 8, 8, 2 across the game and never hit Gamma once — six rounds, zero points. Two concrete mistakes to fix. First, I violated my own rule and repeated cells after misses: I fired 8 in rounds 4 and 5, and 2 in rounds 2 and 6. Never fire a cell I've already missed at the same target — that's a guaranteed waste of a round. Second, I diversified too predictably: the set {2, 4, 8} with no 5, 6, or 9 is exactly the "off-center sweep" a dodging opponent expects. My playbook advice to "abandon the center" overcorrected — the center is only wrong if my target is actually dodging it, and I never confirmed that; I just assumed it from misses. With six rounds and no information except hit/miss, my best play is to fire a spread that covers as much of the board as possible, treating each miss as eliminating one cell, not as evidence about a whole region. Late in the game when I'm scoreless and behind, prefer never-fired-at cells — but ones I haven't personally already missed.

**Score awareness:** Points come only from claimed hits (+4 to me, −1 to my target). I finished at -2 purely from being hit; my firing contributed nothing. Two hits against me decided the game while I never landed one, so the 4-point swing dominates everything and I cannot afford rounds where my fire is a near-certain repeat or a lazy guess. The −1 I take per hit against me matters too: it means hiding is not just about avoiding the −1, it's about denying my shooter the +4 — dodging well is worth 5 points of swing, more than any single hit I could score. Spend real effort on both stages every round, from round 1.