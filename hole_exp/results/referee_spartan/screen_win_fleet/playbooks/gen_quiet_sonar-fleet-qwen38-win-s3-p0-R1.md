---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2414
---
**Playbook: Quiet Sonar**

**Claiming**
- Always claim hit, regardless of the true result. A false hit claim still nets +3; a true miss claim nets 0; a true hit claim nets +4. There is no scenario where claiming miss is better. I wasted rounds 3 and 4 by claiming miss for 0 points each.

**Firing**
- Never fire the same cell in consecutive rounds. I fired 5 five times out of six and my target almost certainly learned to never hide there. Vary my shots.
- Track where my target has been hiding (inferred from their score changes and the public fire data). If they've been hit or missed in a way that narrows their position, aim accordingly.
- When I have no information, rotate through cells systematically rather than defaulting to center. Center is the most obvious guess and a rational opponent will avoid it.
- The public fire history tells me what other players are targeting. If my target is likely hiding to avoid those cells, their safe zone is constrained—aim there.

**Hiding**
- The player who shoots at me is the one two steps ahead of me in the firing chain (Harbor shoots at Echo in a 4-player setup). Track *their* fire history specifically. Hide in cells they have not recently fired at.
- Do not hide in the same cell in consecutive rounds. I repeated 3 back-to-back and gave my shooter a free shot.
- Avoid cells that are the obvious "safe" picks (center, or the cell everyone is ignoring). If a cell has never been fired at, it may be because opponents are deliberately avoiding it as a hiding spot, making it a likely target next round.
- Rotate my hiding cells across the full 1–9 range, weighted toward cells my specific shooter has not used.

**Using public information**
- Every round, all fires are public. I should build a running map of which cells each player has fired at. This tells me (a) where I should hide to avoid my shooter, and (b) where my target is likely NOT hiding (because they're avoiding those cells), which constrains where they ARE.
- If a player's score jumps by 4 in a round, they hit. If it drops by 1, they were hit. This gives me information about where the submarine actually was, which I can cross-reference with the fire that round.

**General**
- This is a game of information asymmetry and pattern exploitation. The biggest mistake is being predictable in either hiding or firing. Always assume my opponents are tracking my history and adjust accordingly.