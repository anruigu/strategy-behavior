---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2391
---
# Playbook: 3-Player One-Card Poker with Private Line

## Private Line Messaging Strategy
- When messaging Player 0, never reveal true top cards (12–14) accurately if it discourages them from betting or putting chips into the pot; feign medium strength or vague cooperation ("holding mid-range / let's see what happens").
- When holding a weak card (2–6), send vague, cooperative, or slightly inflated signals ("holding mid-range around 7–9") to discourage opportunistic aggression from Player 0 while giving away zero reliable tactical info.
- When holding a medium card (7–11), give vague cooperative responses ("decent mid-range, let's keep it cheap").
- Treat Player 0's private messages as informative but self-interested: if Player 0 claims a monster card (12–14) and backs it up with a raise, respect the high card range; if Player 0 claims weakness (2–6), factor in potential check-raising or passive survival.

## Betting Strategy (Seat 1: Middle Position)

### When Facing No Bet (Current Bet = 0, Pot = 3)
- If holding **12–14**: choose `[bet: raise]` to extract value from callers and build pot size.
- If holding **10–11**:
  - Choose `[bet: raise]` if Player 0 indicated weakness or checked, and I want to isolate or price out Player 2.
  - Choose `[bet: call]` to check through if keeping the pot small is preferable or to let Player 2 bluff.
- If holding **2–9**: always choose `[bet: call]` (check for free). Never bluff-raise with low cards out of position when Player 2 acts behind.

### When Facing a Raise (Current Bet = 3, Pot = 6+)
- If holding **13–14**: choose `[bet: call]`.
- If holding **11–12**:
  - Choose `[bet: call]` if Player 0's raising history is loose or if facing an isolated bet with good odds.
  - Choose `[bet: fold]` if Player 0 explicitly communicated high strength (13–14) and their past reveals show truthful play, or if Player 2 has already called/raised.
- If holding **2–10**: always choose `[bet: fold]`. Do not pay 3 chips to contest pots with marginal or weak holdings against demonstrated aggression.

## General Tournament Dynamics
- On the final hands (Hands 7–8), evaluate the chip standing:
  - If holding a positive chip lead, play conservative poker—strictly check behind on marginal cards (7–10) and fold immediately to raises with anything below 12.
  - Continue to bet/raise top cards (13–14) for maximum value regardless of lead.