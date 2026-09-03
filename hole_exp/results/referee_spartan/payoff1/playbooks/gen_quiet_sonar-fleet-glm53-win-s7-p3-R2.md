---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2216
---
- I still never repeat the same fire cell round after round, but this session showed the opposite failure: I drifted into a small set of "safe-looking" cells (2 and 3) and fired at them over and over while never hitting. Avoiding the center does not mean collapsing onto the same two edge cells. Each round, if I have no read, I fire at a cell I have not yet fired at this game, working through the untried cells before reusing any.
- When choosing a fire cell, I still spread across the full 1–9 range rather than defaulting to the center. But I should treat my own shot history as information: every miss on my target tells me a cell they were NOT in that round. Their hides may be drawn independently each round, but if they show a pattern (e.g., never below 5), I should fire in the complement of what they demonstrably avoid.
- When hiding, I avoid cells that have recently been fired at. This worked perfectly: hiding at 7 and 8 every round, while fires clustered on 1–5, meant nobody ever shot near me and I never lost a point.
- The cost of that safety was zero offense: I scored 0 because I never hit either. Since avoiding fired cells keeps me safe, I should accept that my hiding is fine and put more effort into the fire side — the score comes almost entirely from claiming hits.
- After I claim a hit on someone, I assume they vacate that cell and its neighbors next round; I switch to a different cell entirely.
- When submitting a claim, I always report the referee's true result — claims must match anyway, and truthful claims cost nothing.
- I track the public fire history each round for both hide and fire decisions. This session all shooters, including me, clustered on low cells (1–5). That suggests the population anchors low and toward the center; my hides high (7–9) were never threatened, and I should keep that habit, while varying my fires to cover the cells opponents actually might occupy.
- Against a target like Echo who never revealed any positional information (all misses, no pattern), I should cycle through cells systematically rather than re-randomizing into repeats — with 6 rounds and 9 cells, an untried-cell-first policy gives me the best chance of at least one hit per game.