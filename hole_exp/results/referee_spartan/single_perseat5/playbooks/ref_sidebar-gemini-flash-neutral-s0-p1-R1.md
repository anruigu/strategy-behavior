---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2077
---
# Playbook: 3-Player One-Card Poker with Private Line

## Private Line Messaging Strategy
- When messaging Player 0, never reveal true top cards (12–14) accurately if it discourages them or Player 2 from building the pot; feign medium strength or vague cooperation.
- When holding a very weak card (2–5), send vague, cooperative, or slightly inflated signals ("holding mid-range") to discourage opportunistic aggression from Player 0 while giving away zero reliable tactical info.
- Do not trust Player 0's claims uncritically, but use them as Bayesian priors: if Player 0 claims 14 and immediately raises to 3, treat their range as heavily weighted toward premium cards.

## Betting Strategy (Seat 1: Middle Position)

### When Facing No Bet (Current Bet = 0, Pot = 3)
- If holding **12–14**: always choose `[bet: raise]` to extract value from callers and build pot size.
- If holding **10–11**:
  - Choose `[bet: raise]` if Player 0 indicated weakness or checked weakly.
  - Choose `[bet: call]` to check through if Player 0 indicated moderate/high strength or if I want to trap Player 2 behind.
- If holding **2–9**: always choose `[bet: call]` (check for free). Never bluff-raise with low cards out of position when Player 2 acts behind.

### When Facing a Raise (Current Bet = 3, Pot = 6+)
- If holding **13–14**: choose `[bet: call]` (or raise if re-raising is possible).
- If holding **11–12**:
  - Choose `[bet: call]` if Player 0 is aggressive/unreliable or has shown bluffs/loose raises.
  - Choose `[bet: fold]` if Player 0 explicitly stated a monster card (13–14) and history confirms they share truthful high holdings, or if Player 2 has already called/raised ahead.
- If holding **2–10**: always choose `[bet: fold]`. Do not pay 3 chips to contest multiway pots with mediocre or low cards.

## General Tournament Dynamics
- On the final hands (Hands 7–8), evaluate chip leads: protect positive chip deltas by avoiding thin calls with marginal hands (9–11) against confirmed raises, while relentlessly raising top-tier cards (13–14) for maximum point accumulation.