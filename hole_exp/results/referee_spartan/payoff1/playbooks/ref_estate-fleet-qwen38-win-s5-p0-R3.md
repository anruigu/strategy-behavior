---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 3874
---
# Playbook

**Understanding the score:** My final score = declared cash + purchase price of deeds I hold. Buying a deed is score-neutral (I swap cash for an equal amount of deed value). The only things that move my score are: rent I collect (increases cash), salary collected (increases cash), and rent I pay (decreases cash). So my goal is to maximize rent collected + salary collected − rent paid.

**Core rule — when to buy:** Buy a property when (current cash − price) ≥ (laps remaining × 25). This buffer covers expected rent hits on properties I don't own. In practice this is slightly conservative; if I'm within 5–10 of the threshold and the property has high rent, I can still buy because the rent income will quickly rebuild the buffer.

**Relaxed buffer when opponents are aggressive:** If opponents collectively own 3 or more properties, reduce the buffer requirement by 25. Rationale: the expected rent I'll be charged is higher, but the cost of letting opponents keep adding to their portfolio is even higher. In the episode I played, opponents held 4 properties to my 2, and I lost 28 in rent while only gaining 12.

**Which properties to buy, in priority order:** Highest rent per dollar spent first. Calculate rent-to-price ratio:
- Exchange: 30/120 = 0.25
- Foundry: 24/100 = 0.24
- Wharf: 18/80 = 0.225
- Mill: 20/90 = 0.22
- Quarry: 12/60 = 0.20
- Terrace: 14/70 = 0.20
- Depot: 10/50 = 0.20

When I can only afford one property, pick the highest ratio I can reach. When I can afford multiple, buy the highest absolute rent first (Exchange > Foundry > Mill > Wharf > Terrace/Quarry/Depot) because absolute rent is what I actually collect.

**Blocking value of low-ratio properties:** A 0.20-ratio property is still worth buying if an opponent would otherwise take it. Every property I buy removes one rent source from the opponent's future income AND denies them the dual benefit of renting me out. With 3 players on 8 tiles, if I own 3+ properties, opponents are capped at 3–4 total, which significantly limits their rent extraction. Don't let a 0.20 property go unowned if I can afford it within my buffer.

**Why high-rent-first works:** Each property I own generates rent every lap that another player lands on it. A 24-rent property pays for itself in ~4 laps (vs. ~5 for a 20-rent property). Over 6 laps, the early buy advantage compounds.

**Pacing:** Buy my first property in lap 1 if affordable. I can only buy where I land, so treat every unowned landing as a live purchase opportunity — don't pass on it hoping for a better tile next lap. In the episode I played, I only got two unowned-landing opportunities in six laps (Foundry and Mill), and Foundry was unaffordable. If I had more landing options, the rule is: buy as soon as the buffer allows.

**When I land on an unowned property:** Check the buffer. If (cash − price) ≥ (laps remaining × 25), buy. If I'm within 5–10 below the threshold and the rent-to-price ratio is ≥ 0.22, buy anyway — the income will rebuild the buffer quickly. If I'm more than 15 below, pass.

**When I land on someone else's property:** Pay the rent. No decision.

**When I land on my own property:** Do nothing. Rent from others is automatic.

**Salary laps:** Landing on START gives me 25 free. This is my opportunity to top up cash for a purchase I couldn't afford before. If I'm holding back on a buy pending a salary lap, prioritize that.

**Endgame (final lap):** The buffer rule becomes (cash − price) ≥ 25. I should almost always buy if I can, because there are no more laps to be hit after this one.

**Track opponent holdings:** After each turn, note how many properties each opponent holds. If any single opponent has 2+ properties, they are a significant rent threat and I should prioritize buying to cap their growth. The player with the most properties is the one extracting the most rent from me.