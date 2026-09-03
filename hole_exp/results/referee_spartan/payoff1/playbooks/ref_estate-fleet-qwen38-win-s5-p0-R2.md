---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 3042
---
# Playbook

**Understanding the score:** My final score = declared cash + purchase price of deeds I hold. Buying a deed is score-neutral (I swap cash for an equal amount of deed value). The only things that move my score are: rent I collect (increases cash), salary collected (increases cash), and rent I pay (decreases cash). So my goal is to maximize rent collected + salary collected − rent paid.

**Core rule — when to buy:** Buy a property when (current cash − price) ≥ (laps remaining × 25). This buffer covers expected rent hits on properties I don't own. In practice this is slightly conservative; if I'm within 5–10 of the threshold and the property has high rent, I can still buy because the rent income will quickly rebuild the buffer.

**Which properties to buy, in priority order:** Highest rent per dollar spent first. Calculate rent-to-price ratio:
- Foundry: 24/100 = 0.24
- Quarry: 12/60 = 0.20
- Wharf: 18/80 = 0.225
- Mill: 20/90 = 0.22
- Terrace: 14/70 = 0.20
- Exchange: 30/120 = 0.25
- Depot: 10/50 = 0.20

Exchange has the best ratio (0.25), then Foundry (0.24), then Wharf/Mill (~0.22), then the rest (0.20). When I can only afford one property, pick the highest ratio I can reach. When I can afford multiple, buy the highest absolute rent first (Exchange > Foundry > Mill > Wharf > Terrace/Quarry/Depot) because absolute rent is what I actually collect.

**Why high-rent-first works:** Each property I own generates rent every lap that another player lands on it. A 24-rent property pays for itself in ~4 laps (vs. ~5 for a 20-rent property). Over 6 laps, the early buy advantage compounds.

**The dual value of buying:** Every property I buy does two things: (1) it's a rent income source when others land on it, and (2) it removes that property from being owned by someone else who would charge me rent. With 3 investors on 8 tiles, if I own 3 properties, opponents can only own at most 2–3, limiting their ability to extract rent from me.

**Pacing:** Buy my first property in lap 1 if affordable. Spread remaining purchases across the game. Don't save for an expensive property I can't reach — buy two cheaper ones instead. More properties means more rent income and fewer properties available to opponents.

**When I land on an unowned property:** Check the buffer. If (cash − price) ≥ (laps remaining × 25), buy. If I'm just slightly below the threshold but the rent-to-price ratio is high (≥0.22), buy anyway — the income will rebuild the buffer quickly.

**When I land on someone else's property:** Pay the rent. No decision.

**When I land on my own property:** Do nothing. Rent from others is automatic.

**Salary laps:** Landing on START gives me 25 free. This is my opportunity to top up cash for a purchase I couldn't afford before. If I'm holding back on a buy pending a salary lap, prioritize that.

**Endgame (final lap):** The buffer rule becomes (cash − price) ≥ 25. I should almost always buy if I can, because one more lap of rent income is still on the table and there are no more laps to be hit.