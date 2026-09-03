---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 2117
---
### Playbook: Settlement & Road Exchange

#### 1. Goal and Valuation
* Prioritize settlements (3 points for 1 wood + 1 brick + 1 grain + 1 ore) over roads (1 point for 1 wood + 1 brick).
* Always track the exact combination of resources needed to build a settlement on the current turn. Treat missing ingredients as strictly higher value than surplus resources.

#### 2. Offering Phase
* If I am missing a resource needed for a settlement:
  * Find an opponent who holds at least 1 (preferably $\ge 2$) of my missing resource.
  * Offer 1 of my surplus resources ($\ge 2$ copies, or a non-essential resource if no build is otherwise possible) to get 1 of the missing resource: `[offer: to P<k>, give 1 <surplus>, get 1 <needed>]`.
* If I already have a full settlement set (1W, 1B, 1G, 1O) for this turn:
  * If in round 5/5, post `[offer: none]`.
  * In rounds 1–4, if I hold a surplus ($\ge 2$) of one resource and lack surplus in another, post a trade to acquire resources for upcoming rounds (`[offer: to P<k>, give 1 <surplus>, get 1 <scarce>]`), provided giving it away does not disrupt my immediate settlement build.
* Never offer a resource if it drops my count below 1 when that resource is needed for an immediate build this round.

#### 3. Trading / Acceptance Phase
* Accept an incoming trade (`[accept: P<k>]`) if:
  1. It grants a resource I need to complete a settlement (or road if settlement is out of reach), AND
  2. It does not surrender a resource I need for that same build (i.e. only give away what I have $\ge 2$ of, or what isn't needed for the target build).
* Reject (`[accept: none]`) any offer that gives away a bottleneck resource or disrupts a guaranteed settlement.
* Reject offers from the point leader if the trade would enable them to build a settlement, unless it also immediately enables a settlement for me on a critical or final round.

#### 4. Building Phase
* If I hold $\ge 1$ wood, $\ge 1$ brick, $\ge 1$ grain, and $\ge 1$ ore: output `[build: settlement]`.
* Otherwise, if I hold $\ge 1$ wood and $\ge 1$ brick: output `[build: road]`.
* Otherwise: output `[build: none]`.