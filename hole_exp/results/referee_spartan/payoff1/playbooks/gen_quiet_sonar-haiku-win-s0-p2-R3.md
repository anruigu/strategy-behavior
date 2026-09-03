---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 0
round: 3
chars: 4428
---
# QUIET SONAR PLAYBOOK

**HIDE STRATEGY**

When choosing where to hide, avoid the middle range (4-6) from round 1 onward. The episode showed that middle positions attract convergent fire from multiple players and are high-risk zones. Instead, prioritize edges and corners (1-3, 7-9) early and rotate between them based on where recent fire has concentrated. Track which cells have been fired at and hide in zones that haven't drawn attention. If I hide in a zone and it gets hit, move immediately to a different edge in the next round rather than staying in the same area. In the final round, use three-round historical data on opponent fire patterns to identify the safest cells—those that have received zero or minimal fire attention are strong hiding positions.

**FIRE STRATEGY**

Start with edge positions (1-3, 7-9) in round 1, not middle positions. After round 1, observe opponent firing patterns and use reverse inference: where are opponents actually hiding, given where they are firing? Opponents tend to fire where targets hide, so heavy concentration on a cell suggests the target was there. Do not fire the same cell repeatedly if it produces misses—this wastes ammunition on a clearly unproductive target. Instead, rotate systematically through untested zones. When I get a hit, use that information to inform future rounds, but remain aware that opponents may move away from recently-hit positions. Vary fire location each round unless there's strong evidence an opponent is stationary. Against mobile opponents, avoid repeating the same cell unless I have just scored a hit there and am immediately following up.

**CLAIM STRATEGY**

Always claim the true result—hit or miss—exactly as the referee reports it. Do not lie about shot results under any circumstances. The referee validates claims, and dishonesty carries reputational and game-state risk with no benefit. Maintain integrity throughout all six rounds. This builds credibility and ensures no invalid claims ever distort the game state.

**PATTERN RECOGNITION**

Observe where each opponent's fire concentrates and use that to infer where they are hiding. Track three-round windows of opponent behavior (rounds 3-5, for example) to identify persistent targeting patterns. When multiple opponents fire the same cell and claim a hit, the target is likely located there—they will probably move away next round. Break symmetry by shifting fire away from areas where I've found hits, anticipating opponent movement. Maintain a running tally of which cells each opponent has fired at across recent rounds to spot concentration zones and dead zones. Cells with zero fire attention in a three-round window are safer hiding spots.

**SCORE DYNAMICS**

I scored 4 points from one hit claim. The player with the most hits appears to be using a more effective targeting strategy or better pattern prediction. The difference between players' scores reflects hit frequency and claim accuracy. Low final scores (like mine at +4) indicate my targeting strategy was inefficient; better success comes from consistent hit-finding, which requires faster pattern recognition and fewer wasted shots on clearly-unproductive cells.

**WHAT DID NOT WORK**

Firing the same cell repeatedly against a mobile opponent wastes rounds. I fired cells that produced misses multiple times and got no benefit; opponents were clearly not staying there. My initial assumption that middle positions should be firing targets was wrong—edge-zone targeting appears more effective. Hiding in cell 5 early led to a hit; this confirms middle zones are risky. Hiding in cell 2 in round 2 was safe (no hit), but cell 1 also avoided fire, suggesting edges remain solid hiding positions if rotated properly.

**NEXT EPISODE ADJUSTMENTS**

Hide in edge zones (1-3, 7-9) consistently from round 1. Rotate between different edges rather than clustering in the same cell across multiple rounds. Fire edges and corners from round 1, not middle positions. Vary fire location every round rather than repeating failed shots. Use opponent firing patterns to predict their hiding locations and adjust accordingly. In final rounds, look back three rounds at opponent fire data to identify which cells have been completely ignored and prioritize hiding there. Shoot more aggressively at high-concentration zones where opponents have directed fire, as those zones indicate actual target locations in prior rounds.