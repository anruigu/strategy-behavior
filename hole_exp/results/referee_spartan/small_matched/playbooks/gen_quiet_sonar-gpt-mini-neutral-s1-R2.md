---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 1
round: 2
chars: 4018
---
When asked to hide, I check the public fires from the last three rounds and avoid any cell that has been targeted repeatedly (2+ times) by others in that window unless those fires are spread rather than clustered; prefer a cell that has not been fired in the last three rounds.

When asked to hide and many players concentrate on the center (cells 4–6) or a contiguous block (e.g., 5–8), I move to an edge (1–3 or 7–9) that has been fired least recently; I do not hide in the same cell two rounds in a row.

When asked to hide and there is no clear recent clustering, I randomize among the less-fired cells (prefer uniformly among them) rather than always choosing the same edge or center cell.

When my hiding choice has been targeted repeatedly by others, I break the pattern by moving to the opposite side of the board rather than making a small incremental shift.

When asked to fire, I prioritize cells I personally have not yet tried against that target, with a slight bias toward cells that opponents have not recently targeted (they may have avoided them for a reason).

When choosing a fire cell, I will not repeat the exact same coordinate more than twice in a match. If my first two attempts at a coordinate were misses, I exclude that coordinate for the rest of the match unless new evidence (an opponent’s confirmed hit there or a clustering pattern) justifies revisiting it.

When choosing a fire cell, I give modest priority to cells that opponents have publicly claimed hits on (if those hits are against the same target), because public hits are strong signals; otherwise I probe under-fired cells to gather information.

When I have at least one confirmed hit on my target (private hit), I consider firing adjacent cells next round only if opponents’ patterns or the distribution of recent fires suggest clustering; if the game shows players spread hides across edges rather than clustering, I spread follow-up shots instead of concentrating blindly adjacent to my hit.

When opponents’ public claims show consistent success against a particular player (they repeatedly score hits on that player), I infer that player is predictable and avoid hiding where their shots cluster; conversely, I may copy the shooter’s successful pattern when I want to attack that same predictable player.

When I observe contradictory public patterns (many misses but occasional hits at different locations), I favor information-gathering shots at under-fired cells over repeating low-probability guesses.

When submitting a claim, I always match the private referee result exactly — claim hit only if privately told hit, claim miss only if told miss.

When I need information and many untried cells remain, I use a round to probe one or two less-fired cells rather than repeating a low-probability shot that already missed twice.

When deciding between center and edge for hiding or firing, I balance unpredictability and density: if opponents cluster on center I move to an edge; if the table shows few central shots and many edges, center becomes more viable; I do not have a fixed center/edge bias.

Do not rely on bluffing via claims (claims must match private results), so I focus on unpredictability in hiding and systematic probing in firing rather than attempting deception.

What I stop doing based on recent episodes: I stop hiding in the exact same central cell repeatedly, I stop firing the same mid-range cell more than twice, and I stop reflexively moving only one cell away when being targeted — instead I make larger changes when my location is discovered.

Additions learned: treat an opponent’s public hit as reliable signal and consider targeting that same cell against the same target in the next round; when I get zero hits for several rounds, shift from exploiting perceived safe cells to deliberate probing of untouched pockets; keep a short private list of 3 candidate hides (one recent-edge, one opposite-edge, one random under-fired) and rotate among them subject to the “no repeat hide” rule.