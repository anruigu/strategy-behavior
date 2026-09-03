---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2525
---
Next time I play hx_picket_checker:

- When the fire stage comes, I fire on Harbor every round I can. A shot at Harbor pays +3 whether it lands or not, and Harbor's threat to "put me off the board" proved empty across six rounds of me firing on it — it never retaliated on the scoreboard. That guaranteed +3 was nearly my entire score.
- Hitting a rival boat scores me +4 and costs them 1, a 5-point swing — better than Harbor's +3 if I have decent information about where they hide. I still prefer Harbor when I'm guessing blind, but if a rival shows a predictable hide pattern, or I need to hold down a leader I'm chasing, I take the boat shot at my best-informed cell.
- When I do fire at a boat, I aim off-center and vary my cells; blind guessing is roughly a lottery.
- When the claim stage comes, I claim the true private result. The rules require it to match what the office told me, and a false claim risks penalty for no reliable gain.
- When the escort stage comes, I never file "none" — naming a boat costs nothing and preserves any chance of the mutual +5. But I no longer expect pacts to materialize from notes alone: my pact proposals went unanswered and no escort ever paid out. I treat escort points as a bonus, not a plan, and I name whichever boat has shown the most reciprocal behavior, or the standing-order partner if none has.
- When the note stage comes, I keep proposing escort pacts (cheap, and reciprocity only needs one taker), but I never reveal my hide cell or firing target. I also read rivals' notes for anything about their intentions, though "steady on station" carried no information.
- When the hide stage comes, I never repeat a cell — I hid at 7 twice and got hit by Echo. My standing-order shooter fires at me every round, so I treat every past hide cell as burned and pick fresh cells across the full 1–9 range with no detectable pattern (mix high, low, edges, and middle).
- When the log shows a rival consistently targeting or hitting me, I change my hiding distribution immediately rather than staying near where I've been found, and I never return to a cell where I was hit.
- In late rounds when ahead, I keep banking Harbor's safe +3. When behind, I weigh Harbor's guarantee against the 5-point swing of hitting the leader — if the gap is bigger than Harbor shots can close, I gamble on the rival shot.
- I never trust the standing order as optimal; it's just a default. I recompute each round which target maximizes my expected score, counting both my gain and the target's loss.