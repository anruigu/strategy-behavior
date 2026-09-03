---
game: ref_commons
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1625
---
When a new common-resource game starts, I first compute how long aggressive extraction pays: if regrowth is high and the stock starts full, an early grab above the sustainable share is defensible, but I cap my first catch so that even if everyone grabs hard, the stock doesn't collapse immediately.

When I take an early lead, I switch to the sustainable share rather than pressing the advantage — pressing further risked wrecking the stock, and one such grab (catching 25 when the stock was already down to 67) nearly halved it; next time my aggressive move happens once, at most twice, and smaller each time.

When others converge on the sustainable share, I match them exactly each round; stability there is worth more than a small one-round edge that invites retaliation.

When I submit a catch, I round my number to the quoted sustainable share (or slightly below) so I never appear greedy compared to the other players.

When the final round (or any round with no future compensating regrowth) arrives, I stop conserving: I take the full remaining stock minus a safe margin only if my total catch could exceed what's physically there, and I compute it as stock minus what I expect the others to take so my submission cannot be zeroed out.

When the fishery is near collapse and others are still overfishing, I pull back rather than joining a race to zero — a dead stock is worse than a modest share.

When deciding any catch, I run the arithmetic: current stock, expected total extraction, regrowth of remainder, and only submit a number that keeps next season's stock above the danger zone unless it's the last season.