---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 3443
---
**Playbook**

**Core principle: a purchase is net-zero for your score unless you collect rent on it.** Your score is cash + sum of deed purchase prices you hold. Buying converts cash to deed value at par, so the only way a purchase changes your score is if another player later lands on your tile and pays you rent. Every purchase decision should be framed as: "What is the expected rent income from this tile over the remaining laps?"

**Buy early because expected rent scales with remaining laps.** A tile bought in lap 1 has 5 laps left to generate rent; one bought in lap 4 has only 2. With 2 other players on an 8-tile board, a specific tile is expected to be hit roughly 1–1.5 times over 5 laps (two players × 5 laps × ~1/8 per tile per lap). So a cheap tile (rent ~10–14) bought in lap 1 has expected rent income of roughly 12–20. That's positive but modest — you're not going to get rich from one tile, but you should still take it.

**Prefer cheap tiles.** Since rent-to-price ratios are roughly flat across the board (~20–25%), the cheapest available tile gives you the same expected yield per tile while preserving more cash for a second purchase. Prioritize Depot (50), Quarry (60), Terrace (70) over Exchange (120) or Foundry (100) when both are available.

**Do not buy on the final lap.** No one will land on a tile you just bought on the last turn. The purchase is a pure no-op. This is absolute.

**Do not buy in lap 5 unless the tile is very cheap (≤50).** You have at most 1 lap of rent collection. Expected income is ~rent × 0.25 (one other player, one lap, 1/8 chance each). For a 50-price tile with rent 10, that's expected income of ~2.5 — barely worth it, but if you have surplus cash it's a small positive.

**Cash management:** After each purchase, ask "can I still afford at least one more cheap property (≤70) if I get the chance?" If yes, buy now. If you're in lap 1–2, be liberal with purchases — you have the most laps to collect rent. In lap 3+, be more selective. In lap 4+, only buy the cheapest available.

**When I land on an owned tile, pay the rent and move on.** No purchase decision arises. This is a pure outflow I cannot avoid.

**When I land on my own tile, nothing happens.** No self-rent. Note that this tile is "safe" from rent-outflow.

**Track the board state each lap.** Note which tiles are unowned, who owns what, and which tiles are high-rent. If one player is accumulating expensive high-rent tiles (Exchange, Foundry), expect to pay them heavily when you land on their tiles. This doesn't change your buying decisions directly, but it helps you model your expected net cash flow.

**Salary at START is a meaningful income source.** It's 25 per pass, and with 6 laps and an 8-tile board, you'll pass START roughly once per lap on average (depending on roll sizes). Budget for it but don't count on it being frequent enough to fund expensive purchases.

**Endgame (laps 5–6):** Stop buying unless it's a 50-price tile and you have surplus cash you won't need. On the very last lap, never buy under any circumstances.

**Recognize that your score is largely determined by rent you avoid paying.** In a game where you pay rent to others but rarely collect rent from them (because you own few tiles), your score is mostly: starting cash + salary income − total rent paid. Purchases are a small positive modifier. Focus on not overpaying and on the occasional lucky purchase that generates rent.