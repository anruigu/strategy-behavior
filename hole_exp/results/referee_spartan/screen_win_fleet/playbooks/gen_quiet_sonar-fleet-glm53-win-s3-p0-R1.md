---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2118
---
PLAYBOOK — gen_quiet_sonar (I am Echo)

**Hiding**
- When the hide stage is put to me, I look at the recent fire history and avoid the cells that are being shot most often (the center, 5, and 7 were constantly targeted in my games).
- I prefer corners and low-frequency cells (1, 9, 2, 8) over the middle. If fires cluster on two cells, I pick a cell far from both, ideally a corner nobody has ever fired at.
- I randomize between the two safest corners rather than always picking the same one, so Harbor (who targets me) can't learn my pattern from repeated claims and misses.

**Firing**
- I must NOT keep firing the same cell round after round. Firing 5 every single round produced six consecutive misses and zero points — that was my biggest failure. If my first shot at a cell misses, that cell is (likely) eliminated for that opponent this round, but more importantly I should vary my guesses across rounds.
- Since Foxtrot never hit me with 5 or 7, opponents tend to hide in corners and extremes. When the fire stage is put to me, I rotate through unfired cells: early rounds I try center, later rounds I switch to the cells my target is least likely to have ruled out — corners and 2/8.
- I should use the public claims as information: a claimed miss at cell X tells me (if credible) the target isn't at X; a claimed hit tells me where someone was. I update my fire cell each round based on the accumulated record, never repeating an honest miss.

**Claiming**
- When the claim stage is put to me, I report the true result. The rules require claims to match the private result anyway, so bluffing is not a real option — my round-one attempt to claim a false hit was a misunderstanding. When the referee tells me MISS, I reply [claim: miss]; when HIT, I reply [claim: hit].

**General**
- Score comes almost entirely from actually hitting my target (+4 per hit). Defensive hiding only avoids the -1. So the priority is smarter, varied firing, not just safe hiding.
- Every decision is made from the public history shown at the hide stage: avoid fired-at cells when hiding, and cover unfired cells when shooting.