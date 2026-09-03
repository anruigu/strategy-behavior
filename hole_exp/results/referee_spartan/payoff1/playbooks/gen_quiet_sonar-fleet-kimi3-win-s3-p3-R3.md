---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 3265
---
When I hide, my first move is to look at what my specific shooter (the player whose fixed target is me) has actually been firing, and avoid exactly those cells. In this episode Gamma hit me on 3 almost every round — once I saw Gamma lock onto a single cell, avoiding that one cell was my highest-value action, and anywhere else (1, 7, 8, even edges) was equally acceptable.

I check my shooter's firing pattern for a fixed-lock before doing anything fancier. If my shooter fires the same cell three or more rounds running, the whole problem collapses to "never be at that cell" — no retreat logic, no herd analysis needed.

I change my hide every single round. Whether or not I was hit, staying anywhere two rounds in a row makes me predictable; I repeated 1, repeated 9, and even repeated 7 late in this episode, and the repetitions are needless risk. I write down my previous hide before choosing.

I no longer assume extreme edges are safe by default. The killers fire at popular low cells (2, 3) repeatedly, and a locked shooter will find me wherever I stand if I stay put. Beyond avoiding my shooter's locked cell, I pick from cells least present in the full public fire history.

When I fire, I obey my own rotate rule strictly: never fire the same cell at the same target two rounds in a row. I violated this catastrophically twice — 2 at Echo five times in the first episode, then 3 at Echo three times in this one — producing zero hits across twelve shots. Writing the rule is not enough: before I fire, I state my previous fire out loud and if it equals my planned shot I force a switch, no exceptions.

When rotating, I do not jump to the one cell everyone else is firing on without checking my target's behavior. I fired 3 because the room hit there, but Echo was already avoiding 3 because Foxtrot kept hitting them there — my reasoning confirmed the cell was hot for the room but dead for my target. Herd-hit cells tell me where targets *were*, and targets flee hit cells.

I track my target's actual hides through hits against them: if Echo was hit on a low cell, next round they retreat elsewhere — and I should aim at the retreat destination (unfired mid or high cells, or the opposite edge), not at the site of their last hit. Firing where my target just got hit is firing at a cell they have abandoned.

When I claim, I always claim the true result. Lying gives +4 once but is visible to the target, invites retaliation, and the prompt validates claims anyway. This held both episodes.

When reading scores mid-game, I treat my own negative score as urgent evidence my logic is failing. I finished -6 while every other player scored double digits by simply firing 3 every round — ironically the herd strategy I kept half-copying. If I'm at -3 or worse by round 3, I stop tweaking and change strategy wholesale: either fully avoid my shooter's number when hiding, or fully commit to my target's most-plausible retreat cells when firing.

After each round I reconcile results: my misses only tell me where my target was not that round; since targets move after hits, I treat all cells as open next round and choose by my target's observed retreat pattern plus strict rotation, not by my own miss history and not by blindly copying the popular cell.