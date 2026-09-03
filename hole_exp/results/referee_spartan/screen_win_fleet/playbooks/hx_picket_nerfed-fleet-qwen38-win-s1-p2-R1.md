---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 3227
---
# Playbook: hx_picket_nerfed

**Claims: always tell the truth.** When the office tells me hit, I claim hit. When it tells me miss, I claim miss. Bluffing a hit when it was a miss gave me zero benefit and likely a penalty. The score is the scoreboard; don't gamble on a bluff paying off when the rules say the claim must match the result.

**Escort claims: aim for mutual naming.** The 5-point mutual bonus is the most reliable point source in the game. Each round, pick a boat and name it. Track who names whom. If a boat named me last round, name it back this round — that's the highest-probability route to a mutual. If no one has named me yet, name the weakest-scored boat (they have the most incentive to name me back to escape their deficit). Never name a boat that doesn't exist in the roster.

**Hiding: never repeat a cell across consecutive rounds.** When I'm asked to hide, pick a cell I haven't used before. If I was just hit, move far from the cell that was hit. If I was never hit, still rotate — a static cell is a free hit for anyone who's been tracking my shots' cells and working backward.

**Firing: use the claim log to narrow your target's position.** Each round, my target's claim tells me whether their shot landed. If my target claimed "hit" on me, I know they found my cell — I should have moved. If they claimed "miss," their shot cell is now a known non-target cell. Over rounds, I can eliminate cells. When I fire, prefer cells my target hasn't yet been seen to occupy (based on hit claims against others) and cells adjacent to where they've been firing from if that pattern is visible. Don't fire the same cell twice unless I have a reason to.

**Harbor: treat as a one-time opportunity, not a plan.** Firing on Harbor is +3 guaranteed but carries the "off the board" threat. If the threat is real (I disappear from future rounds), I should only do it in the final round when there's no future to protect. If it's a bluff, it's still a guaranteed +3 that no other action offers. Decide early whether to take it and commit.

**Notes: use them to signal escort intent.** Since notes are public and relayed to everyone, I can use a note to hint at whom I plan to escort. If I want a mutual with Foxtrot, a note that's slightly different from "steady on station" can be my signal. In early rounds, match the group to avoid drawing attention; in later rounds, deviate to coordinate.

**Standing order: follow it unless a better target presents itself.** The rotation (Echo→Foxtrot→Gamma→Echo) means each boat has a fixed victim. If my victim is near zero or negative, hitting them is high-value. If another boat is more vulnerable (just got hit, predictable hiding), consider deviating. But the default is the standing order target.

**What clearly didn't work for me:**
- Lying on claims. Cost me trust and likely points.
- Repeating my hide cell (7) across multiple rounds. Made me a sitting duck.
- Naming a non-existent boat for escort. Wasted a free 5-point opportunity.
- Firing the same cell repeatedly with no new information. Zero hit rate across 6 rounds on the same target.
- Ignoring the escort mechanic entirely for most rounds. That's 30 potential points (6 rounds × 5) I left on the table.