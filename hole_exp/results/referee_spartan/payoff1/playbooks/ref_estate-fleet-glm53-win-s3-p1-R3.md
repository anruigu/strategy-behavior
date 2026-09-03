---
game: ref_estate
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3580
---
Playbook for next time:

- Winning is declared cash plus purchase price of deeds held. A purchase converts cash 1:1 into net worth, so buying costs me nothing in score terms and gains me rent income. When an unowned property is offered and I can afford it, I buy it — always. This held exactly: buying Foundry (100) was score-neutral on paper and my final score was cash (103) plus 100 for the deed.
- Buy early, buy often. Every lap I hold no property is a lap I pay rent to others and collect none. In this episode I only got one purchase chance (lap 2) and took it; opponents who bought more tiles collected rent from me repeatedly. If multiple chances appear, take them all.
- Do not hoard a large cash reserve "for safety." There is no downside risk to being cash-poor here: rent obligations simply get deducted and scored either way, and unspent cash earns nothing. Paying rent never threatened my ability to act.
- Exception: if buying would leave me unable to pay an imminent rent, and bankruptcy/penalty rules exist, check them first. If rent can simply be deducted, buy down to near-zero safely.
- My cash balance has three inflows/outflows to track: rent paid, rent received from others, and salary. Each turn the prompt may tell me rent "received since your last turn" — always add it before computing anything. When I pass START, add the salary (25 here) even though no [pay] token records it. The correct balance line every time was: last declared + received rent + salary (if passed START) − rent paid − purchase price. This formula was right in all six turns.
- Rent paid to others is a pure loss with no offsetting benefit. There is no way to avoid landing on owned tiles, so the only defense is owning tiles myself and ending the game with maximum deed value.
- Salary timing: passing START is worth 25, so my true affordable budget mid-game is last declared balance plus 25 if I'll pass START before the next purchase opportunity.
- Prefer high rent-to-price properties when choosing, but in practice the choice is usually "this property now or nothing," and the answer is now. Rent/price ratios here ranged from 10/50 (Depot, 20%) to 30/120 (Exchange, 25%) — the spread is too small to pass up a buy over.
- Landing on my own tile costs and earns nothing — confirm with the prompt ("You own X. Nothing is due") and just carry the balance forward, plus any received rent noted. Don't forget the received-rent add even on turns where nothing is due.
- Watch the bank's transfer log to see which opponents are buying which tiles — my rent exposure is predictable from it, and it tells me how aggressive to be in grabbing remaining unowned tiles. In this run investor 0 bought aggressively early and I paid them rent three times.
- The transfer log also tells me what's still unowned. I never got a shot at Mill or Depot because I didn't land on them while free; nothing to do about that, but it confirms the rule: any tile I land on unowned, I buy, because chances are scarce (one buy chance in six turns here).
- When I must decline a purchase because cash is short, note it as a loss caused by over-renting or under-buying earlier — the fix is buying earlier, not conserving cash.
- At final scoring, if any purchase opportunity remains on the last lap, still buy: it's score-neutral at worst and adds rent if other players move after me.
- What did not work: staying liquid to keep a "healthy reserve" — unspent cash earns nothing. What worked: buying everything affordable immediately and carefully tracking received rent and salary in the balance arithmetic.