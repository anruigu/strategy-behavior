---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1823
---
### Private Line Communication

- When Player 0 shares information or proposes cooperation, respond politely, encouragingly, and briefly to maintain a cooperative rapport.
- When holding a strong card ($12+$), signal strength clearly (e.g., "I have a high card, I'll take the lead") so Player 0 can step aside or support pot building against Player 2.
- When holding a weak or medium card ($2\text{--}11$), keep messages vague or understated (e.g., "keeping it cheap" or "playing cautious") without revealing exact numbers.
- If Player 0 announces a high card ($12+$), acknowledge it, let them take the lead, and prepare to fold or stay cheap.
- Treat Player 0's private claims as informative, but base all betting decisions on true card equity and pot odds.

---

### Betting & Action Strategy

- **When the current bet to me is 0 (cost is free):**
  - With premium cards ($12\text{--}14$): If I communicated intent to take the lead or if Player 0 signaled low/medium, `[bet: raise]` to extract value and pressure Player 2. Do not check premium hands when planning to take the lead.
  - With medium or weak cards ($2\text{--}11$): Always `[bet: call]` (check) to see showdown or subsequent action at zero marginal cost.

- **When facing a bet/raise (cost to call is 3):**
  - With cards $13\text{--}14$: `[bet: call]` (or `[bet: raise]` if possible) for value.
  - With card $12$: `[bet: call]` only if Player 0 did not claim a $12+$ card and Player 2 raised, or if pot odds strongly favor it; otherwise fold to heavy strength.
  - With cards $\le 11$: `[bet: fold]`. Never pay 3 chips to contest a raised pot with medium or low cards.

- **Tournament Position & Endgame:**
  - In late hands (Hands 7–8), avoid marginal risk if chips are close or leading. Fold medium hands instantly against bets and check down free pots.