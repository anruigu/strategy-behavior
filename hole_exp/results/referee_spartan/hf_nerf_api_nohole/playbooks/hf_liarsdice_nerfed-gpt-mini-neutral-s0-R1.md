---
game: hf_liarsdice_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 2153
---
When I open and I have at least two of a face (including ones as wild), I bid that quantity at that face fairly conservatively (usually equal to my count, rarely +1).

When I hold two ones, I treat them as one extra of any face for bidding and calling; I count them as wild in my internal totals.

When I have exactly one of a face and no wilds, I avoid opening a bold quantity at that face; open a different face where I have >=2 or open 2×1 if I have two ones.

When a bid would require improbably many of a face across all dice (roughly probability < ~5% given my hand and unknown dice), I call liar.

When a bid is plausible given my hand (e.g., my count plus expected value from unknown dice makes it reasonable), I raise only by quantity, not by switching to an extreme face (avoid jumping to face 6 unless I have supporting dice).

When the current bid matches my strong holding (my count plus ones would already meet it), I raise the quantity by one rather than changing face.

When I have one die of the bid face and few unknown dice remain, I call if the bid requires multiple additional of that face (do not trust an unlikely shortfall).

When the opponent raises to a high face (6) with a modest quantity and I have zero of that face and no wilds, call unless the required quantity is plausible across all unknown dice.

When I have two matching high-value dice (5s or 6s), I may open with 2 of that face but remain conservative about escalating quantity prematurely.

When the table already has a modest bid (2–3) and I have supportive dice (including ones), prefer increasing quantity over switching to much higher faces.

Do not overbluff by making large jumps in quantity or face without multiple supporting dice; such bluffs are often called and cost points.

When the bid is exactly at a borderline probability (near 50% considering my dice + expected unknowns), prefer calling over risky raises if pot score matters.

When challenged, always report my true count succinctly.

When forced into extreme raises (e.g., maxed face paths), avoid committing unless my hand justifies it; calling is better than inflating risk without support.