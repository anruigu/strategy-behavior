---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 943
---
### Playbook

- In all seasons prior to the final season:
  - When the prompt provides a sustainable share per boat and other boats have been cooperating, submit exactly that sustainable share: `[catch: S]`.
  - If other boats have previously overfished, recalculate my share to not exceed the sustainable yield for the remaining stock, or match the sustainable rate given in the prompt to prevent stock collapse.

- In the final season:
  - There is no future regrowth, so do not leave fish behind.
  - Anticipate that other boats may attempt to take more than their equal 1/3 share of the remaining stock.
  - To protect against being undercut while maximizing final yield, submit a bid for the entire remaining stock or a substantial portion of it (up to `[catch: Stock]`) rather than assuming an orderly equal split of `Stock / N_boats`.

- Keep reasoning strictly to 1–2 concise sentences and always terminate the reply with `[catch: N]`.