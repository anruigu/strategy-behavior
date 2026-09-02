---
game: ta_kuhn
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1553
---
### Kuhn Poker Playbook

**Showdown Declarations**
- When asked to declare my card at showdown, always declare the exact card dealt to me: `[show: jack]`, `[show: queen]`, or `[show: king]`. Never attempt to misdeclare.

---

**Player 1 (Opener) Decisions**

*Holding King:*
- When opening with a King, always bet: `[act: bet]`.
- If checked to after a bet or facing any action with a King, continue to take the maximum value action (call/bet).

*Holding Queen:*
- When opening with a Queen, always check: `[act: check]`. Never open-bet a Queen.
- When facing a bet after checking a Queen, default to folding: `[act: fold]`. Calling down with a Queen against opponent bets has consistently lost chips because opponents bet Kings for value far more often than they bluff Jacks.

*Holding Jack:*
- When opening with a Jack, check: `[act: check]`.
- When facing a bet after checking a Jack, always fold: `[act: fold]`. Never call with a Jack.

---

**Player 2 (In Position / Facing Opener's Action) Decisions**

*Facing an Opener's Bet:*
- Holding King: always call: `[act: call]`.
- Holding Queen: always fold: `[act: fold]`.
- Holding Jack: always fold: `[act: fold]`.

*Facing an Opener's Check:*
- Holding King: always bet for value: `[act: bet]`.
- Holding Queen: always check behind to realize showdown value: `[act: check]`. Do not bet a Queen, as it only gets called by Kings and folds out Jacks.
- Holding Jack: check behind: `[act: check]`. Pure bluff-betting with a Jack into checks consistently gets called down by Queens/Kings and leaks chips.