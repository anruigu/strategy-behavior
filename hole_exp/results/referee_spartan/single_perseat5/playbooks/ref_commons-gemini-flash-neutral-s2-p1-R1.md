---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1235
---
**Playbook: Multi-Boat Fishery Commons**

- **Seasons 1 through $N-1$ (Pre-Final Seasons):**
  - If the previous season's total catch kept the stock healthy, submit the exact sustainable share specified in the prompt (`[catch: sustainable_share]`).
  - If other boats overfished in the previous season and reduced the stock below maximum capacity, do not try to punish them by emptying the pool early; submit the adjusted sustainable share for the current stock level to allow the stock to recover or sustain maximal regrowth.

- **Final Season ($N$ of $N$):**
  - There is zero future regrowth value. Never leave fish in the water in the final round.
  - Anticipate that other players will also attempt to defect or harvest heavily in the final round. If the harbour truncates/allocates catches proportionally when total requests exceed the remaining stock, do not restrict myself to a polite equal split ($S / 3$). 
  - When the final season is put to me, submit a demand for the entire remaining stock or a substantially larger share (`[catch: remaining_stock]`) to guarantee I capture my full proportional entitlement even if other boats over-claim. Restricted claims (e.g., exactly 33.3) result in lost yield if others claim more.