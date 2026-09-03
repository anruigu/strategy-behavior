---
game: ref_estate
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3362
---
# Playbook for ESTATE

**Scoring:** Final score = cash + purchase prices of deeds held. Buying a property at its listed price is cash-neutral at the whistle — the real gain is the rent it collects along the way, and denying it to rivals. Never buy purely to "convert cash to assets"; buy for rent income and denial. My Wharf (80) and Exchange (120) buys both counted at full price at the end and collected rent en route, so the scoring rule held up exactly as written.

**Early-lap buying rule:** When I land on an unowned property early (laps 1–3) and it's affordable with cushion, buy it — rent streams accumulate over remaining laps and opponents will otherwise buy it and charge me. Wharf lap 1 was clearly right. But note the affordability trap that actually happened: after buying Exchange on lap 2 I was down to 36 cash and could not buy Depot (50) on lap 3, plus I didn't pass START until lap 4. **New cushion rule:** after any buy, I want enough left to cover (a) likely rent hits before my next salary (~20–30) and (b) the cheap unowned tiles (50-range) I might land on. Two big early buys back-to-back starved me. If a second early buy would leave me under ~50, consider deferring it — one strong property plus liquidity beats two properties and no cash.

**Don't overextend late:** On the final lap, buying an unowned property is usually pointless — no time for it to earn rent, and the price returns dollar-for-dollar in score. My lap-6 no-buy on Mill was right (and I couldn't afford it anyway at 55).

**Track my balance carefully.** Always include salary (25 per START pass) AND transfers received since my last turn before declaring. Do the arithmetic explicitly in writing: previous balance + salary + transfers received − payments out. This game the arithmetic was clean every turn (36 + 25 = 61; 61 − 24 = 37; 37 + 18 = 55) — keep that discipline. The "transfers received" line in the prompt is easy to skim past; read it every time and fold it in before declaring.

**When I land on someone's property:** Pay the rent, declare honestly, no agonizing. Paying 24 (Foundry) went smoothly.

**When I can't afford a buy:** Declare no purchase cleanly and move on; don't count on future income I haven't received. The Depot pass at 36 < 50 was handled correctly.

**Priority order for purchases when money is limited:** Prefer high rent-to-price properties first, and prefer properties rivals are likely to land on. Wharf (18/80 = 22.5%) and Exchange (30/120 = 25%) were both good on this logic. Denying a strong property to a leader matters more than grabbing a weak one. Cheap tiles (Depot 50, Quarry 60) are efficient rent-per-cash and good liquidity-preserving picks.

**Watch the rivals' books too:** The transfer log tells me who owns what and who is bleeding rent. Investor 0 grabbed Quarry and Foundry and was collecting steadily; investor 1 spread across Terrace and Depot. If one investor is pulling ahead on rent income, lean toward buying anything that denies them landing revenue, even at a thinner ratio — subject to the cushion rule above.

**General default:** When a settle prompt is put to me, I pay what's due, buy only if affordable with cushion and strategically worthwhile, recompute my balance from scratch (last declared + salary + transfers received − payments), and end with the exact bracketed tokens: pay, buy, balance.