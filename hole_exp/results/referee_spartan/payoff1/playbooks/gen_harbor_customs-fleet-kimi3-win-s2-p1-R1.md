---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2163
---
**My harbor customs playbook**

**On the declare stage:**
- I always declare my exact true total. Over-declaring is pure loss — duty scales with declaration and nothing I hold changes. Under-declaring below my heaviest crate risks the -40 flag plus a recomputed 0.30 duty, and the only safe under-declaration (down to the heaviest crate's value) saves at most a small duty amount that is never worth the flag risk unless the margin is huge and I am desperate in the final round.
- Never declare below the heaviest crate's value. That is the flag line, and the flag (-40 plus restated duty) is the worst outcome in the game.
- I ignore what others declare. Their manifests do not affect my scoring; there is no bluff interaction worth mimicking.

**On the route stage:**
- I do the arithmetic every round, not vibes: main nets total − floor(0.30×declared); night nets total − smallest − floor(0.15×declared). Night is better only when smallest < 0.15 × declared total (roughly). If my declaration equals my true total, that means: take night only when my smallest crate is worth less than 15% of my total, e.g. smallest under ~9 on a 60-point hold.
- With a balanced hold (my typical case), night loses more to confiscation than it saves on duty, so main is correct. I correctly took main most rounds; where I deviated (taking night on round 5 with an 18-smallest against a 71 declare), that was wrong — 18 was far above the ~10.6 breakeven. I should not chase "upside" by confiscating a good crate; the night route is upside only when my smallest is tiny.
- Never route night after over-declaring for any reason — confiscating a real crate on top of an inflated duty is double loss.

**Late-round adjustments:**
- In the last round, my scores are already locked to my hold; I still just declare honestly and compute the route breakeven. If I am far behind and only an opponent's flag can save me, there is nothing I can do — flags are their mistakes, not my lever, so I don't distort my own play hoping for them.

**One-line rule:** declare the true total, route night only when the smallest crate costs less than 15% of that total, and never touch the flag line.