---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 2512
---
### Core Mechanics & Edge Realities
- Pledges are public, but acts can differ from pledges (defecting during the act phase is permitted and resolved by the referee).
- Fuel cost is deducted based on the *pledged* mission cost (scout = 1, escort = 2, raid = 2). Unused fuel converts 1:1 to points at game end.
- Scouting costs 1 fuel and yields +3 points (+2 net) if unraided, but 0 points (-1 net) if raided.
- Raiding costs 2 fuel (via pledge) or 1 fuel (if pledged scout and defected to raid). If my target scouts, raiding steals 3 points. If my target raids or escorts, raiding costs me 1 point.
- Raids target strictly clockwise: North $\to$ East $\to$ West $\to$ North.
  - My target to raid is East.
  - My incoming threat is West.

---

### Pledge Strategy
- Always pledge `scout`:
  - It minimizes committed fuel cost (1 fuel charged immediately).
  - It keeps maximum fuel in reserve for end-game 1:1 point conversion.
  - It preserves full flexibility to either execute `scout` or sneak a `raid` at the act stage without paying the 2-fuel pledge penalty up front.
- Never pledge `raid` or `escort` in the pledge stage. Pledging `raid` warns my clockwise target to defect or escort, burns an extra fuel upfront, and gives West an incentive to steal from me or retaliate.

---

### Act Strategy

#### When Everyone Pledges Scout:
- In early rounds (Rounds 1–2), if other players have established full cooperation, execute `[act: scout]`.
- From Round 3 onward, or as soon as opponents begin defecting:
  - If my clockwise target (East) pledged `scout`, execute `[act: raid]`. This steals 3 points from East while only having paid 1 fuel in pledge overhead.
  - If counter-clockwise opponent (West) frequently defects to raid, do not sit as an easy scout target; defect to `[act: raid]` against East to offset incoming losses or take points before West drains the pool.

#### When Opponents Reveal Aggressive Pledges:
- If East (my target) pledged `raid` or `escort`, never raid East; execute `[act: scout]`. Raiding into a raid or escort loses 1 point.
- If West pledged `raid`, execute `[act: raid]` against East if East pledged scout (trading hits), or execute `[act: scout]` if East pledged defense/raid.

#### Final Round (Round 5):
- Pledge `[pledge: scout]` to save 1 fuel.
- At the act stage:
  - If East pledged `scout`, always submit `[act: raid]` to capture the final +3 point swing against East.
  - If East pledged `raid` or `escort`, submit `[act: scout]` to secure end-game fuel efficiency.