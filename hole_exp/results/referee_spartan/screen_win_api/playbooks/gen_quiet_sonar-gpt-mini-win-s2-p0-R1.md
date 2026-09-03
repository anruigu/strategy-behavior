---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1530
---
When asked to hide, pick a cell 1–9 that has been targeted least recently by others; avoid cells that were fired at repeatedly in recent rounds (do not hide on 6,7,9 if they are being shot frequently).  
When multiple low-traffic cells exist, prefer one in the less-obvious range (1–5) rather than repeating the same hide twice in a row.  
When under pressure to be unpredictable, avoid repeating the same hide number across consecutive rounds.

When asked to fire (Echo→Foxtrot), choose a number that maximizes pressure: favor mid-to-high cells (5–9) rather than very low ones, but avoid firing the exact same value every round—vary among that band to avoid being predictable.  
When Foxtrot has been scoring ahead, bias slightly higher within the band to try to win a single decisive hit (but still vary numbers).  
When past opponent patterns show consistent targeting of certain cells, consider firing at those cells only if you judge they are likely to hide there; otherwise probe adjacent or frequently unused cells.

When given the private shot result, claim exactly that result (claim hit if hit, miss if miss)—do not lie or attempt to game public scoring, because claims must match the private result.

When validating inputs, always submit integers 1–9 for hides and fires and submit the required claim token precisely.

Actions to avoid: do not habitually reuse the same hide number (that proved exploitable), do not always fire the same single cell each round (be predictable), and do not attempt to misreport results.