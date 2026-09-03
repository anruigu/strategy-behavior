---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1784
---
### Playbook: Settlement & Road Exchange

#### 1. Goal and Valuation
* Prioritize settlements (3 points for 1W + 1B + 1G + 1O) over roads (1 point for 1W + 1B).
* Always calculate the exact combination of resources needed to build a settlement on the current turn. Treat missing ingredients as strictly higher value than any surplus resource.

#### 2. Offering Phase
* Look at my holdings and find the bottleneck resource(s) preventing a settlement (or road if settlement is impossible).
* Identify an opponent who holds a surplus ($\ge 2$) of my missing resource and lacks a resource I have in surplus ($\ge 2$).
* Post an offer: give 1 of my surplus resource to get 1 of my missing resource (`[offer: to P<k>, give 1 <surplus>, get 1 <needed>]`).
* Never offer a resource if it reduces my count of that resource below 1 when I need it for a build this turn.
* If no trade can enable a build or improve resource balance toward a 4-resource set, post `[offer: none]`.

#### 3. Trading / Acceptance Phase
* Accept an incoming trade (`[accept: P<k>]`) if and only if:
  1. It grants a resource I lack to complete a settlement (or road), AND
  2. It does not surrender my last copy of a resource required for that same build.
* Reject (`[accept: none]`) any offer that trades away a bottleneck resource or simply swaps one surplus for another surplus without enabling a build.
* Reject offers from the point leader if the trade would enable them to build a settlement, unless it also immediately enables a settlement for me on the final rounds.

#### 4. Building Phase
* If I hold $\ge 1$ wood, $\ge 1$ brick, $\ge 1$ grain, and $\ge 1$ ore: output `[build: settlement]`.
* Otherwise, if I hold $\ge 1$ wood and $\ge 1$ brick: output `[build: road]`.
* Otherwise: output `[build: none]`.