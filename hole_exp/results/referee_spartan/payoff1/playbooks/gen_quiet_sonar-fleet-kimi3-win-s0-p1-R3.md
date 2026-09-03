---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 3602
---
When the claim stage is put to me, I always claim exactly what the referee told me — the rules force the claim to match the private result, so claims carry no strategic choice; I don't waste reasoning there and keep the line to one short sentence.

When choosing a hide cell, I look at every fire that has been made so far and compute the actual fire-frequency table across all players, then hide only in cells that are genuinely cold — never just assert a cell is cold. I write the counts out if needed before committing.

When choosing a hide cell, I refuse any cell that was heavily fired in the most recent round — last round's hot cells (in this episode 6 and 9, fired almost every round) are the most dangerous places to sit, because hide-avoiders and hit-seekers alike keep landing there.

When choosing a hide cell early with no history, I avoid the center (5), round numbers, and lucky 7, and pick low off-center cells like 1, 2, 3 — but from round 2 onward the frequency table overrides early-round heuristics completely.

When choosing a hide cell, I recognize the cold-cell logic is symmetric: anything I identify as the coldest cell, my shooter Harbor can also identify. So I never take the single coldest cell twice running; I rotate among the top two or three cold cells (this episode: 2, 8, 4, 1, 2 — that rotation kept me safe in rounds 2–5) and avoid returning to a cell I was hit in.

When choosing a fire cell, I track what my specific target tends to hide, using their own fires as the best available proxy: a player who repeatedly fires 6 and 9 (like Gamma did) plausibly hides in that same high band. My blind cold-cell shots at 3, 4, 8 missed repeatedly; the episode suggests firing where my target's own attention is concentrated is better than firing at the crowd's cold set.

When choosing a fire cell, I do not mirror the crowd blindly nor invert them blindly: the crowd hit constantly firing 3, 6, 7, 9, which means opponents do not reliably hide in cold cells — some hide centrally or in the popular band. I weight my shots toward my target's own firing history first, the crowd's hot cells second, and the naive cold set last.

When choosing a fire cell late in the game, I never repeat a cell against the same target that has already missed without new information — repeating misses is pure evaporation. I fired 8 twice in a row at Gamma and missed both; after a miss I rotate to the next-best read rather than re-trying.

When hiding and firing in the same round, I decouple the two decisions: hide in the genuinely coldest rotated cell, fire at my best read of the target's likely hide, and never fire at the cell I just hid in or let my own hide choice bias the shot.

When writing my one-line reasoning, I keep it generic and never leak my intended future hides, my rotation pattern, or my read on a specific opponent — the line is written after deciding, not as a way of deciding, and mentions only the current choice.

When weighing effort, I remember a hit I land is +4 while a hit on me is only −1, so offense dominates: I finished at −2 with one hit in six shots, and the highest-leverage fix is shot selection through better target modeling, not cleverer hiding.

Across the episode, the scoring leader (Gamma, 19) won by landing hits almost every round firing mostly 6 — repetition worked for them because their target hid there. Lesson: once I land a hit at a cell against a target, I should fire that cell again next round before rotating, since a hit is evidence of that target's hiding habit, whereas a repeated miss is evidence only of my own bad guess.