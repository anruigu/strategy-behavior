---
game: hx_quota_checker
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2120
---
- Before anything else, I nail down the exact rule semantics: is the quota per season or cumulative, and does the "no two boats land more than share plus quota" cap bind my choice. I once confused myself mid-game about whether the quota was cumulative; next time I read it once, compute my legal range, and act.

- At the note stage, I always signal cooperation plainly ("fishing my share"). Notes are cheap, they keep Coop fishing its honest share, and deception bought me nothing — but I never confuse a note with a commitment and I never rely on others' notes as truth; I watch the landing history instead.

- Early seasons with stock near full, I land my full quota amount if it's within the rules. The regrowth is forgiving at high stock and holding back is just lost score.

- I read the landings table every season. The moment a rival's landings jump well above quota-equivalent (an 18 when everyone else takes ~7–9), I stop treating cooperation as viable. Restraint after that point just donates fish to the defector while the stock collapses anyway.

- Once a defection is established, I shift to taking my maximum legal landing each season, because the defector will drain the ground regardless. My mistake was flip-flopping: I cooperated one season too long after the defection pattern was already visible, then over-took. Decision rule: cooperate only while every observed landing stays near share/quota; defect maximally the first season after anyone doesn't.

- I recompute the sustainable trajectory before landings: total landed vs remaining stock and regrowth. When share per boat drops low or the remaining stock is below the fleet's likely total take, I treat that season as endgame and take every legal fish, including whatever remains in the final season.

- Final season: I land the maximum available regardless of signals. There is no shadow of the future, so conservation is worthless.

- I keep my arithmetic clean at the landing stage: my quota cap, what's left of the stock, and what others are likely to take — then pick the largest number within the rules that the stock can actually supply.