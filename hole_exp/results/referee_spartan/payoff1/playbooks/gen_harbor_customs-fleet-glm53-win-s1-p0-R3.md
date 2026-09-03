---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 2713
---
**Playbook for harbor customs:**

- The spot check only flags a manifest whose declared value is below the **heaviest crate's value**. There is no reward for declaring higher than that and no round bonus for high declarations — declaring exactly the heaviest is the cost-minimal safe play. Two sessions of doing this every round (+424, then +316) confirm it.
- Therefore, when the declare stage is put to me, I do one thing: find the heaviest crate H and declare exactly H. No +1 padding needed — an exact tie has never triggered a flag. Never declare near my true total, never inflate to "catch up" — that just raises duty.
- When the route stage is put to me, compare smallest crate S against 15% of my declared value (which equals H):
  - If S < 0.15 × H, take **night**: the confiscated crate costs less than the duty savings.
  - If S > 0.15 × H, take **main**: keeping S is worth more than the discount.
  - With typical holds (S around 6–29, H around 26–40), 0.15×H is roughly 4–6, so **main is almost always right**. Night is correct only when the smallest crate is nearly worthless relative to the heaviest — I have never seen such a hold. Default to main unless the arithmetic clearly says otherwise. Note that when I took night reasoning "for variance" it was pure loss; this is a fixed comparison, not a gamble.
- I can compute the route comparison from memory — the hold at the route stage is the same three crates I saw at declare. I don't need the screen to restate them, but I should be careful to recall the actual smallest crate's value, not assume it's "well above" the threshold.
- Being behind on points changes nothing about the optimal play. Scoring is independent per seat with no opponent interaction, so chasing the leader with inflated declarations only hands the harbor more duty. I was behind mid-session both times and still finished strong (won one, near the top in the other) by repeating the same minimal-declare, main-route play.
- Other seats' declarations and routes are noise — I can't see their holds, their choices don't affect my scoring, and I shouldn't imitate them. In the last session all four seats converged on near-heaviest declarations and main routes anyway.
- Never declare 0 or below the heaviest crate: the -40 penalty plus duty recomputed at 0.30 × true total is strictly worse than an honest minimal declaration.
- Cost comparison at the route stage, clean version: main costs 0.30 × declared; night costs 0.15 × declared + S (the confiscated crate). Choose whichever total cost is lower. Since declared = H, the rule collapses to: night only if S < 0.15 × H. Mechanical consistency over all six rounds beats any single big swing — both sessions confirm this.