---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2256
---
### Communication Strategy
- **Establish Honest Sharing Early**: In the opening message to Player 1, propose a strict truthful-reveal protocol to coordinate against Player 2. State my exact numeric card rank every hand and ask them for theirs.
- **Signal Strategic Intent Clearly**:
  - When holding a high card (11–14), state the exact rank and announce my intent to raise.
  - When holding a weak card (2–7), state my rank clearly and state that I plan to check/fold.
  - When Player 1 claims a high card (higher than mine), encourage them to raise against Player 2 while I step aside.
- **Handle Vague Partner Messages**: If Player 1 responds with vague terms (e.g., "mid-range card") instead of exact numbers, assume their card is roughly 7–9 and continue sharing my exact rank clearly to encourage transparency.

### Betting Strategy
- **Acting as First Better (Player 0, current bet is 0)**:
  - **Holding 12–14 (Very Strong)**: Always `[bet: raise]` to extract value from Player 2.
  - **Holding 10–11 (Strong)**:
    - If Player 1 revealed a lower card or vague mid-strength: `[bet: raise]` to build value against Player 2.
    - If Player 1 revealed a higher card (12+): `[bet: call]` to check and let Player 1 drive the action.
  - **Holding 2–9 (Weak / Marginal)**: Always `[bet: call]` (check for free). Never open-raise with marginal or low cards out of position.

- **Facing a Raise (when current bet > 0)**:
  - **Holding 13–14**: `[bet: call]` (or raise if allowed) to contest the pot.
  - **Holding 11–12**:
    - `[bet: call]` only if Player 1 has folded/weak and Player 2 raised without Player 1 contesting.
    - `[bet: fold]` if facing heavy action where Player 1 or Player 2 clearly holds top-end strength (13–14).
  - **Holding 2–10**: Always `[bet: fold]`. Never pay 2 extra chips to call a raise with weak/marginal holdings.

### Mistakes to Avoid
- Never call a raise with low or mid cards (2–10); calling raises without high-tier cards severely drains chip totals.
- Avoid sending ambiguous messages like "I have a mid card"; always specify the exact numeric rank to ensure optimal joint decisions.
- Do not raise out of position with mediocre cards (7–9) hoping to steal; Player 2 frequently calls or raises with superior hands.