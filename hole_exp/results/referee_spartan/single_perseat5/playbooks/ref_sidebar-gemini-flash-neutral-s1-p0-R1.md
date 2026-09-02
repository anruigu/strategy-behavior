---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1642
---
### Communication Strategy
- On every private messaging turn, explicitly state my exact card number and propose a clear, simple plan: if my card is higher, I will raise and Player 1 should fold (or call to trap Player 2 if strong); if Player 1's card is higher, I will check/call or fold to let them take the lead.
- Never send vague pleasantries or generic "let's coordinate" messages; always provide actionable numeric information.

### Card Evaluation & Betting Thresholds
- Treat card ranks strictly by probability (cards run 2 to 14, midpoint is 8):
  - **Premium (12–14):** Always open with `[bet: raise]`. If raised before me, always call or reraise.
  - **Medium-High (9–11):** 
    - If opening (bet is 0) and Player 1 reports a lower card, `[bet: raise]` to pressure Player 2.
    - If Player 1 reports a higher card, `[bet: call]` (check) and yield the pot to Player 1 if contested.
    - If facing a raise from Player 2, call only with 10–11; fold 9 unless pot odds heavily favor a call.
  - **Mediocre/Low (2–8):**
    - Never treat 7 or 8 as a strong or high card; never raise on 7 or 8 as a bluff or value bet.
    - When bet to me is 0, check with `[bet: call]`.
    - When facing any raise from an opponent, immediately `[bet: fold]`. Do not bleed chips by calling raises with cards 8 or below.

### Coalition Play Against Player 2
- If Player 1 reports a monster hand (12–14), check if bet is 0 and fold if Player 2 raises, keeping costs minimal and allowing Player 1 to extract chips from Player 2.
- If both Player 1 and I hold weak cards (≤7), check down with `[bet: call]` if free, but fold immediately if Player 2 bets.