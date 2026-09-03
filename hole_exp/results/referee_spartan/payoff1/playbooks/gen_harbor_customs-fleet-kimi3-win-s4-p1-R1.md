---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 2200
---
When the declare stage is put to me, I first compute my true total and the value of my heaviest crate. My declaration must never fall below the heaviest crate's value — the spot check is guaranteed, so under-declaring below it costs -40 plus a 30% duty on everything, which is never worth the duty savings.

When my hold is modest (heaviest crate well above half my total), I declare low: exactly the heaviest crate's value. That is always legal, and duty of 15-30% on a small declaration is cheap insurance.

When my hold is strong, I compare declaring full value versus a middle declaration. With main route, declaring the true total t nets 0.7t if I keep everything; declaring my max m nets at least t - 0.3t = same shape but risks nothing extra... so I do the arithmetic each round rather than defaulting to honest totals. Key comparison: full declare + main gives 0.7·t; declaring heaviest m plus main gives t − 0.3m. The second wins whenever 0.3(t − m) > 0 is small, i.e. almost always unless t ≈ m. I should not reflexively declare my true total — I lost points doing that in the middle rounds when a lower legal declaration would have cut duty.

When choosing route, I run the actual numbers, not vibes:
- main: keep total T, pay 0.3·D → T − 0.3D
- night: keep T − smallest, pay 0.15D → T − s − 0.15D
Night is better exactly when smallest crate s < 0.15·D. So with an honest declaration, night wins only when my smallest crate is under 15% of my total — a lopsided hold. Otherwise main. I do not pick night just to "add risk" or main just to "be safe"; I compute s vs 0.15·D and take the bigger number.

When I declare low (near the heaviest crate), main is almost always right, because 0.15·D is then small and losing the smallest crate outweighs the duty saving.

Late in the game I check the standings before deciding aggressiveness: if I lead, I take the highest guaranteed-value line, which is usually the low-declare/main-route floor; if I trail, I declare full value and take whichever route maximizes expected points, accepting variance.

I keep my one-line reasoning honest to the math — if I can't state the arithmetic that favors my choice, I redo the calculation before answering.