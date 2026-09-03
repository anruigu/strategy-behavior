---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 2306
---
PLAYBOOK — gen_quoet_sonar (Echo-type seat)

Claims: the referee forces claims to match the true result, so there is no bluffing layer. When the claim stage is put to me, I just submit the true result immediately and spend no thinking time there.

Hiding: the only player who can hit me is my fixed shooter (Harbor in this configuration). So at every hide stage I look at the fire history of the one player who targets ME, not the aggregate fire pattern. Harbor fired 5 at me round after round and I kept getting hit by staying near the middle. When the shooter who targets me has repeated a cell or a small cluster, I hide far from that cluster and prefer cells that player has never fired. When their fires have covered most of the line, I switch to unpredictable, non-modal cells (avoid 4-5, avoid cells I've used before). Never hide twice in the same cell across rounds — patterns get exploited.

Firing: my target is fixed too (Foxtrot). The only hard information about their hide is when someone hits them — a hit reveals their cell for that round only, but it tells me they like that region. I fired 5 twice and 9 twice against the same target with no reason to believe those cells were special; that was wasted. Instead: if my target was hit by anyone in a recent round, bias my fire toward that neighborhood; otherwise spread my fires across rounds rather than repeating the same miss twice. Firing the same cell twice at a target who moved is strictly worse than trying a new cell, since there is no reason to expect them to return to a cell I just missed on.

Scoring arithmetic: a claimed hit is +4 for me and −1 for my target. The best marginal use of my fire is to deny the leader points if the target choice mattered — but here targets are fixed, so my whole job is (a) maximize hits on my fixed target via pattern-reading, (b) minimize being hit via unpredictable hides. Going 1-for-6 on fires and being hit several times netted about +1; the fix is not "more aggression," it is target-tracking on fires and anti-pattern hides.

When the hide stage is put to me: check the fire history of my shooter, avoid their cluster and my own past hides, pick a low-traffic cell.
When the fire stage is put to me: check where my target was last hit; otherwise pick a cell I have not yet fired at them.