---
game: ta_liarsdice
model: qwen
condition: neutral
seed: 0
round: 2
chars: 741
---
**Opening bids**
- When I open, I bid quantity 2 on the lowest face where my effective count is ≥2. If no face has count ≥2, open quantity 1 on the highest face I hold.
- When behind by ≥4 chips, open at quantity 3 on the lowest face with effective count ≥3 (aggressive); if no such face, quantity 2.
- When ahead by ≥4 chips, open at quantity 1 on a face I hold (tight).

**Response to opponent's bid QxF (effective count c of face F, counting wild 1s for F≠1):**
- c ≥ Q: The bid is met by my hand alone. RAISE to (Q+1)xF. If a different face G has effective count ≥ Q+1, prefer to raise to (Q+1)xF still (keep it simple, stay on same face). Never call here—bid is true so calling guarantees my loss.
- c = Q−1 (opponent needs 1): PIVOT to