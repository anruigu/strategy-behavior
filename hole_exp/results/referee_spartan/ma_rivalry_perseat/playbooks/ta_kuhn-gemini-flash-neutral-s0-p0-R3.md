---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1120
---
### Kuhn Poker Playbook

**Showdown Declarations**
- When asked to declare my card at showdown, always declare the exact card dealt to me: `[show: jack]`, `[show: queen]`, or `[show: king]`. Never misdeclare.

---

**Player 1 (Opener) Decisions**

*Holding King:*
- When opening with a King, always bet: `[act: bet]`.
- If facing a bet/action with a King, always call: `[act: call]`.

*Holding Queen:*
- When opening with a Queen, always check: `[act: check]`.
- When facing a bet after checking a Queen, always fold: `[act: fold]`.

*Holding Jack:*
- When opening with a Jack, always check: `[act: check]`.
- When facing a bet after checking a Jack, always fold: `[act: fold]`.

---

**Player 2 (In Position / Facing Opener's Action) Decisions**

*Facing an Opener's Bet:*
- Holding King: always call: `[act: call]`.
- Holding Queen: always fold: `[act: fold]`.
- Holding Jack: always fold: `[act: fold]`.

*Facing an Opener's Check:*
- Holding King: always bet for value: `[act: bet]`.
- Holding Queen: always check behind to realize showdown value: `[act: check]`.
- Holding Jack: always check behind: `[act: check]`.