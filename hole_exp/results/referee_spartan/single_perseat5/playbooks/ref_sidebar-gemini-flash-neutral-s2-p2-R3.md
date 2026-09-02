---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1086
---
# Playbook: Sidebar (One-Card 3-Player Poker)

### Card Strength Benchmarks
* Trash / Weak: 2–9
* Marginal / Bluff-Catcher: 10–11
* Strong Value / Premium: 12–14

---

### Facing a Bet to Me (Bet = 3)

* **When facing a bet with 9 or lower:**
  * Always reply `[bet: fold]`. Opponents bet strong ranges; calling with sub-10 hands is negative EV.

* **When facing a single bet (Pot = 6, Bet = 3):**
  * With 2–10: Reply `[bet: fold]`.
  * With 11 or 12: Reply `[bet: call]`.
  * With 13 or 14: Reply `[bet: raise]` for maximum value against single-bettor ranges.

* **When facing bets/calls from BOTH opponents (Pot = 9, Bet = 3):**
  * With 2–11: Reply `[bet: fold]`.
  * With 12: Reply `[bet: call]`.
  * With 13 or 14: Reply `[bet: raise]`.

---

### Checked / Unopened to Me (Bet = 0, Pot = 3)

* **When holding 11 or lower:**
  * Reply `[bet: call]` to check and take the free showdown. Never bluff weak hands.

* **When holding 12, 13, or 14:**
  * Reply `[bet: raise]` for pure value. Opponents checking before me have capped/weak ranges and will frequently call with worse hands.