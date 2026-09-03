---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2009
---
- At declare stage, I compute the heaviest crate H and declare exactly H unless I plan to go night — the flag triggers only if I declare below H, and every extra point declared costs me duty for nothing. Declaring my full true total wastes duty; I never declare above H.
- Crucially, I know my smallest crate L at decision time — it's printed with my hold at the declare stage. I must write its value down mentally and carry it to the route stage. Last game I repeatedly hedged with "I don't have the smallest-crate value" and guessed route by assumed shape, which lost points (e.g., took night when L=13 and the duty saving was only 4). Never guess: I have all three numbers.
- Exact route math, done every route stage with actual H and L: main nets S − floor(0.3H) where S is my true hold total; night nets (S − L) − floor(0.15H). Night wins iff floor(0.15H) > L. I compute both numbers explicitly and take the larger; if tied, either is fine but I lean main (keeps options/feels cleaner, no penalty difference).
- Top-heavy holds (H large, L small: L < floor(0.15H)) → declare H, go night; harbor takes the dross. This is the best pattern: declare honestly at H, route night, keep the two big crates at 15% duty.
- Balanced holds (L ≥ floor(0.15H)) → declare H, go main, keep all three crates.
- I never declare below H: −40 plus recomputed 30% duty on the true total is strictly worse than any saving.
- Declaring above H never helps either, even when I plan night — night duty is keyed off declared value, so a higher declaration raises it. Always exactly H.
- Opponents' declarations and scores don't change my math; I ignore them except as a sanity check on the flagging rule. Score position doesn't justify inflating declarations or gambling on routes; the same H/L comparison applies in every round including the last.
- Discipline rule: at declare stage I state H, L, and S in my reasoning line, then at route stage I reuse those exact numbers — this prevents the memory gaps that cost me last game.