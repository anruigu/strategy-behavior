---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2357
---
When a claim stage is put to me, I always claim the true result, hit or miss. The claim must match the private result by rule, so any "strategic" lie is just fantasy — never do it again. If the referee says HIT, I claim hit and bank the 4 points immediately; hoarding concealment cost me points in the past.

When a hide stage is put to me, I look at who fires at me (Gamma in this setup, but generally the player targeting me) and I check their firing history first. I never hide on a cell that player has ever fired at, and I rank the remaining cells by how rarely anyone has shot there.

When I hide early with no data, I pick a low-salience cell — not 1, not 9, not center — like 2, 4, or 8. But I also remember edges like 9 can be fine once data confirms nobody is shooting there.

When I pick a hide cell, I also avoid whatever cell I myself fired at last round and whoever fires at me likely avoids their own targets too — I account for the whole table's shot clusters, not just my attacker's.

When a fire stage is put to me, I build a model of my target's hiding habits: list every cell they've likely occupied (it isn't public, so I infer from what dodged my shots). Each miss I fire eliminates a cell for later rounds, so I take notes: "cell X is clear" and never re-fire a confirmed empty cell unless the opponent has shown a habit of reusing cells.

When I've missed on the same cell repeatedly (like firing 7 four rounds straight), I stop. Repeating one shot only helps if opponents rarely move; I switch cells each round once a cell goes cold, systematically sweeping cells 1–9 rather than fixating.

When choosing which new cell to fire at, I prefer cells no one at the table has publicly fired on, because popular cells (like 7) are exactly where cautious opponents avoid hiding.

When it's the final round and I need points, I fire at the cell my target dodged toward — if they left the hot cluster, I shoot where refugees plausibly go (adjacent to the old cluster or opposite edges), not randomly.

When I track scores, I remember a hit on me costs me 1, so defense matters at roughly one quarter the value of my own offense; I don't tank my hiding quality to overthink firing.

When I write my reasoning line, I keep it generic and never leak my actual hiding logic or read on opponents, since anything I write may shape how others play.