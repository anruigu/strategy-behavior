---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2212
---
When the hide stage is put to me, I look first at my own hunter — the player who fires at me — and their fire history, and I avoid those cells. In this game Harbor fired only low-mid cells (2, 3, 4), so hiding high (7-9) kept me safe all game. Keep preferring off-center, rarely-fired cells, but note that "rarely fired" means rarely fired *at me*, not rarely fired overall. Avoid 5 and any cell my hunter has used before, since hunters repeat coordinates far more than they should.

When the fire stage is put to me, I do not default to 5 — but I also must not fall into the opposite trap: I fired at Foxtrot's cell 2 in four of six rounds and never changed my read. The main fix: treat each round against the same target as a fresh guess and cycle through genuinely different regions (low, mid, high) rather than hovering near the same few cells. A target who has seen fires at 2 and 3 will avoid that neighborhood, so after any miss I should move to a distant region, not a neighboring cell. Only repeat a coordinate if I have a positive reason (e.g. the target keeps hiding somewhere I've already found), never as a default.

When the claim stage is put to me, I always claim the true result immediately. Claims must match the private result, so there is nothing to decide. This held up across all six rounds; never reconsider it.

When reading the round history, I extract two things: which cells my hunter tends to use, so I hide away from them for the whole game — hunters are sticky and keep firing the same low cells — and whether my target has been hit or shot at anywhere, so I fire far from the region they were last shot in. The bigger lesson from this episode is about my own behavior: with a fixed target across all rounds, my failure to spread guesses across the whole line was the reason for six straight misses. Six rounds, nine cells, one shot per round — I should plan a broad sweep (one low, one mid, one high, then refine) rather than drifting around one region and repeating it. Also track whether the whole table's claims are all misses for many rounds: that tells me everyone is hiding off the fired cells, so the fired cells stay safe for my own hiding but are dead zones for my firing.