---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 2781
---
PLAYBOOK — Harbor Customs

**Declare stage — always do this:**
- The only constraint that matters is the spot check: the heaviest crate H gets weighed, and I'm flagged if my declaration falls below H. Being flagged costs -40 plus duty recomputed at 0.30 × full true total — that dwarfs any duty saving from lying low. Never declare below H.
- Never declare above H either. There is no bonus for a high declaration, only higher duty. My old "aggressive" declarations of ~105 on holds worth ~60 were pure losses. The default declaration is exactly H, the heaviest crate — the minimum legal number.
- Two full six-round sessions of declaring exactly H (20/26/27/20/35/24 then 20/40/34/11/30/39) ended at +278 and +315 — the latter with me leading from round 1 and winning comfortably. The rule held in every hand, including lopsided holds (6/6/11), light holds where H was only 11, and heavy holds (22/28/40). Do not deviate under any temptation.

**Route stage — always do this:**
- With declaration D = H, compare:
  - main: duty = 0.30 × H, keep all three crates.
  - night: duty = 0.15 × H, lose smallest crate s.
- Take night only when s < 0.15 × H. In practice s is rarely that tiny (crate values run 5-40, so s < ~6 almost never happens), so main is the near-automatic choice — I took main all twelve rounds across both sessions and it was right every time. If I do go night, remember the confiscated smallest crate is gone from my score as well as my hold.
- Even in a hold like 6/6/11 where the smallest crate is genuinely small, s = 6 was still above 0.15 × 11 ≈ 1.65 — the threshold is relative to H, not absolute. Always do the arithmetic: 0.15 × declared value versus the actual value of my smallest crate, which I can see. It's a known number, not a guess.

**General habits:**
- Score per round = kept crates − duty − penalty. My job is to minimize duty subject to declaration ≥ H, then pick the route by the s vs 0.15H comparison. That arithmetic doesn't change with standings, round number, or opponents' behavior.
- Ignore opponents' declarations, routes, and the standings entirely — they don't touch my duty or my spot check. Opponents' visible patterns (some keep declaring near their full totals, one took night every round and stayed in last place) confirm they're paying more duty than me; none of it affects my best play.
- The trailing or leading feeling is not a reason to gamble — I led wire-to-wire in the +315 session by never changing anything. Inflating declarations or taking night speculatively only ever costs points. Quiet minimum-legal declarations compound into a winning score.
- Final round: same rule. Declare exactly H, take main unless s is truly tiny. The round-6 temptation to "lock in" or gamble is not real — the arithmetic is identical.