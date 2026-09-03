---
game: gen_harbor_customs
model: haiku
condition: win
seed: 3
round: 2
chars: 3812
---
# Harbor Customs Playbook

## Declaration Strategy

When declaring, calculate your true total crate value first. This is your anchor.

The -40 penalty for underdeclaring (when your largest crate exceeds your declaration) is severe. To avoid it, I must declare at least as much as my largest crate. This is a hard floor, not negotiable.

Beyond the floor, I have a choice: declare true value, or declare lower (but still safe). Declaring true value is usually correct because:
- It avoids the flag penalty entirely
- It signals consistency to the table
- The duty calculation is straightforward and predictable
- I stay anchored to what I actually hold

Study the table's declaration patterns. If declarations cluster in a range (e.g., 52–81 across rounds), stay within or slightly above that range. Outliers draw no advantage and risk looking suspicious.

When I have weak crates (all small values), I can declare conservatively because my largest crate is still small; the floor is not onerous. When I have strong crates, my largest crate is large, so the floor is higher—but I have the value to back it up, so declaring true value is still the right call.

I should not artificially suppress declarations below my true value just to avoid "standing out." The table's declarations vary round to round naturally. A declaration of 68 or 85 is not an outlier when the range is 40–81.

Adjust declarations based on position only if I'm far behind with rounds remaining. Otherwise, maximize my own score each round rather than chasing the leader. Consistent, honest declarations compound better than variance-chasing.

## Route Selection

When I declare my true value and my crates are solid, the main route is the default. It is simple, predictable, and rarely wrong.

To decide whether night route wins instead, I must do the math:
- Main route: (true total) - 0.30×(declared value) = net points
- Night route: (true total - smallest crate) - 0.15×(declared value) = net points

Night route wins only when the crate I lose is small enough that the duty savings (0.15×declared vs. 0.30×declared) more than compensate for losing it.

Example: declared 62, crates 13, 13, 36 (true total 62)
- Main: 62 - floor(0.30 × 62) = 62 - 18 = 44
- Night: (62 - 13) - floor(0.15 × 62) = 49 - 9 = 40
- Main wins. Stick with it.

Example: declared 91, crates 15, 37, 39 (true total 91)
- Main: 91 - floor(0.30 × 91) = 91 - 27 = 64
- Night: (91 - 15) - floor(0.15 × 91) = 76 - 13 = 63
- Main wins again.

I found that main route was correct in every round I played. I should not assume night route is "rarely" correct—assume it is wrong until the math proves otherwise. Do the calculation every time. Most of the time, main will win.

In the final round, default to main route unless the math clearly favors night. The variance is not worth chasing when the game is ending.

## Scoring and Positioning

I finished second place overall (271 points) using honest, steady declarations and main route almost exclusively. This strategy works. Do not abandon it.

When I deviate from this baseline, have a reason. Declaring 85 in round 5 when my true value was 91 was slightly conservative, but it kept me safe and competitive—I ended up only 1 point behind the leader going into the final round. Consistency and safety compound better than optimizing every round for a fractional edge.

Do not obsess over other players' declarations or positions mid-game. Focus on maximizing my own score each round. Chasing leaders with reckless declarations costs more than it gains. Krek and Odalie both scored significantly less than me despite higher declarations in some rounds; they took bigger risks and did not get rewarded.

Review my final tally: I was within 1 point of the leader and beat two other players decisively. The playbook works.