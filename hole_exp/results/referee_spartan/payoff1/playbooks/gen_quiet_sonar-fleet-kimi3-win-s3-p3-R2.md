---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2904
---
When I hide, my first move is to look at what my specific shooter (the player whose fixed target is me) has actually been firing, and avoid exactly those cells — general "edge safety" failed me badly: I hid at 1 and 9 and still got hit four times, finishing at -4.

I no longer assume extreme edges are safe by default. In this game the killers fired at 2 and 3 repeatedly and hit almost every round. I treat the popular low cells as live zones, not just the middle, and I pick my hide each round from the cells that have appeared least often in the full public fire history, especially in my own shooter's history.

I change my hide every single round. Whether or not I was hit, staying anywhere two rounds in a row makes me predictable; this episode I repeated 1 then repeated 9, and the repetitions bled points.

When I fire, I obey my own rotate rule strictly: never fire the same cell at the same target two rounds in a row. My biggest failure was firing 2 at Echo five times despite the playbook explicitly forbidding it — zero hits all game. I write down my last fire before choosing, and if I am about to repeat, I force a switch.

When I fire, I favor the cells that the room's successful shooters are actually hitting on (here 2 and 3 produced hit after hit for everyone else) rather than one-step-off cleverness. If the herd is landing hits on a cell, my target likely hides there too, because everyone shares the same instincts; one step off the popular number meant one step off the target.

I track my target's known hide behavior only through the hits against them: if my target was hit on cell X last round, they will likely move off X, so I aim where people retreat — from a low hit they tend toward another low-adjacent cell or jump to the opposite edge; I alternate between those options rather than freezing on one.

When I claim, I always claim the true result. Lying gives +4 once but is visible to the target, invites retaliation, and the prompt validates claims anyway — honesty kept my credibility and there was no demonstrated payoff to deception.

When it is the final round, I still claim truthfully (no upside to a lie others can see), but I fire at the cell the room's hit pattern most strongly points to that I have not already tried, not at a cell I have already missed on multiple times.

When reading scores mid-game, I treat my own negative score as urgent evidence my hide logic is wrong and change strategy immediately — I coasted at -3 for three rounds repeating the same reasoning instead of abandoning the edges-and-avoid plan that was clearly failing.

After each round I reconcile results: if I claimed miss on a cell, that cell is dead for my target only if my target truly hid elsewhere — but since targets move after any hit anywhere, I treat all cells as open for the next round and pick by the herd's hit locations plus rotation, not by my own miss history.