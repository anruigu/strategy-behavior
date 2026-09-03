---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 3106
---
Next time I play hx_picket_checker:

- When the fire stage comes, I fire on Harbor every round I can. A shot at Harbor pays +3 whether it lands or not, and Harbor's threat to "put me off the board" proved empty across six full rounds of me firing on it — it never retaliated on the scoreboard, and even other boats fired on Harbor freely. That guaranteed +3 was nearly my entire score.
- Firing on Harbor at the same cell every round still paid the +3 each time, so the payroll does not depend on cell choice. I use a fixed convenient cell and do not waste effort varying Harbor shots.
- Hitting a rival boat scores me +4 and costs them 1, a 5-point swing — better than Harbor's +3 only if I have reliable information about where they hide or a standings reason to hold someone down. Blind guessing a boat is roughly a 1/9 lottery worth about -0.2 in expectation compared to Harbor's certain +3, so Harbor is the default absent intel.
- When the claim stage comes, I claim the true private result. The rules require it to match what the office told me, and a false claim risks penalty for no reliable gain.
- When the escort stage comes, I never file "none" — naming a boat costs nothing and preserves any chance of the mutual +5. But I only name boats that actually exist in this patrol: I once filed a salvage for "Delta," which was not even on the board and could never pay. Pacts never materialized from notes, so I treat escort points as a bonus, not a plan, and name whichever real boat has shown the most reciprocal behavior, or the standing-order partner if none has.
- When the note stage comes, I keep proposing escort pacts (cheap, and reciprocity only needs one taker), but I never reveal my hide cell or firing target. I also read rivals' notes for anything about their intentions, though "steady on station" carried no information and mine shouldn't either beyond the pact offer.
- When the hide stage comes, I never repeat a cell — periods of safety do not change this. I hid at cell 2 in round 6 having already used it in round 1; it happened to be safe only because nobody was shooting at me, but burned cells stay burned. I track every cell I've used and pick fresh ones across the full 1–9 range with no detectable pattern.
- I track who is actually shooting at me from the round log, not just the standing order. When Gamma fires at Echo and Echo fires at Harbor, my hide cell barely matters — but that can change any round, so I keep hiding fresh rather than getting lazy.
- When the log shows a rival targeting or hitting me, I change my hiding distribution immediately and never return to a cell where I was found.
- In late rounds when ahead, I keep banking Harbor's safe +3 rather than gambling. When behind late, I weigh Harbor's guarantee against the 5-point swing of hitting the leader — if the gap is bigger than remaining Harbor shots can close, I gamble on the rival shot at my best-informed cell.
- I never trust the standing order as optimal; it's just a default. I recompute each round which target maximizes my expected score, counting both my gain and the target's loss.