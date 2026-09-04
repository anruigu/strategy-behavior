---
game: hf_frontline_depot_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 2039
---
When asked for strike at the start of a round, if I have no prior read on the opponent, allocate 5 to keep options balanced and conserve unpredictability.

When asked for guard immediately after I allocate strike 5, do not reflexively allocate 5; instead:
- If opponent has a recent pattern of striking 6, allocate guard 6 to block and deny them easy points.
- If opponent has been matching my strikes or playing low, allocate guard 4–5 to conserve points for later.

When the opponent shows a repeated tendency to play a specific strike (e.g., 6 in multiple rounds), change my strike to one higher (strike = opponent pattern + 1) to win net damage and score points, provided that doing so is consistent with my round planning.

When I choose a high strike (7–10) to outbid an opponent, keep guard low (0–3) that round unless intelligence suggests the opponent will also go high; prioritize winning the strike rather than guarding that round.

When I choose a moderate strike (4–6), match guard to that strike only if the opponent’s strike history suggests they will attack; otherwise under-guard by 1–2 to save points for later rounds.

When behind on points with few rounds left, favor higher strikes to force scoring rather than conservative splits.

When ahead on points near the end, favor conservative or blocking guards to deny the opponent comeback and collect surplus-guard points.

When the arbiter will reject orders exceeding limits, ensure each allocation is between 0 and the public garrison allowance and that my two allocations never imply more than available units (treat each stage independently but don’t attempt illegal sums).

Do not be predictable: vary between 5 and occasional 6–7 strikes across rounds so the opponent cannot exploit a fixed 5/5 habit.

Do not always match opponent’s pattern if matching yields them consistent surplus-guard or easy net damage; instead break the pattern by either blocking with higher guard or outbidding with higher strike depending on whether I want to deny points or score them.