---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1180
---
# Playbook: Sidebar (One-Card 3-Player Poker)

### Card Strength Benchmarks
* Low / Trash: 2–9
* Marginal / Medium: 10–11
* Strong Value: 12–14

---

### Facing a Bet to Me (Bet = 3)

* **When facing a bet with a card of 9 or lower:**
  * Always reply `[bet: fold]`. Calling with medium or weak cards (like 9 or 8) against active bets is a leak; opponents' betting ranges are too strong.

* **When facing bets from BOTH opponents (Pot = 9, Bet = 3):**
  * With 10 or 11: Reply `[bet: fold]`. The requirement to beat two callers/bettors severely depresses hand equity.
  * With 12: Reply `[bet: call]`.
  * With 13 or 14: Reply `[bet: raise]` to extract maximum value.

* **When facing a single bet (Pot = 6, Bet = 3):**
  * With 10 or lower: Reply `[bet: fold]`.
  * With 11 or 12: Reply `[bet: call]`.
  * With 13 or 14: Reply `[bet: raise]`.

---

### Checked / Unopened to Me (Bet = 0, Pot = 3)

* **When holding 11 or lower:**
  * Reply `[bet: call]` (take the free showdown). Never turn weak hands into bluffs.

* **When holding 12, 13, or 14:**
  * Reply `[bet: raise]` every time. Opponents who checked rarely have premium holdings and will often pay off with medium cards.