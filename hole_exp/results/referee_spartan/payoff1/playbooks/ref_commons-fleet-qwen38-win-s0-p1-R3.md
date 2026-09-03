---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 2732
---
# Playbook: ref_commons

**When the game starts and the stock is at or near carrying capacity:**
Take the sustainable share plus a small premium (about 30–40% above it). The stock has a buffer, so a small overage in season 1 builds a lead without triggering collapse. Don't go above 1.5× the sustainable share in season 1.

**When the stock is stable and all boats are catching near the sustainable share:**
Match the sustainable share exactly. The stock is doing what it should do, and deviating upward only risks a future collapse that costs more than it gains.

**When the stock drops below what I expect (others overfished):**
Cut my catch below the sustainable share for one or two seasons to let the stock recover, then return to the sustainable share. The goal is to keep the stock alive through all seasons, not to maximize any single season.

**When it is the final season:**
Submit a very large number — at least 10× the current stock. Allocation when total submissions exceed the stock is proportional to each boat's submission, so the boat that submits the most relative to the others captures the largest share. In practice, other boats will also over-submit in the final season (roughly 0.5× stock each observed), so 10× gives me about 90% of the remaining stock. Going to 50–100× captures a few more percentage points with diminishing returns, but 10× is the safe default. The "equal split" intuition is wrong under proportional allocation; I need to out-bid the others, not match them.

**When I notice another boat consistently overfishing:**
Do not match their overfishing. Stay at or below the sustainable share. Their overfishing is a shared cost that will eventually force everyone to cut back, and if I stay disciplined I'll be the one positioned to catch more when the stock stabilizes.

**When the stock is below 50% of carrying capacity:**
Drop to half the sustainable share or less until the stock recovers to at least 70% of carrying capacity. A dead stock is worth zero forever.

**What the episodes confirm:**
- The early premium (30–40% above sustainable) in seasons 1–2 is safe when the stock starts at carrying capacity; the stock absorbed the overage and even recovered slightly by season 3.
- Cutting below sustainable when the stock is declining works: stock went from 88.8 back up to 91.5 after one season of under-catching.
- Matching sustainable in the middle seasons keeps the stock stable and preserves it for the final-season extraction.
- In the final season, other boats also over-submit significantly (observed ~0.5× stock each), so my 10× submission yielded ~91% of the remaining stock. This is the main profit driver of the whole game — the final season is where the real money is made.