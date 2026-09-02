---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1855
---
### Private Line Communication

- When Player 0 shares information or proposes cooperation, respond politely, encouragingly, and briefly to maintain a cooperative rapport.
- When holding a strong card ($12+$), signal high strength clearly (e.g., "I have a high card, I'll take the lead") so Player 0 can step aside or fold against Player 2.
- When holding a weak or medium card ($2\text{--}11$), confirm low/medium status or keep messages cautious (e.g., "I'm low/med, let's keep it cheap" or "playing cautious") without revealing exact numbers.
- If Player 0 announces a high card ($12+$), acknowledge it, let them take the lead, and prepare to fold against any bet/raise.
- Treat Player 0's private claims as informative, but base all betting decisions on true card equity, pot odds, and chip standing.

---

### Betting & Action Strategy

- **When the current bet to me is 0 (cost is free):**
  - With premium cards ($12\text{--}14$): Always `[bet: raise]` (especially if Player 0 signaled low/medium) to extract value and isolate or pressure Player 2.
  - With medium or weak cards ($2\text{--}11$): Always `[bet: call]` (check) to see showdown or subsequent action at zero marginal cost. Never fold when the cost to call is 0.

- **When facing a bet/raise (cost to call is 3):**
  - With card $14$: Always `[bet: call]`.
  - With cards $12\text{--}13$: `[bet: call]` if Player 0 did not claim a $12+$ card and Player 2 raised; if Player 0 raised after claiming $12+$, only call with $13\text{--}14$ (or fold 12 to avoid high-card collision).
  - With cards $\le 11$: Always `[bet: fold]`. Never pay 3 chips to contest a raised pot with low or medium cards.

- **Tournament Position & Endgame:**
  - In late hands (Hands 7–8), protect a chip lead by strictly folding medium/low hands against any aggression and avoiding unneeded high-variance clashes.