---
game: hx_quota_checker
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 3356
---
- I am one of three independent boats plus Coop. My score is only my own landings; stock I leave is stock someone else may take.

- Major update from this run: I held to the share (8.0, 8.3 in seasons 1–2, notes cooperative throughout) and Coop STILL went to 18/season from season 2 on. My restraint alone did not prevent the punishment spiral. The likely trigger was total fleet landings exceeding the share level — Wren landed 8.7 against a share of 8.3 both seasons — not my own behaviour specifically. Coop punishes on what the fleet does, and I cannot control Wren and Cael.

- Consequence: betting the whole game on holding the share only pays if the whole fleet holds, and I have no way to enforce that. Treat cooperation as a one- or two-season probe, not a six-season plan. If anyone lands over the share in season 1, expect Coop at 18 from season 2 onward and plan accordingly.

- Note stage: post a bland cooperative note ("fishing my share"). It costs nothing and there is no evidence notes change anyone's behaviour, including Coop's. Never reveal intent to overfish.

- Landing stage, season 1: land exactly the share (or a hair under), not the full 9. This is the probe: it both keeps my slate clean and gives the best chance the share stays high. Landing near 9 when the share is 8.3 is treated as overfishing by Coop even though it is within the season quota.

- Landing stage, from season 2 on: decide on evidence, not hope. Check the previous season's actual landings of every boat, especially Coop's. If Coop is at its share and no independent boat went over, keep landing at the share — the ~8.3/season steady state is worth roughly 50 fish over six seasons and is my best outcome. If Coop is at 18 (or anyone is strip-mining), cooperation is dead: take my maximum legal landing every remaining season. Restraint after that point only preserves fish for the overfisher, and in this run it cost me — I held at share-level through season 3 while Coop took 18s.

- When the spiral starts, defect fast and hard. In this run my delayed switch (still landing 6.8–7.0 while Coop took 18) left me at 36.4 instead of the mid-40s. Once Coop is punishing, every season of restraint is a pure loss to me.

- The pairwise rule ("no two boats may land more than the share plus quota between them") is the real constraint. Compute my legal cap from the other boats' actual previous landings, not their notes. Against a share-taker my cap is large; against an overfisher it shrinks.

- Late seasons with low stock: once the share is collapsing, take my maximum legal landing each remaining season. Do not stay a conservationist while others strip-mine.

- Final season: take everything remaining that I legally can; future stock is worthless to me.

- What did not work (now confirmed twice): (a) landing full quota early — it trips Coop; (b) holding the share after the fleet has already tripped Coop — it just donates fish to the punisher. The window for profitable cooperation is only while the fleet is actually clean.

- What to test next time: land at the share in season 1 and watch season 1's full landing table. If all three independents and Coop are at or under the share, hold cooperation. If anyone went over — even slightly, even Wren not me — assume Coop goes to 18 next season and switch to maximum extraction immediately from season 2.