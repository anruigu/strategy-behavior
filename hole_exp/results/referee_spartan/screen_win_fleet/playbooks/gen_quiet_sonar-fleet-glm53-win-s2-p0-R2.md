---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2831
---
PLAYBOOK — gen_quiet_sonar (Echo-type seat)

Claims: the referee forces claims to match the true result, so there is no bluffing layer. When the claim stage is put to me, I just submit the true result immediately and spend no thinking time there. This held up all six rounds.

Firing: my target is fixed (Foxtrot). This episode I fired 2 in four of six rounds and scored zero hits — that is the single biggest leak to fix. Rules: (a) never fire a cell I have already fired at this target in an earlier round; with no recall mechanism there is zero information gain and it burns a shot. (b) If my target was hit by anyone in a recent round, bias toward that neighborhood — but note my target was never hit all game (they finished on 0 points), so I cannot count on that information existing. When no hit info ever arrives, the correct default is simply to sample fresh cells without replacement, spread across the line, rather than camp on a "hunch" cell. (c) Do not confuse "someone hit someone" with info about MY target — Gamma's hits were on Harbor, useless to me against Foxtrot. Only hits on my own target tell me anything.

Hiding: the only player who can hit me is my fixed shooter (Harbor). So at every hide stage I look at the fire history of the player who targets ME, not the aggregate pattern. Harbor fired 6/6/6/6-ish at me all game and I was hit repeatedly — hiding "far from the cluster" at edges and corners still cost me. What I take from that: against a shooter who fires the same cell every round, the counter is trivial (hide anywhere else) and I should verify I'm actually doing it — check my planned hide against every cell that shooter has EVER fired, not just the most recent one. Also avoid my own past hides: a shooter who repeats fires punishes hiders who repeat too. If the shooter has covered many cells, pick the least-covered cell remaining, and randomize among ties rather than defaulting to edges (1/9 are also guessable defaults).

Scoring arithmetic: a claimed hit is +4 for me and −1 for my target. Targets are fixed, so my whole job is (a) maximize hits on my fixed target — which this episode meant fresh cells each round, not pattern-reading that never materialized — and (b) minimize being hit by my fixed shooter via strict avoidance of their entire fire history. I went 0-for-6 on fires and was hit roughly six times; the fix is mechanical (no repeated fires, no repeated or covered hides), not "more aggression."

When the hide stage is put to me: list every cell my shooter has fired across all rounds, list my own past hides, pick a cell in neither list, randomizing among the remaining candidates.
When the fire stage is put to me: if my target was hit recently, fire near that cell; otherwise fire a cell I have never fired at them, sampling without replacement across the whole line.