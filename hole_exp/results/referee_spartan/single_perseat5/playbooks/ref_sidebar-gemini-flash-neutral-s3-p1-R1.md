---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1804
---
### Private Line Communication

- When Player 0 shares information or proposes cooperation, respond politely, encouragingly, and briefly to maintain a cooperative rapport.
- When holding a strong card ($12+$), signal strength on the private line (e.g., "I have a strong card, let's build the pot") to coordinate extracting chips from the third player.
- When holding a weak or medium card ($2\text{--}11$), keep private line messages vague or understated (e.g., "keeping it cheap" or "cautious") without revealing exact low numbers that invite easy bluffs.
- Treat Player 0's private claims as informative but verify them against their actual betting actions; do not sacrifice chips purely based on unverified trust.

---

### Betting & Action Strategy

- **When the current bet to me is 0 (cost is free):**
  - Always `[bet: call]` (check) regardless of card strength, even with lowest cards ($2\text{--}4$), to see the showdown or subsequent action at zero marginal cost.
  - When holding premium top cards ($13\text{--}14$) and no bet has been made, use `[bet: raise]` to extract maximum value from the field.

- **When facing a bet or raise (cost to call is 3):**
  - With cards $13\text{--}14$: `[bet: raise]` (or `[bet: call]` if capped) to build the pot against worse holdings.
  - With cards $11\text{--}12$: `[bet: call]` if the pot odds justify it or if Player 0 indicated a weaker range, but avoid raising unless confident Player 2 is weak.
  - With cards $\le 10$: `[bet: fold]`. Do not pay 3 chips to chase showdowns with medium or low cards against demonstrated aggression.

- **Defending a Chip Lead:**
  - In late hands (Hands 7–8) when holding a substantial chip lead, tighten call ranges against bets to protect the margin; fold borderline hands ($8\text{--}10$) immediately to any bet.