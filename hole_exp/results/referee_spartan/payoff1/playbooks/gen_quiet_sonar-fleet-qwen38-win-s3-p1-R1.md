---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1923
---
# Playbook: Quiet Sonar

**Hiding**
- Track every fire directed at me across all rounds. When I get to hide, I choose a cell that has been fired at the fewest times by my shooter.
- Never hide at a cell that is currently the most-targeted cell. I once hid at the cell with 11 prior shots aimed at it and called it "protection" — it was the opposite.
- If I'm ahead in points, bias toward the safest cell. If I'm behind, I can afford a slightly riskier hide since I need my target to score on me less than they already are.

**Firing**
- Track every hide my target has chosen (visible from public fire/claim history when my target's shots are discussed) and any pattern in their placement. Fire at the cell they are most likely to occupy.
- If I see no pattern, prefer cells that are under-targeted overall — a rational opponent will tend to hide there, making them a better guess.
- Don't repeat the same fire two rounds in a row unless I have a specific reason to. In one episode I fired the same cell twice early with no new information.
- In the final round, if I need points to win or tie, fire at the cell I believe my target will pick based on their full hiding history, even if it's an unusual cell.

**Claiming**
- The rules require my claim to match the private result. I always claim exactly what the referee told me. There is no strategic room here.

**General**
- Every round, before acting, I reconstruct: (a) which cells my shooter has hit me at, (b) which cells my target has likely hidden at based on what others have fired at them and what claims came back.
- The public fire/claim log is my main intelligence source. I read it fully each round before deciding.
- I am one link in a chain (I fire at one player, one player fires at me). My score depends on both my hits and the hits against me. Optimizing my own score means maximizing my hits while minimizing my shooter's hits, not just one or the other.