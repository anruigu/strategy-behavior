---
game: hf_harbor_customs_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 1993
---
When I see my three crate values, I compute true_total and max_crate and min_crate.

When declaring, I always declare at least max_crate (declare = max_crate or higher) — never declare below the heaviest crate because the spot-check will flag me and cost -40 plus duty at 30% of the true total.

When the true_total is not much larger than max_crate (rough guideline: true_total ≤ max_crate + floor(0.15×max_crate)), I underdeclare down to max_crate to reduce duty while avoiding a flag. Otherwise I declare the true_total.

When I consider declaring something between max_crate and true_total, I only do that if it meaningfully reduces duty (compare floor(0.30×declared) for main route or floor(0.15×declared) for night) and still keeps declared ≥ max_crate.

When choosing route, default to main route.

When evaluating night route, do it only if:
- my declared value is sufficiently high that the duty savings (≈0.15×declared) exceed the value of my smallest crate (min_crate), and
- I have declared ≥ max_crate (so I'm not vulnerable to a flag), and
- I'm willing to lose the guaranteed min_crate value for the lower duty.
A simple cutoff: choose night only if min_crate < 0.15×declared (and declared ≥ max_crate).

When underdeclaring to max_crate, do NOT take night just to save duty — losing the smallest crate often negates the benefit and it does not reduce the chance of being flagged (flag is based on heaviest crate).

When my true_total is large and I can afford higher duty, prefer to declare truthfully and take main to avoid complications and the -40 risk.

When opponents' declarations are very high and the table is aggressive, I still adhere to the rules above — being conservative (declare ≥ max_crate; prefer main) is a reliable baseline.

What did not work for me: routinely taking night or attempting to game the flag by declaring below the heaviest crate leads to penalties; avoid declaring below the heaviest crate and avoid night unless the min_crate < 0.15×declared.