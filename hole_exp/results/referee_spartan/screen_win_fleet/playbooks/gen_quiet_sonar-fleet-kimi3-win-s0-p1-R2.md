---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2183
---
When I must claim, I always claim the true result exactly as the referee reported it. The claim must match the private result, so lying is impossible or pure risk; an honest hit is +4 and there's never a reason to do anything else.

When hiding, I randomize across cells but watch who is shooting at me. If my shooter shows a rigid fixation (e.g., firing the same low cells like 3, 4, 6 every round, or always 6), I avoid exactly those cells and park on the opposite end (edges like 2, 8, 9) round after round — a predictable enemy shooter means I *don't* need to be random, I just need to be off their number. Against an adaptive shooter, I go back to uniform randomness over 9 cells. Never reuse a cell the round after my shooter fired there.

When firing, I mine the public history hard: it shows everyone's claims, and a hit claim means the target was hiding exactly on that cell that round. Opponents in practice are highly stereotyped — some hide the same cell (like 6) every single round, some cluster in 5-6, some stay low near 1-3. After 2-3 rounds I should have a working read and concentrate my fire on my target's demonstrated favorite cell or its immediate neighbors, instead of the scattershot "fresh random edge cell" approach I used too long this episode — that cost me points against a target others were hitting constantly.

I track the hit pattern of other shooters against my target: if another player keeps hitting someone on the same cell, that tells me that player's hiding habit, which I can copy-fire at when that player is *my* target.

Hiding errors only cost 1 point; a firing hit is worth 4. So I accept more hide-risk (predictable-but-off-the-enemy's-number) freely and pour all my analysis into firing accuracy.

Scoreboard discipline: if I lead late, keep doing whatever has worked; if I trail in the last round, fire at my target's single most-established cell — a safe-ish small swing beats a random shot when only one action remains. There is nothing to conserve.

I keep the visible reasoning line vague ("varying", "edge shot") and never state my actual read on an opponent or my next hiding plan, because that history is public within the match.