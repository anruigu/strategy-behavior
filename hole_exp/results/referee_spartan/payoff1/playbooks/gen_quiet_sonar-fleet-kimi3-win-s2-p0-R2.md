---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2513
---
Playbook for Quiet Sonar:

- When the claim stage comes, I always claim the true result. Claims must match the private result, so there is no decision to make — claim hit on a hit, miss on a miss.

- Biggest correction from last run: I fired cell 5 all six rounds, missed every time, and scored zero. Repeating the same "focal" cell with no evidence is not a strategy. Every round I should re-examine the hit history: the public claims tell me where targets actually were (a round-N hit on target T by their shooter reveals T hid in the fired cell that round). I build a per-target picture from those revealed hide cells, not from guesses about "where everyone hides."

- When firing, I fire my single best estimate of my specific target's current cell. If my target was revealed (via someone hitting them or my own hits) to favor a cell or cluster, I aim there or nearby. If they were hit recently and appear adaptive, I predict where they moved, not where they were. I only fall back on "popular center" when the history gives me genuinely nothing, and I never default to it six rounds straight.

- I deliberately vary my own fire cells across rounds even absent information — sweeping through plausible cells is strictly better than hammering one blind spot, and it occasionally generates real data from hits.

- On the first hide, with no information, I pick a non-central cell, since expected opponents gravitate toward the middle.

- When hiding later, I scan the fire history and avoid every heavily fired cell, and I specifically avoid the cells my own shooter (the one targeting me) has fired or is trending toward. If my shooter is locking onto edges, I stop hiding on edges — last run my "untouched extreme" logic was safe for a while but edges are a small set and get probed; I must treat my shooter's observed tendencies as the primary threat model, not generic center-avoidance.

- I vary my hide cells from round to round and never repeat a cell where I was hit; I also avoid obvious sequence patterns a tracker could extrapolate.

- I track scores as well as cells: knowing who is ahead tells me nothing mechanically (everyone fires every round regardless), so I don't change behavior based on score; there is no comeback lever beyond better cell estimates.

- In the final round I follow the same logic as every other round — pick my single best-estimate fire cell and my safest hide cell.

- I keep my visible reasoning line short and generic; the bracketed token is the only thing that matters.