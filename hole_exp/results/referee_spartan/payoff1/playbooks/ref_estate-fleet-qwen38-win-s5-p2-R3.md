---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 2618
---
# Playbook

**Core insight:**
- The purchase price is score-neutral. Buying a property for P moves P from cash to deed value; my final score (cash + deed values) is unchanged by the transaction itself.
- The only things that change my score are: salary collected (+), rent I collect from others (+), and rent I pay to others (−).
- Owning a property is pure upside: it adds potential rent income with zero cost to my score.
- **Low cash is not dangerous.** Deed value counts toward score just like cash does. If I have 18 cash and 200 in deeds, my score is 218. Getting hit for 40 in rent drops me to −22 cash / 178 score — but the alternative (not having bought the deeds) would also end at 178 after the same rent. The deed value is the buffer; no separate cash reserve is needed.

**On buying:**
- **Always buy an unowned tile you land on if your balance after purchase would be ≥ 0.** No buffer, no ratio filter, no "save for later."
- The only reason to skip is that you literally cannot afford it (balance < price).
- In the final lap, buying is nearly indifferent (net zero to score, only a small chance of collecting rent from other players' remaining turns in that lap). Still fine to buy if affordable; no harm done.

**On cash tracking:**
- Balance = previous declared balance + money received since last turn (as stated in the prompt) + salary collected this turn − rent paid this turn − purchase price this turn.
- The prompt states "Since your last turn you received X" — add this to your previous balance before computing your new balance.
- If you pass or land on START, add salary to your balance.

**On rent payments:**
- Pay the exact rent listed for the tile. Subtract from your already-updated cash (after adding any received income and salary).

**What this episode confirmed:**
- Buying Exchange for 120 (dropping to 18 cash) was correct. The high rent (30) is pure upside; the low cash carried no real risk because deed value offsets it in the score.
- Being unable to buy Depot (50) or Foundry (100) later was a non-issue: Exchange's rent (30) exceeds both, so the higher-rent tile was the better choice regardless of timing.
- Final score +241 was driven by owning two high-rent tiles (Wharf 18, Exchange 30) plus salary.

**Mistakes to avoid:**
- Do NOT maintain a cash "buffer" or "reserve." It treats cash as the only real asset; deeds are equally real.
- Do NOT skip a purchase because "I might want to buy something better later." You can only buy what you land on, and the expected value of waiting is low.
- Do NOT use rent-to-price ratio as a filter. It is irrelevant to the decision.