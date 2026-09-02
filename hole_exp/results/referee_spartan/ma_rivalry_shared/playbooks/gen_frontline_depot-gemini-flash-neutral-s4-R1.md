---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1537
---
# Playbook: Frontline Depot

- **Understanding Budget Rules**:
  - The garrison limit (e.g., 10 units) applies independently to each parameter (`allocate_strike` and `allocate_guard`), but do not artificially handicap guard by treating it as `10 - strike`. 
  - Submitting `10` for strike and `10` for guard is fully legal when the maximum allowance per parameter is 10.

- **Round Progression Strategy**:
  - **Round 1**:
    - When prompted for `allocate_strike`, play `6` to immediately pressure standard `5` guards.
    - When prompted for `allocate_guard`, play `6` to ensure surplus guard against standard `5` strikes.
  - **Round 2**:
    - When prompted for `allocate_strike`, play `7` to beat escalating `6` guards.
    - When prompted for `allocate_guard`, play `6` or `7` based on opponent's Round 1 strike pattern.
  - **Round 3**:
    - When prompted for `allocate_strike`, play `7` or `8`.
    - When prompted for `allocate_guard`, play `7` or `8`.
  - **Round 4 (Final Round)**:
    - When prompted for `allocate_strike`, allocate the maximum allowed value (`10`).
    - When prompted for `allocate_guard`, allocate the maximum allowed value (`10`). Do not reduce guard to a low value (e.g., `2`) under the mistaken assumption of a shared budget.

- **What Did Not Work**:
  - Playing passive/balanced `5/5` in early rounds yields 0 net points against identical play.
  - Under-allocating guard in later rounds (e.g., allocating guard 2 after strike 8) unnecessarily surrenders net damage and bonus points to the opponent.