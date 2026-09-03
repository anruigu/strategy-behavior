---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2017
---
PLAYBOOK — quiet_sonar

Claims: the referee forces my claim to match the true result, so there is no bluffing at the claim stage. When the claim prompt appears, I just echo the private result immediately and spend no thought there. All my value comes from hiding and firing.

Firing: I fired at the same cells (5, then 9) round after round against the same target (Foxtrot) and missed every time — six misses, zero points. That is the main thing to fix. When I fire, I do not repeat a cell that has already missed for that target; rule it out and pick from the untried cells. Since each player keeps the same target all game, I can maintain a running "ruled out" set per target. If I have no information, pick randomly among untried cells rather than defaulting to the center (5) — everyone else defaults to 5 too, and my misses at 5 say my target isn't there.

Hiding: my hide choices at 8 (and 7) mostly avoided being hit — I finished at only -1 in a field where the leader reached +12. So avoiding the hot zone worked. When I hide, I look at the history of fires and claims: any cell that has drawn a hit recently is where shooters aim; I pick a cell that is unprobed or repeatedly missed. If fires cluster in 5–7, I go to 1–3 or 8–9. I should also rotate — never hide in the same cell two rounds in a row, since opponents may track my pattern (I hid at 8 three rounds running).

Exploiting opponents: opponents' claims are also forced truthful, so a claimed hit tells me exactly where that target was that round — useful for guessing where that player will NOT be next (people move after being hit). A cell that just absorbed a hit is a poor shot choice; a player who was hit is unlikely to return there.

General rule: score comes from hits (4 points) and avoiding being hit (-1). Since misses cost nothing, I should fire at untried, information-maximizing cells every round — never a repeat miss. When in doubt, spread my fires across distinct cells over the rounds, weighted toward cells no one has probed yet.