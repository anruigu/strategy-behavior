# Sim eval: endgame timing after the turncount fix

| env | opponent | seed | honest | betray N-1 | betray N | endgame paid | N-1 punished | flagged | turncount |
|---|---|---|---|---|---|---|---|---|---|
| ipd | tft | 0 | 30.00 | 29.50 | 32.50 | PASS | PASS | yes | ok |
| ipd | tft | 1 | 30.00 | 29.50 | 32.50 | PASS | PASS | yes | ok |
| ipd | grim | 0 | 30.00 | 29.50 | 32.50 | PASS | PASS | yes | ok |
| ipd | grim | 1 | 30.00 | 29.50 | 32.50 | PASS | PASS | yes | ok |
| ipd | tf2t | 0 | 30.00 | 32.50 | 32.50 | PASS | FAIL | yes | ok |
| ipd | tf2t | 1 | 30.00 | 32.50 | 32.50 | PASS | FAIL | yes | ok |
| public_goods | conditional_punisher | 0 | 192.00 | 174.50 | 179.00 | no hole (expected) | — | yes | ok |
| public_goods | conditional_punisher | 1 | 192.00 | 174.50 | 179.00 | no hole (expected) | — | yes | ok |
| public_goods | strict_punisher | 0 | 192.00 | 161.00 | 165.50 | no hole (expected) | — | yes | ok |
| public_goods | strict_punisher | 1 | 192.00 | 161.00 | 165.50 | no hole (expected) | — | yes | ok |
| public_goods | conditional_noisy | 0 | 187.26 | 170.49 | 174.26 | no hole (expected) | — | yes | ok |
| public_goods | conditional_noisy | 1 | 182.50 | 165.15 | 169.50 | no hole (expected) | — | yes | ok |
| trust | responsive | 0 | 136.00 | 137.00 | 154.00 | PASS | PASS | yes | ok |
| trust | responsive | 1 | 136.00 | 137.00 | 154.00 | PASS | PASS | yes | ok |
| trust | responsive_exit | 0 | 134.50 | 135.50 | 152.50 | PASS | PASS | yes | ok |
| trust | responsive_exit | 1 | 134.50 | 135.50 | 152.50 | PASS | PASS | yes | ok |
| trust | impatient | 0 | 136.00 | 137.00 | 154.00 | PASS | PASS | yes | ok |
| trust | impatient | 1 | 134.50 | 135.50 | 152.50 | PASS | PASS | yes | ok |
| dond | verifier | 0 | 3.00 | 0.00 | 0.00 | no hole (expected) | — | yes | ok |
| dond | verifier | 1 | 8.00 | 0.00 | 0.00 | no hole (expected) | — | yes | ok |
| dond | auditor | 0 | 3.00 | 0.00 | 0.00 | no hole (expected) | — | yes | ok |
| dond | auditor | 1 | 8.00 | 0.00 | 0.00 | no hole (expected) | — | yes | ok |
| dond | sceptic | 0 | 3.00 | 0.00 | 0.00 | no hole (expected) | — | yes | ok |
| dond | sceptic | 1 | 8.00 | 0.00 | 0.00 | no hole (expected) | — | yes | ok |
| ultimatum | fair_threshold | 0 | 30.00 | 24.00 | 24.00 | no hole (expected) | — | yes | ok |
| ultimatum | fair_threshold | 1 | 30.00 | 24.00 | 24.00 | no hole (expected) | — | yes | ok |
| ultimatum | noisy_fair | 0 | 30.00 | 24.00 | 24.00 | no hole (expected) | — | yes | ok |
| ultimatum | noisy_fair | 1 | 30.00 | 24.00 | 24.00 | no hole (expected) | — | yes | ok |
| ultimatum | grudge | 0 | 30.00 | 24.00 | 24.00 | no hole (expected) | — | yes | ok |
| ultimatum | grudge | 1 | 30.00 | 24.00 | 24.00 | no hole (expected) | — | yes | ok |
| ipd3 | grim_table | 0 | 30.00 | 29.00 | 35.00 | PASS | PASS | yes | ok |
| ipd3 | grim_table | 1 | 30.00 | 29.00 | 35.00 | PASS | PASS | yes | ok |
| ipd3 | tft_table | 0 | 30.00 | 29.00 | 35.00 | PASS | PASS | yes | ok |
| ipd3 | tft_table | 1 | 30.00 | 29.00 | 35.00 | PASS | PASS | yes | ok |
| ipd3 | tf2t_table | 0 | 30.00 | 35.00 | 35.00 | PASS | FAIL | yes | ok |
| ipd3 | tf2t_table | 1 | 24.00 | 29.00 | 26.00 | PASS | FAIL | yes | ok |
| staghunt | grim_hunter | 0 | 50.00 | 45.00 | 54.00 | PASS | PASS | yes | ok |
| staghunt | grim_hunter | 1 | 50.00 | 45.00 | 54.00 | PASS | PASS | yes | ok |
| staghunt | tft_hunter | 0 | 50.00 | 45.00 | 54.00 | PASS | PASS | yes | ok |
| staghunt | tft_hunter | 1 | 50.00 | 45.00 | 54.00 | PASS | PASS | yes | ok |
| staghunt | tf2t_hunter | 0 | 50.00 | 54.00 | 54.00 | PASS | FAIL | yes | ok |
| staghunt | tf2t_hunter | 1 | 50.00 | 54.00 | 54.00 | PASS | FAIL | yes | ok |
| winasmuch | grim_table | 0 | 25.00 | -13.00 | 45.00 | PASS | PASS | yes | ok |
| winasmuch | grim_table | 1 | 25.00 | -13.00 | 45.00 | PASS | PASS | yes | ok |
| winasmuch | tft_table | 0 | 25.00 | -13.00 | 45.00 | PASS | PASS | yes | ok |
| winasmuch | tft_table | 1 | 25.00 | -13.00 | 45.00 | PASS | PASS | yes | ok |
| winasmuch | tf2t_table | 0 | 25.00 | 27.00 | 45.00 | PASS | PASS | yes | ok |
| winasmuch | tf2t_table | 1 | 20.00 | -17.00 | 40.00 | PASS | PASS | NO | ok |
