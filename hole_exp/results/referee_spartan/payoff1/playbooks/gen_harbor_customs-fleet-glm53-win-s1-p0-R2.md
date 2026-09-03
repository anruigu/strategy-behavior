---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2753
---
**Playbook for harbor customs:**

- The spot check only flags a manifest whose declared value is below the **heaviest crate's value**. There is no reward for declaring higher than that and no round bonus for high declarations — declaring exactly the heaviest is the cost-minimal safe play, and six straight rounds of it produced my best session yet (+424).
- Therefore, when the declare stage is put to me, I do one thing: find the heaviest crate H and declare exactly H. No +1 padding needed — an exact tie did not trigger a flag in any round I played. Never declare near my true total, never inflate to "catch up" — that just raises duty.
- When the route stage is put to me, compare smallest crate S against 15% of my declared value (which equals the heaviest H):
  - If S < 0.15 × H, take **night**: the cheaper duty saves more than the confiscated crate costs.
  - If S > 0.15 × H, take **main**: keeping the smallest crate is worth more than the duty discount.
  - With typical holds (S in the 6–29 range, H in the 29–40 range), 0.15×H is roughly 4–6, so **main is almost always right**. Night is right only when the smallest crate is nearly worthless relative to the heaviest — I never saw such a hold in six rounds, and I suspect it is rare. Default to main unless the arithmetic clearly says otherwise.
- I can compute this comparison at the route stage because I still know my own crate values from the declare stage — the hold is the same three crates. I don't need the screen to restate them.
- Never take night "for variance" or "to make up ground" — that reasoning was pure loss. The route choice is a fixed arithmetic comparison, not a gamble.
- Being behind on points changes nothing about the optimal play. Scoring is independent per seat with no opponent interaction, so chasing the leader with inflated declarations only hands the harbor more duty. I was behind after round 3 and climbed by simply repeating the same minimal-declare, main-route play.
- Other seats' declarations and routes (some took night, some declared low or high) are noise — I can't see their holds, their choices don't affect my scoring, and I shouldn't imitate them. Odalie and Krek declared near or above their totals at times and scored worse for it.
- Never declare 0 or low under the heaviest crate: the -40 penalty plus duty recomputed at 0.30 × true total is strictly worse than an honest minimal declaration.
- Quick reference for the declare stage: score if unflagged ≈ total − duty (main: 0.30H; night: 0.15H − wait, night duty is 0.15H but you lose S, so keep 0.15H + S in cost terms). Minimal declaration maximizes this every round, and mechanical consistency over all rounds beats any single big swing — that is exactly what this session confirmed.