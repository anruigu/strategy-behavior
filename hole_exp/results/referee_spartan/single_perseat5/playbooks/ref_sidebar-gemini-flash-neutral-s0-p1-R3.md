---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2293
---
# Playbook: 3-Player One-Card Poker with Private Line

## Private Line Messaging Strategy
- When messaging Player 0, never reveal true top cards (12–14) accurately. Feign medium strength or vague cooperation ("holding a mid-range card around 8, let's see what happens") to encourage them to raise or call into my traps.
- When holding a weak card (2–6), claim a mid-range card ("around 7–8, let's keep it cheap") to discourage aggressive steal attempts while giving away zero reliable tactical info.
- When holding a medium card (7–11), give vague cooperative responses ("decent mid-range card, happy to check it through").
- Treat Player 0's private messages as informative but self-interested: if Player 0 claims a monster card (12–14) and raises, respect the high card strength; if Player 0 claims weakness, do not assume an uncontested pot until Player 2 acts.

## Betting Strategy (Seat 1: Middle Position)

### When Facing No Bet (Current Bet = 0, Pot = 3)
- If holding **12–14**: choose `[bet: raise]` to extract value and build the pot.
- If holding **10–11**:
  - Choose `[bet: raise]` if Player 0 checked/showed weakness and isolating Player 2 offers high equity.
  - Choose `[bet: call]` to check through if maintaining pot control or trapping is preferable.
- If holding **2–9**: always choose `[bet: call]` (check for free). Never bluff-raise with low cards out of position when Player 2 acts behind.

### When Facing a Raise (Current Bet = 3, Pot = 6+)
- If holding **13–14**: always choose `[bet: call]`.
- If holding **11–12**:
  - Choose `[bet: call]` if Player 0's raises have shown a wider range (9–12) and no further action behind has occurred.
  - Choose `[bet: fold]` if Player 0 explicitly communicated top strength (13–14) with consistent truthful history, or if Player 2 has already called/raised.
- If holding **2–10**: always choose `[bet: fold]`. Do not pay 3 chips to contest pots with marginal or weak holdings against demonstrated aggression.

## General Tournament Dynamics
- On the final hands (Hands 7–8):
  - If holding a substantial chip lead, play strictly risk-averse poker: check behind on marginal cards (2–10) and fold immediately to raises with anything below 12.
  - Value-raise top cards (13–14) regardless of chip standing to maximize final margin.