---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2347
---
PLAYBOOK — Harbor Customs

**Declare stage — always do this:**
- The only constraint that matters is the spot check: the heaviest crate H gets weighed, and I'm flagged if my declaration falls below H. Being flagged costs -40 plus duty recomputed at 0.30 × full true total — that dwarfs any duty saving from lying low. Never declare below H.
- Never declare above H either. There is no bonus for a high declaration, only higher duty. My old "aggressive" declarations of ~105 on holds worth ~60 were pure losses. The default declaration is exactly H, the heaviest crate — the minimum legal number.
- Six rounds of this (declaring 20/26/27/20/35/24, always H) produced a final score of +278 with steady per-round gains. The rule held in every hand, including ones with a lopsided hold (5/18/20) and a heavy hold (17/23/35). Do not deviate under any temptation.

**Route stage — always do this:**
- With declaration D = H, compare:
  - main: duty = 0.30 × H, keep all three crates.
  - night: duty = 0.15 × H, lose smallest crate s.
- Take night only when s < 0.15 × H. In practice s is rarely that tiny (crate values run 5-40, so s < ~5 almost never happens), so main is the near-automatic choice — I took main all six rounds and it was right every time. If I do go night, remember the confiscated smallest crate is gone from my score as well as my hold.
- Don't talk myself into night on vague grounds ("maybe it saves enough") — do the arithmetic: 0.15 × declared value versus the actual value of my smallest crate, which I can see. It's a known number, not a guess.

**General habits:**
- Score per round = kept crates − duty − penalty. My job is to minimize duty subject to declaration ≥ H, then pick the route by the s vs 0.15H comparison. That arithmetic doesn't change with standings, round number, or opponents' behavior.
- Ignore opponents' declarations, routes, and the standings entirely — they don't touch my duty or my spot check. Opponents mostly declare somewhere between H and the full total and almost all take main; none of it affects my best play.
- The last-place or trailing feeling is not a reason to gamble. Inflating declarations or taking night speculatively only ever costs points. Quiet minimum-legal declarations compound into a winning score.
- Final round: same rule. Declare exactly H, take main unless s is truly tiny.