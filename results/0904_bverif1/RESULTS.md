# bverif1 -- do REGIME and GROUP variants change behaviour?

30,816 rows, 43 arms, 6 models, rounds 0-3.

Rates are pooled `sum(v_headline)/sum(o_headline)`. Every delta is a variant arm minus the `@shipped` baseline of its own cell, at the same model and round. `floor` is the baseline arm's own split-half spread at that model and round -- the measured null.


## Round 0  (no playbook yet: the knob acting on the shipped prompt)

**REGIME**: 72 (arm, model) cells. mean |delta| 0.086 against a mean noise floor of 0.061; 35/72 clear their own floor.

**GROUP**: 48 (arm, model) cells. mean |delta| 0.079 against a mean noise floor of 0.063; 22/48 clear their own floor.


| arm | axis | model | base | variant | delta | floor | over? | dT(N-1) |
|---|---|---|---:|---:|---:|---:|:-:|---:|
| `ref_commons@regen-30` | GROUP | gemini-flash | 0.856 | 0.216 | -0.641 | 0.157 | yes | -0.75 |
| `ref_invoice@retainer-40` | REGIME | gemini-flash | 0.977 | 0.426 | -0.551 | 0.046 | yes | +0.00 |
| `ref_invoice@retainer-40-tight` | REGIME | gemini-flash | 0.977 | 0.500 | -0.477 | 0.046 | yes | +0.00 |
| `ta_letterauction@contest` | REGIME | fleet-glm53 | 0.500 | 0.125 | -0.375 | 0.238 | yes | -10.80 |
| `gen_seven_seal@budget-13` | REGIME | gemini-flash | 0.456 | 0.099 | -0.357 | 0.040 | yes | -49.00 |
| `ta_pubgoods@mf-4` | GROUP | gemini-flash | 0.417 | 0.117 | -0.300 | 0.233 | yes | +0.00 |
| `gen_seven_seal@budget-20` | REGIME | gemini-flash | 0.456 | 0.163 | -0.294 | 0.040 | yes | -55.85 |
| `gen_seven_seal@budget-13` | REGIME | fleet-kimi3 | 0.440 | 0.155 | -0.286 | 0.040 | yes | -49.00 |
| `ref_commons@regen-11` | GROUP | fleet-glm53 | 0.477 | 0.708 | +0.231 | 0.102 | yes | +7.17 |
| `gen_seven_seal@budget-20` | REGIME | fleet-kimi3 | 0.440 | 0.214 | -0.226 | 0.040 | yes | -55.85 |
| `ref_commons@regen-30` | GROUP | fleet-kimi3 | 0.507 | 0.282 | -0.225 | 0.033 | yes | -0.75 |
| `gen_seven_seal@budget-13` | REGIME | fleet-qwen38 | 0.329 | 0.107 | -0.222 | 0.024 | yes | -49.00 |
| `gen_sovereign_vaults@crowding-3` | GROUP | fleet-glm53 | 0.208 | 0.417 | +0.208 | 0.117 | yes | -82.37 |
| `ta_letterauction@contest` | REGIME | fleet-qwen38 | 0.000 | 0.200 | +0.200 | 0.000 | yes | -10.80 |
| `gen_harbor_customs@rebate-1` | REGIME | fleet-glm53 | 0.420 | 0.601 | +0.181 | 0.062 | yes | -16.42 |
| `gen_sovereign_vaults@crowding-18` | REGIME | fleet-kimi3 | 0.458 | 0.633 | +0.175 | 0.017 | yes | -49.42 |
| `ref_invoice@retainer-40-tight` | REGIME | fleet-qwen38 | 0.551 | 0.380 | -0.171 | 0.009 | yes | +0.00 |
| `ta_pubgoods@mf-4` | GROUP | fleet-qwen38 | 0.017 | 0.183 | +0.167 | 0.033 | yes | +0.00 |
| `ref_invoice@retainer-40` | REGIME | fleet-qwen38 | 0.551 | 0.389 | -0.162 | 0.009 | yes | +0.00 |
| `ref_commons@regen-30` | GROUP | gpt-mini | 0.921 | 0.759 | -0.162 | 0.080 | yes | -0.75 |
| `ref_invoice@retainer-40` | REGIME | fleet-kimi3 | 0.583 | 0.426 | -0.157 | 0.148 | yes | +0.00 |
| `ref_commons@stock-300` | GROUP | gemini-flash | 0.856 | 0.702 | -0.154 | 0.157 | no | +35.56 |
| `ref_commons@regen-11` | GROUP | haiku | 0.426 | 0.273 | -0.153 | 0.074 | yes | +7.17 |
| `ref_invoice@retainer-40-tight` | REGIME | fleet-kimi3 | 0.583 | 0.431 | -0.153 | 0.148 | yes | +0.00 |
| `ref_commons@regen-11` | GROUP | gemini-flash | 0.856 | 0.990 | +0.133 | 0.157 | no | +7.17 |
| `ref_commons@regen-11` | GROUP | fleet-kimi3 | 0.507 | 0.625 | +0.118 | 0.033 | yes | +7.17 |
| `ref_commons@stock-300` | GROUP | fleet-glm53 | 0.477 | 0.594 | +0.117 | 0.102 | yes | +35.56 |
| `gen_frontline_depot@supply-4` | GROUP | fleet-qwen38 | 0.312 | 0.427 | +0.115 | 0.042 | yes | -13.24 |
| `ref_commons@regen-30` | GROUP | fleet-qwen38 | 0.310 | 0.204 | -0.106 | 0.083 | yes | -0.75 |
| `gen_icebound@steal-5-hard-fail` | REGIME | gemini-flash | 0.656 | 0.761 | +0.106 | 0.200 | no | -25.00 |
| `gen_frontline_depot@supply-1` | REGIME | gemini-flash | 0.698 | 0.594 | -0.104 | 0.021 | yes | -8.73 |
| `ta_letterauction@contest` | REGIME | gpt-mini | 0.333 | 0.231 | -0.103 | 0.667 | no | -10.80 |
| `gen_seven_seal@budget-13` | REGIME | fleet-glm53 | 0.190 | 0.095 | -0.095 | 0.048 | yes | -49.00 |
| `gen_sovereign_vaults@crowding-18` | REGIME | fleet-glm53 | 0.208 | 0.300 | +0.092 | 0.117 | no | -49.42 |
| `ref_invoice@retainer-40-tight` | REGIME | gpt-mini | 0.829 | 0.741 | -0.088 | 0.120 | no | +0.00 |
| `gen_quiet_sonar@loss-5` | GROUP | gemini-flash | 0.235 | 0.320 | +0.085 | 0.002 | yes | +0.00 |
| `ref_commons@stock-300` | GROUP | fleet-kimi3 | 0.507 | 0.423 | -0.084 | 0.033 | yes | +35.56 |
| `ref_commons@regen-11` | GROUP | fleet-qwen38 | 0.310 | 0.394 | +0.083 | 0.083 | yes | +7.17 |
| `ta_letterauction@contest` | REGIME | fleet-kimi3 | 0.083 | 0.000 | -0.083 | 0.167 | no | -10.80 |
| `gen_quiet_sonar@loss-5` | GROUP | gpt-mini | 0.215 | 0.292 | +0.077 | 0.009 | yes | +0.00 |
| `gen_seven_seal@budget-20` | REGIME | fleet-qwen38 | 0.329 | 0.254 | -0.075 | 0.024 | yes | -55.85 |
| `gen_frontline_depot@supply-1` | REGIME | gpt-mini | 0.698 | 0.625 | -0.073 | 0.062 | yes | -8.73 |
| `ref_invoice@retainer-40` | REGIME | haiku | 0.269 | 0.199 | -0.069 | 0.056 | yes | +0.00 |
| `gen_quiet_sonar@congested` | REGIME | gpt-mini | 0.215 | 0.280 | +0.065 | 0.009 | yes | -16.50 |
| `ref_estate@bank-reserve-2` | REGIME | haiku | 0.227 | 0.162 | -0.065 | 0.102 | no | -284.76 |
| `gen_frontline_depot@supply-1` | REGIME | fleet-glm53 | 0.740 | 0.677 | -0.062 | 0.104 | no | -8.73 |
| `gen_frontline_depot@supply-1` | REGIME | haiku | 0.656 | 0.594 | -0.062 | 0.062 | no | -8.73 |
| `gen_frontline_depot@supply-4` | GROUP | gpt-mini | 0.698 | 0.635 | -0.062 | 0.062 | no | -13.24 |
| `gen_frontline_depot@supply-1` | REGIME | fleet-qwen38 | 0.312 | 0.365 | +0.052 | 0.042 | yes | -8.73 |
| `gen_harbor_customs@rebate-1` | REGIME | fleet-qwen38 | 0.330 | 0.382 | +0.052 | 0.062 | no | -16.42 |
| `gen_frontline_depot@supply-4` | GROUP | gemini-flash | 0.698 | 0.646 | -0.052 | 0.021 | yes | -13.24 |
| `gen_seven_seal@budget-20` | REGIME | fleet-glm53 | 0.190 | 0.139 | -0.052 | 0.048 | yes | -55.85 |
| `gen_sovereign_vaults@crowding-18` | REGIME | gemini-flash | 0.050 | 0.000 | -0.050 | 0.100 | no | -49.42 |
| `gen_sovereign_vaults@crowding-3` | GROUP | gemini-flash | 0.050 | 0.000 | -0.050 | 0.100 | no | -82.37 |
| `ref_exchange@build-slots-4` | REGIME | gpt-mini | 0.094 | 0.044 | -0.050 | 0.033 | yes | -7.90 |
| `gen_icebound@steal-5-hard-fail` | REGIME | fleet-glm53 | 0.422 | 0.472 | +0.050 | 0.089 | no | -25.00 |
| `gen_icebound@steal-5-hard-fail` | REGIME | gpt-mini | 0.789 | 0.739 | -0.050 | 0.044 | yes | -25.00 |
| `gen_harbor_customs@rebate-1` | REGIME | gemini-flash | 0.573 | 0.524 | -0.049 | 0.076 | no | -16.42 |
| `gen_quiet_sonar@loss-5` | GROUP | fleet-glm53 | 0.099 | 0.144 | +0.045 | 0.002 | yes | +0.00 |
| `ref_exchange@build-slots-4` | REGIME | fleet-glm53 | 0.028 | 0.072 | +0.044 | 0.011 | yes | -7.90 |
| `gen_icebound@steal-5-hard-fail` | REGIME | fleet-kimi3 | 0.656 | 0.700 | +0.044 | 0.111 | no | -25.00 |
| `gen_sovereign_vaults@crowding-3` | GROUP | fleet-kimi3 | 0.458 | 0.500 | +0.042 | 0.017 | yes | -82.37 |
| `gen_sovereign_vaults@crowding-18` | REGIME | gpt-mini | 0.025 | 0.067 | +0.042 | 0.050 | no | -49.42 |
| `gen_frontline_depot@supply-4` | GROUP | fleet-kimi3 | 0.885 | 0.844 | -0.042 | 0.062 | no | -13.24 |
| `ref_invoice@retainer-40` | REGIME | gpt-mini | 0.829 | 0.787 | -0.042 | 0.120 | no | +0.00 |
| `gen_seven_seal@budget-13` | REGIME | gpt-mini | 0.048 | 0.008 | -0.040 | 0.032 | yes | -49.00 |
| `gen_icebound@steal-5-hard-fail` | REGIME | haiku | 0.594 | 0.633 | +0.039 | 0.144 | no | -25.00 |
| `ref_estate@bank-reserve-2` | REGIME | fleet-glm53 | 0.009 | 0.046 | +0.037 | 0.019 | yes | -284.76 |
| `ta_letterauction@contest` | REGIME | haiku | 0.632 | 0.667 | +0.035 | 0.011 | yes | -10.80 |
| `ta_pubgoods@mf-4` | GROUP | haiku | 0.183 | 0.217 | +0.033 | 0.100 | no | +0.00 |
| `ref_exchange@build-slots-4` | REGIME | fleet-qwen38 | 0.089 | 0.056 | -0.033 | 0.022 | yes | -7.90 |
| `ta_pubgoods@mf-4` | GROUP | fleet-kimi3 | 0.067 | 0.100 | +0.033 | 0.133 | no | +0.00 |
| `ta_pubgoods@mf-4` | GROUP | fleet-glm53 | 0.067 | 0.033 | -0.033 | 0.067 | no | +0.00 |
| `ref_commons@regen-30` | GROUP | fleet-glm53 | 0.477 | 0.444 | -0.032 | 0.102 | no | -0.75 |
| `ref_invoice@retainer-40` | REGIME | fleet-glm53 | 0.190 | 0.157 | -0.032 | 0.009 | yes | +0.00 |
| `ref_commons@regen-30` | GROUP | haiku | 0.426 | 0.394 | -0.032 | 0.074 | no | -0.75 |
| `gen_frontline_depot@supply-1` | REGIME | fleet-kimi3 | 0.885 | 0.854 | -0.031 | 0.062 | no | -8.73 |
| `ref_commons@regen-11` | GROUP | gpt-mini | 0.921 | 0.950 | +0.029 | 0.080 | no | +7.17 |
| `ref_invoice@retainer-40-tight` | REGIME | haiku | 0.269 | 0.241 | -0.028 | 0.056 | no | +0.00 |
| `gen_icebound@steal-5-hard-fail` | REGIME | fleet-qwen38 | 0.633 | 0.606 | -0.028 | 0.067 | no | -25.00 |
| `gen_quiet_sonar@loss-5` | GROUP | fleet-qwen38 | 0.274 | 0.248 | -0.026 | 0.023 | yes | +0.00 |
| `gen_sovereign_vaults@crowding-3` | GROUP | fleet-qwen38 | 0.183 | 0.158 | -0.025 | 0.033 | no | -82.37 |
| `ref_estate@bank-reserve-2` | REGIME | fleet-kimi3 | 0.009 | 0.032 | +0.023 | 0.000 | yes | -284.76 |
| `gen_quiet_sonar@congested` | REGIME | gemini-flash | 0.235 | 0.256 | +0.021 | 0.002 | yes | -16.50 |
| `gen_harbor_customs@rebate-1` | REGIME | haiku | 0.503 | 0.524 | +0.021 | 0.062 | no | -16.42 |
| `ta_liarsdice@rake-1` | GROUP | fleet-glm53 | 0.021 | 0.000 | -0.021 | 0.014 | yes | -2.97 |
| `ref_commons@stock-300` | GROUP | gpt-mini | 0.921 | 0.903 | -0.018 | 0.080 | no | +35.56 |
| `gen_quiet_sonar@loss-5` | GROUP | fleet-kimi3 | 0.390 | 0.373 | -0.018 | 0.019 | no | +0.00 |
| `gen_harbor_customs@rebate-1` | REGIME | gpt-mini | 0.347 | 0.330 | -0.017 | 0.125 | no | -16.42 |
| `ref_commons@stock-300` | GROUP | haiku | 0.426 | 0.443 | +0.017 | 0.074 | no | +35.56 |
| `ref_exchange@build-slots-4` | REGIME | fleet-kimi3 | 0.050 | 0.033 | -0.017 | 0.033 | no | -7.90 |
| `gen_sovereign_vaults@crowding-18` | REGIME | fleet-qwen38 | 0.183 | 0.167 | -0.017 | 0.033 | no | -49.42 |
| `gen_sovereign_vaults@crowding-18` | REGIME | haiku | 0.058 | 0.075 | +0.017 | 0.017 | no | -49.42 |
| `gen_seven_seal@budget-13` | REGIME | haiku | 0.000 | 0.012 | +0.012 | 0.000 | yes | -49.00 |
| `gen_quiet_sonar@congested` | REGIME | fleet-glm53 | 0.099 | 0.111 | +0.012 | 0.002 | yes | -16.50 |
| `gen_quiet_sonar@congested` | REGIME | fleet-kimi3 | 0.390 | 0.401 | +0.011 | 0.019 | no | -16.50 |
| `gen_frontline_depot@supply-4` | GROUP | fleet-glm53 | 0.740 | 0.750 | +0.010 | 0.104 | no | -13.24 |
| `gen_frontline_depot@supply-4` | GROUP | haiku | 0.656 | 0.646 | -0.010 | 0.062 | no | -13.24 |
| `ref_estate@bank-reserve-2` | REGIME | gpt-mini | 0.287 | 0.296 | +0.009 | 0.019 | no | -284.76 |
| `gen_quiet_sonar@congested` | REGIME | haiku | 0.017 | 0.026 | +0.009 | 0.017 | no | -16.50 |
| `gen_sovereign_vaults@crowding-3` | GROUP | haiku | 0.058 | 0.067 | +0.008 | 0.017 | no | -82.37 |
| `ta_liarsdice@rake-1` | GROUP | gemini-flash | 0.007 | 0.000 | -0.007 | 0.014 | no | -2.97 |
| `ta_liarsdice@rake-1` | GROUP | haiku | 0.000 | 0.007 | +0.007 | 0.000 | yes | -2.97 |
| `gen_seven_seal@budget-20` | REGIME | gpt-mini | 0.048 | 0.052 | +0.004 | 0.032 | no | -55.85 |
| `gen_quiet_sonar@congested` | REGIME | fleet-qwen38 | 0.274 | 0.270 | -0.004 | 0.023 | no | -16.50 |
| `gen_quiet_sonar@loss-5` | GROUP | haiku | 0.017 | 0.017 | +0.000 | 0.017 | no | +0.00 |
| `gen_harbor_customs@rebate-1` | REGIME | fleet-kimi3 | 0.229 | 0.229 | +0.000 | 0.028 | no | -16.42 |
| `gen_seven_seal@budget-20` | REGIME | haiku | 0.000 | 0.000 | +0.000 | 0.000 | no | -55.85 |
| `gen_sovereign_vaults@crowding-3` | GROUP | gpt-mini | 0.025 | 0.025 | +0.000 | 0.050 | no | -82.37 |
| `ref_commons@stock-300` | GROUP | fleet-qwen38 | 0.310 | 0.310 | +0.000 | 0.083 | no | +35.56 |
| `ref_estate@bank-reserve-2` | REGIME | fleet-qwen38 | 0.167 | 0.167 | +0.000 | 0.056 | no | -284.76 |
| `ref_estate@bank-reserve-2` | REGIME | gemini-flash | 0.009 | 0.009 | +0.000 | 0.019 | no | -284.76 |
| `ref_exchange@build-slots-4` | REGIME | gemini-flash | 0.006 | 0.006 | +0.000 | 0.011 | no | -7.90 |
| `ref_exchange@build-slots-4` | REGIME | haiku | 0.178 | 0.178 | +0.000 | 0.022 | no | -7.90 |
| `ref_invoice@retainer-40-tight` | REGIME | fleet-glm53 | 0.190 | 0.190 | +0.000 | 0.009 | no | +0.00 |
| `ta_letterauction@contest` | REGIME | gemini-flash | 0.000 | 0.000 | +0.000 | 0.000 | no | -10.80 |
| `ta_liarsdice@rake-1` | GROUP | fleet-kimi3 | 0.000 | 0.000 | +0.000 | 0.000 | no | -2.97 |
| `ta_liarsdice@rake-1` | GROUP | fleet-qwen38 | 0.000 | 0.000 | +0.000 | 0.000 | no | -2.97 |
| `ta_liarsdice@rake-1` | GROUP | gpt-mini | 0.000 | 0.000 | +0.000 | 0.000 | no | -2.97 |
| `ta_pubgoods@mf-4` | GROUP | gpt-mini | 0.033 | 0.033 | +0.000 | 0.067 | no | +0.00 |

## Round 3  (after the reflection ladder)

**REGIME**: 72 (arm, model) cells. mean |delta| 0.200 against a mean noise floor of 0.052; 38/72 clear their own floor.

**GROUP**: 48 (arm, model) cells. mean |delta| 0.188 against a mean noise floor of 0.097; 28/48 clear their own floor.


| arm | axis | model | base | variant | delta | floor | over? | dT(N-1) |
|---|---|---|---:|---:|---:|---:|:-:|---:|
| `gen_frontline_depot@supply-4` | GROUP | gemini-flash | 0.958 | 0.062 | -0.896 | 0.083 | yes | -13.24 |
| `ref_invoice@retainer-40-tight` | REGIME | fleet-qwen38 | 0.949 | 0.134 | -0.815 | 0.102 | yes | +0.00 |
| `ref_invoice@retainer-40-tight` | REGIME | fleet-kimi3 | 0.898 | 0.139 | -0.759 | 0.167 | yes | +0.00 |
| `gen_seven_seal@budget-13` | REGIME | gemini-flash | 1.000 | 0.246 | -0.754 | 0.000 | yes | -49.00 |
| `ref_commons@regen-30` | GROUP | gemini-flash | 0.905 | 0.167 | -0.738 | 0.177 | yes | -0.75 |
| `ref_invoice@retainer-40` | REGIME | fleet-qwen38 | 0.949 | 0.278 | -0.671 | 0.102 | yes | +0.00 |
| `ref_commons@stock-300` | GROUP | gemini-flash | 0.905 | 0.246 | -0.659 | 0.177 | yes | +35.56 |
| `gen_seven_seal@budget-20` | REGIME | gemini-flash | 1.000 | 0.349 | -0.651 | 0.000 | yes | -55.85 |
| `gen_frontline_depot@supply-1` | REGIME | fleet-qwen38 | 1.000 | 0.375 | -0.625 | 0.000 | yes | -8.73 |
| `ref_invoice@retainer-40` | REGIME | fleet-kimi3 | 0.898 | 0.273 | -0.625 | 0.167 | yes | +0.00 |
| `gen_seven_seal@budget-13` | REGIME | fleet-glm53 | 0.988 | 0.425 | -0.563 | 0.024 | yes | -49.00 |
| `gen_seven_seal@budget-13` | REGIME | fleet-qwen38 | 0.956 | 0.397 | -0.560 | 0.071 | yes | -49.00 |
| `gen_icebound@steal-5-hard-fail` | REGIME | gemini-flash | 0.639 | 0.100 | -0.539 | 0.100 | yes | -25.00 |
| `gen_sovereign_vaults@crowding-3` | GROUP | fleet-glm53 | 0.233 | 0.750 | +0.517 | 0.067 | yes | -82.37 |
| `gen_seven_seal@budget-13` | REGIME | fleet-kimi3 | 0.996 | 0.484 | -0.512 | 0.008 | yes | -49.00 |
| `ref_invoice@retainer-40-tight` | REGIME | fleet-glm53 | 0.481 | 0.000 | -0.481 | 0.093 | yes | +0.00 |
| `gen_frontline_depot@supply-4` | GROUP | fleet-qwen38 | 1.000 | 0.521 | -0.479 | 0.000 | yes | -13.24 |
| `ta_pubgoods@mf-4` | GROUP | gemini-flash | 0.917 | 0.450 | -0.467 | 0.167 | yes | +0.00 |
| `gen_seven_seal@budget-20` | REGIME | fleet-qwen38 | 0.956 | 0.504 | -0.452 | 0.071 | yes | -55.85 |
| `gen_frontline_depot@supply-4` | GROUP | fleet-kimi3 | 1.000 | 0.562 | -0.438 | 0.000 | yes | -13.24 |
| `gen_frontline_depot@supply-1` | REGIME | gemini-flash | 0.958 | 0.542 | -0.417 | 0.083 | yes | -8.73 |
| `ref_invoice@retainer-40` | REGIME | fleet-glm53 | 0.481 | 0.065 | -0.417 | 0.093 | yes | +0.00 |
| `ref_invoice@retainer-40-tight` | REGIME | gemini-flash | 1.000 | 0.588 | -0.412 | 0.000 | yes | +0.00 |
| `gen_sovereign_vaults@crowding-18` | REGIME | fleet-qwen38 | 0.642 | 0.233 | -0.408 | 0.017 | yes | -49.42 |
| `gen_seven_seal@budget-20` | REGIME | fleet-glm53 | 0.988 | 0.619 | -0.369 | 0.024 | yes | -55.85 |
| `ref_commons@regen-30` | GROUP | fleet-kimi3 | 0.582 | 0.222 | -0.360 | 0.111 | yes | -0.75 |
| `ref_commons@regen-30` | GROUP | fleet-qwen38 | 0.535 | 0.199 | -0.336 | 0.229 | yes | -0.75 |
| `ta_pubgoods@mf-4` | GROUP | fleet-qwen38 | 0.000 | 0.333 | +0.333 | 0.000 | yes | +0.00 |
| `ref_invoice@retainer-40` | REGIME | gemini-flash | 1.000 | 0.671 | -0.329 | 0.000 | yes | +0.00 |
| `gen_seven_seal@budget-20` | REGIME | fleet-kimi3 | 0.996 | 0.679 | -0.317 | 0.008 | yes | -55.85 |
| `gen_icebound@steal-5-hard-fail` | REGIME | fleet-kimi3 | 0.733 | 0.422 | -0.311 | 0.156 | yes | -25.00 |
| `ref_commons@regen-11` | GROUP | fleet-qwen38 | 0.535 | 0.843 | +0.308 | 0.229 | yes | +7.17 |
| `ref_invoice@retainer-40` | REGIME | gpt-mini | 0.898 | 0.593 | -0.306 | 0.037 | yes | +0.00 |
| `ref_commons@stock-300` | GROUP | fleet-glm53 | 0.375 | 0.661 | +0.286 | 0.139 | yes | +35.56 |
| `gen_frontline_depot@supply-1` | REGIME | fleet-kimi3 | 1.000 | 0.719 | -0.281 | 0.000 | yes | -8.73 |
| `gen_frontline_depot@supply-4` | GROUP | fleet-glm53 | 0.833 | 0.562 | -0.271 | 0.042 | yes | -13.24 |
| `ref_commons@regen-30` | GROUP | gpt-mini | 0.510 | 0.249 | -0.261 | 0.076 | yes | -0.75 |
| `ref_invoice@retainer-40-tight` | REGIME | gpt-mini | 0.898 | 0.653 | -0.245 | 0.037 | yes | +0.00 |
| `gen_frontline_depot@supply-4` | GROUP | haiku | 0.365 | 0.604 | +0.240 | 0.062 | yes | -13.24 |
| `gen_quiet_sonar@congested` | REGIME | fleet-qwen38 | 0.465 | 0.252 | -0.213 | 0.079 | yes | -16.50 |
| `ref_commons@regen-11` | GROUP | fleet-glm53 | 0.375 | 0.582 | +0.207 | 0.139 | yes | +7.17 |
| `gen_quiet_sonar@loss-5` | GROUP | gemini-flash | 0.502 | 0.300 | -0.202 | 0.167 | yes | +0.00 |
| `gen_frontline_depot@supply-1` | REGIME | fleet-glm53 | 0.833 | 0.635 | -0.198 | 0.042 | yes | -8.73 |
| `gen_harbor_customs@rebate-1` | REGIME | gpt-mini | 0.781 | 0.597 | -0.184 | 0.062 | yes | -16.42 |
| `ref_commons@regen-11` | GROUP | gpt-mini | 0.510 | 0.328 | -0.181 | 0.076 | yes | +7.17 |
| `gen_quiet_sonar@congested` | REGIME | gemini-flash | 0.502 | 0.329 | -0.173 | 0.167 | yes | -16.50 |
| `ref_commons@regen-11` | GROUP | fleet-kimi3 | 0.582 | 0.752 | +0.170 | 0.111 | yes | +7.17 |
| `ta_pubgoods@mf-4` | GROUP | fleet-glm53 | 0.250 | 0.083 | -0.167 | 0.500 | no | +0.00 |
| `gen_quiet_sonar@congested` | REGIME | fleet-kimi3 | 0.328 | 0.163 | -0.166 | 0.253 | no | -16.50 |
| `gen_sovereign_vaults@crowding-18` | REGIME | fleet-glm53 | 0.233 | 0.392 | +0.158 | 0.067 | yes | -49.42 |
| `ref_commons@regen-30` | GROUP | haiku | 0.456 | 0.304 | -0.152 | 0.094 | yes | -0.75 |
| `ta_letterauction@contest` | REGIME | haiku | 0.182 | 0.333 | +0.152 | 0.033 | yes | -10.80 |
| `gen_sovereign_vaults@crowding-3` | GROUP | fleet-qwen38 | 0.642 | 0.492 | -0.150 | 0.017 | yes | -82.37 |
| `ref_commons@regen-11` | GROUP | haiku | 0.456 | 0.324 | -0.132 | 0.094 | yes | +7.17 |
| `gen_quiet_sonar@loss-5` | GROUP | fleet-kimi3 | 0.328 | 0.198 | -0.131 | 0.253 | no | +0.00 |
| `ta_letterauction@contest` | REGIME | fleet-glm53 | 0.071 | 0.200 | +0.129 | 0.125 | yes | -10.80 |
| `gen_icebound@steal-5-hard-fail` | REGIME | fleet-glm53 | 0.428 | 0.300 | -0.128 | 0.167 | no | -25.00 |
| `ref_commons@regen-30` | GROUP | fleet-glm53 | 0.375 | 0.249 | -0.126 | 0.139 | no | -0.75 |
| `gen_sovereign_vaults@crowding-18` | REGIME | fleet-kimi3 | 0.567 | 0.683 | +0.117 | 0.033 | yes | -49.42 |
| `ref_commons@stock-300` | GROUP | haiku | 0.456 | 0.351 | -0.105 | 0.094 | yes | +35.56 |
| `gen_frontline_depot@supply-1` | REGIME | gpt-mini | 0.469 | 0.375 | -0.094 | 0.146 | no | -8.73 |
| `ref_invoice@retainer-40` | REGIME | haiku | 0.185 | 0.097 | -0.088 | 0.019 | yes | +0.00 |
| `ref_commons@regen-11` | GROUP | gemini-flash | 0.905 | 0.993 | +0.088 | 0.177 | no | +7.17 |
| `gen_quiet_sonar@loss-5` | GROUP | fleet-qwen38 | 0.465 | 0.378 | -0.087 | 0.079 | yes | +0.00 |
| `gen_quiet_sonar@congested` | REGIME | fleet-glm53 | 0.249 | 0.163 | -0.086 | 0.102 | no | -16.50 |
| `ref_invoice@retainer-40-tight` | REGIME | haiku | 0.185 | 0.102 | -0.083 | 0.019 | yes | +0.00 |
| `gen_quiet_sonar@loss-5` | GROUP | fleet-glm53 | 0.249 | 0.167 | -0.082 | 0.102 | no | +0.00 |
| `ta_pubgoods@mf-4` | GROUP | fleet-kimi3 | 0.083 | 0.150 | +0.067 | 0.167 | no | +0.00 |
| `ref_commons@stock-300` | GROUP | gpt-mini | 0.510 | 0.444 | -0.065 | 0.076 | no | +35.56 |
| `gen_icebound@steal-5-hard-fail` | REGIME | fleet-qwen38 | 0.556 | 0.494 | -0.061 | 0.111 | no | -25.00 |
| `ta_liarsdice@rake-1` | GROUP | fleet-kimi3 | 0.056 | 0.000 | -0.056 | 0.111 | no | -2.97 |
| `gen_frontline_depot@supply-1` | REGIME | haiku | 0.365 | 0.417 | +0.052 | 0.062 | no | -8.73 |
| `ta_pubgoods@mf-4` | GROUP | haiku | 0.050 | 0.000 | -0.050 | 0.100 | no | +0.00 |
| `gen_icebound@steal-5-hard-fail` | REGIME | haiku | 0.506 | 0.456 | -0.050 | 0.056 | no | -25.00 |
| `gen_seven_seal@budget-13` | REGIME | gpt-mini | 0.067 | 0.020 | -0.048 | 0.056 | no | -49.00 |
| `ref_estate@bank-reserve-2` | REGIME | gpt-mini | 0.204 | 0.250 | +0.046 | 0.000 | yes | -284.76 |
| `ref_commons@stock-300` | GROUP | fleet-kimi3 | 0.582 | 0.537 | -0.045 | 0.111 | no | +35.56 |
| `gen_frontline_depot@supply-4` | GROUP | gpt-mini | 0.469 | 0.427 | -0.042 | 0.146 | no | -13.24 |
| `gen_icebound@steal-5-hard-fail` | REGIME | gpt-mini | 0.561 | 0.522 | -0.039 | 0.122 | no | -25.00 |
| `gen_sovereign_vaults@crowding-18` | REGIME | haiku | 0.000 | 0.033 | +0.033 | 0.000 | yes | -49.42 |
| `ref_exchange@build-slots-4` | REGIME | haiku | 0.072 | 0.039 | -0.033 | 0.122 | no | -7.90 |
| `ref_exchange@build-slots-4` | REGIME | gpt-mini | 0.089 | 0.061 | -0.028 | 0.089 | no | -7.90 |
| `ref_estate@bank-reserve-2` | REGIME | fleet-glm53 | 0.032 | 0.005 | -0.028 | 0.046 | no | -284.76 |
| `ref_estate@bank-reserve-2` | REGIME | fleet-kimi3 | 0.005 | 0.032 | +0.028 | 0.009 | yes | -284.76 |
| `ref_exchange@build-slots-4` | REGIME | fleet-qwen38 | 0.028 | 0.000 | -0.028 | 0.011 | yes | -7.90 |
| `ta_liarsdice@rake-1` | GROUP | gpt-mini | 0.000 | 0.028 | +0.028 | 0.000 | yes | -2.97 |
| `gen_quiet_sonar@loss-5` | GROUP | gpt-mini | 0.004 | 0.029 | +0.025 | 0.008 | yes | +0.00 |
| `gen_sovereign_vaults@crowding-18` | REGIME | gpt-mini | 0.033 | 0.058 | +0.025 | 0.033 | no | -49.42 |
| `gen_harbor_customs@rebate-1` | REGIME | fleet-qwen38 | 0.979 | 1.000 | +0.021 | 0.042 | no | -16.42 |
| `ta_liarsdice@rake-1` | GROUP | fleet-qwen38 | 0.062 | 0.042 | -0.021 | 0.042 | no | -2.97 |
| `ref_estate@bank-reserve-2` | REGIME | haiku | 0.065 | 0.046 | -0.019 | 0.074 | no | -284.76 |
| `ref_commons@stock-300` | GROUP | fleet-qwen38 | 0.535 | 0.552 | +0.017 | 0.229 | no | +35.56 |
| `gen_seven_seal@budget-20` | REGIME | gpt-mini | 0.067 | 0.083 | +0.016 | 0.056 | no | -55.85 |
| `ta_liarsdice@rake-1` | GROUP | haiku | 0.000 | 0.014 | +0.014 | 0.000 | yes | -2.97 |
| `gen_harbor_customs@rebate-1` | REGIME | fleet-kimi3 | 0.882 | 0.892 | +0.010 | 0.056 | no | -16.42 |
| `ref_estate@bank-reserve-2` | REGIME | fleet-qwen38 | 0.074 | 0.065 | -0.009 | 0.037 | no | -284.76 |
| `gen_sovereign_vaults@crowding-3` | GROUP | gpt-mini | 0.033 | 0.025 | -0.008 | 0.033 | no | -82.37 |
| `gen_sovereign_vaults@crowding-3` | GROUP | fleet-kimi3 | 0.567 | 0.558 | -0.008 | 0.033 | no | -82.37 |
| `ta_liarsdice@rake-1` | GROUP | fleet-glm53 | 0.000 | 0.007 | +0.007 | 0.000 | yes | -2.97 |
| `ref_exchange@build-slots-4` | REGIME | fleet-glm53 | 0.028 | 0.033 | +0.006 | 0.011 | no | -7.90 |
| `ref_estate@bank-reserve-2` | REGIME | gemini-flash | 0.005 | 0.000 | -0.005 | 0.009 | no | -284.76 |
| `gen_seven_seal@budget-13` | REGIME | haiku | 0.004 | 0.000 | -0.004 | 0.008 | no | -49.00 |
| `gen_seven_seal@budget-20` | REGIME | haiku | 0.004 | 0.000 | -0.004 | 0.008 | no | -55.85 |
| `gen_quiet_sonar@congested` | REGIME | haiku | 0.004 | 0.000 | -0.004 | 0.008 | no | -16.50 |
| `gen_quiet_sonar@congested` | REGIME | gpt-mini | 0.004 | 0.000 | -0.004 | 0.008 | no | -16.50 |
| `gen_harbor_customs@rebate-1` | REGIME | haiku | 0.035 | 0.038 | +0.003 | 0.028 | no | -16.42 |
| `gen_quiet_sonar@loss-5` | GROUP | haiku | 0.004 | 0.004 | -0.000 | 0.008 | no | +0.00 |
| `gen_harbor_customs@rebate-1` | REGIME | fleet-glm53 | 1.000 | 1.000 | +0.000 | 0.000 | no | -16.42 |
| `gen_harbor_customs@rebate-1` | REGIME | gemini-flash | 1.000 | 1.000 | +0.000 | 0.000 | no | -16.42 |
| `gen_sovereign_vaults@crowding-18` | REGIME | gemini-flash | 0.000 | 0.000 | +0.000 | 0.000 | no | -49.42 |
| `gen_sovereign_vaults@crowding-3` | GROUP | gemini-flash | 0.000 | 0.000 | +0.000 | 0.000 | no | -82.37 |
| `gen_sovereign_vaults@crowding-3` | GROUP | haiku | 0.000 | 0.000 | +0.000 | 0.000 | no | -82.37 |
| `ref_exchange@build-slots-4` | REGIME | fleet-kimi3 | 0.000 | 0.000 | +0.000 | 0.000 | no | -7.90 |
| `ref_exchange@build-slots-4` | REGIME | gemini-flash | 0.000 | 0.000 | +0.000 | 0.000 | no | -7.90 |
| `ta_letterauction@contest` | REGIME | fleet-kimi3 | 0.000 | 0.000 | +0.000 | 0.000 | no | -10.80 |
| `ta_letterauction@contest` | REGIME | fleet-qwen38 | 0.000 | 0.000 | +0.000 | 0.000 | no | -10.80 |
| `ta_letterauction@contest` | REGIME | gemini-flash | 0.000 | 0.000 | +0.000 | 0.000 | no | -10.80 |
| `ta_letterauction@contest` | REGIME | gpt-mini | 0.000 | 0.000 | +0.000 | 0.000 | no | -10.80 |
| `ta_liarsdice@rake-1` | GROUP | gemini-flash | 0.000 | 0.000 | +0.000 | 0.000 | no | -2.97 |
| `ta_pubgoods@mf-4` | GROUP | gpt-mini | 0.000 | 0.000 | +0.000 | 0.000 | no | +0.00 |

## Does the behavioural change follow the structural one?

Each row is one (arm, model) at the last round. `dT(N-1)` is what the scripted curves say the knob did to the payoff of deviating when every other seat already exploits -- the corner `selfplay` samples. If models read the regime, a negative `dT(N-1)` should come with a negative `delta`.

- **REGIME**: 12 distinct arms over 6 models (72 arm-model cells). Sign agreement on arm means 10/12; Pearson r(dT(N-1), mean delta) = -0.302 over 12 arms (per-row, pseudo-replicated: -0.214 over 72 rows).
- **GROUP**: 8 distinct arms over 6 models (48 arm-model cells). Sign agreement on arm means 6/8; Pearson r(dT(N-1), mean delta) = -0.233 over 8 arms (per-row, pseudo-replicated: -0.127 over 48 rows).

### Rule-only arms against payoff-moving arms

`dT(N-1)` is the change in what deviating pays at the all-exploit corner. An arm with `dT(N-1) = 0` that still flips its regime class changed the RULES TEXT and the group's stake without changing the deviator's own payoff where this wave samples it. Those two kinds of arm are reported apart because a model can only be tracking the payoff in one of them.

| kind | arms | arm-model cells | mean delta | mean \|delta\| | over floor |
|---|---:|---:|---:|---:|---:|
| payoff moved (|dT(N-1)| >= 1) | 15 | 90 | -0.103 | 0.162 | 44/90 |
| rule only (|dT(N-1)| < 1) | 5 | 30 | -0.265 | 0.294 | 22/30 |

### Headroom, and the relative effect

The strongest predictor of a raw `|delta|` is the BASELINE RATE: a cell already at 0.02 has nowhere to fall. That is a property of the cell, not of the knob, so the arms with room are separated out and the effect is restated as `delta / baseline` -- the fraction of its own exploiting the arm gained or gave up.

- Pearson r(baseline rate, mean |delta|) = +0.772 over 20 arms -- the confound.
- 16 of 20 arms have a baseline at or above 0.15. Below it, a null cannot be told from a floor.

| arm | axis | baseline | relative change | \|delta\| | chars | dT(N-1) |
|---|---|---:|---:|---:|---:|---:|
| `gen_seven_seal@budget-13` | REGIME | 0.669 | -0.688 | 0.407 | 114 | -49.00 |
| `ref_invoice@retainer-40-tight` | REGIME | 0.735 | -0.640 | 0.466 | 143 | +0.00 |
| `gen_quiet_sonar@congested` | REGIME | 0.259 | -0.609 | 0.108 | 141 | -16.50 |
| `ref_invoice@retainer-40` | REGIME | 0.735 | -0.569 | 0.406 | 143 | +0.00 |
| `ref_commons@regen-30` | GROUP | 0.560 | -0.541 | 0.329 | 2 | -0.75 |
| `gen_seven_seal@budget-20` | REGIME | 0.669 | -0.430 | 0.302 | 114 | -55.85 |
| `ta_pubgoods@mf-4` | GROUP | 0.217 | -0.344 | 0.181 | 3 | +0.00 |
| `gen_icebound@steal-5-hard-fail` | REGIME | 0.570 | -0.307 | 0.188 | 2 | -25.00 |
| `gen_frontline_depot@supply-1` | REGIME | 0.771 | -0.273 | 0.278 | 127 | -8.73 |
| `gen_frontline_depot@supply-4` | GROUP | 0.771 | -0.268 | 0.394 | 127 | -13.24 |
| `ref_commons@stock-300` | GROUP | 0.560 | -0.062 | 0.196 | 1 | +35.56 |
| `gen_harbor_customs@rebate-1` | REGIME | 0.780 | -0.017 | 0.036 | 131 | -16.42 |
| `ref_commons@regen-11` | GROUP | 0.560 | +0.145 | 0.181 | 1 | +7.17 |
| `gen_sovereign_vaults@crowding-18` | REGIME | 0.246 | +0.250 | 0.124 | 111 | -49.42 |
| `gen_sovereign_vaults@crowding-3` | GROUP | 0.246 | +0.429 | 0.114 | 109 | -82.37 |
| `gen_quiet_sonar@loss-5` | GROUP | 0.259 | +0.853 | 0.088 | 2 | +0.00 |

**10 of 16 arms with headroom move the baseline's own exploiting by 30% or more.** That is the answer to whether variants produce meaningful behaviour, and it does not depend on either explanation below.

- r(chars rewritten, relative change) = -0.341
- r(dT(N-1), relative change) = -0.102

### Salience against payoff

`chars` is how much of the rules text the knob rewrote. The roster has clean cases at both ends -- `ref_estate@bank-reserve-2` changes ZERO characters (the reserve is never stated; a model can only find it by playing) and `ref_invoice@retainer-40` adds a whole sentence -- so "the model read the regime" and "the model read a new sentence" are separable here rather than confounded.

- Pearson r(chars rewritten, mean |delta|) = +0.327 over 20 arms.
- Pearson r(|dT(N-1)|, mean |delta|) = -0.268 over 20 arms.

| arm | chars rewritten | dT(N-1) | mean \|delta\| | over floor |
|---|---:|---:|---:|---:|
| `ref_invoice@retainer-40` | 143 | +0.00 | 0.406 | 6/6 |
| `ref_invoice@retainer-40-tight` | 143 | +0.00 | 0.466 | 6/6 |
| `gen_quiet_sonar@congested` | 141 | -16.50 | 0.108 | 2/6 |
| `gen_harbor_customs@rebate-1` | 131 | -16.42 | 0.036 | 1/6 |
| `gen_frontline_depot@supply-1` | 127 | -8.73 | 0.278 | 4/6 |
| `gen_frontline_depot@supply-4` | 127 | -13.24 | 0.394 | 5/6 |
| `gen_seven_seal@budget-13` | 114 | -49.00 | 0.407 | 4/6 |
| `gen_seven_seal@budget-20` | 114 | -55.85 | 0.302 | 4/6 |
| `gen_sovereign_vaults@crowding-18` | 111 | -49.42 | 0.124 | 4/6 |
| `gen_sovereign_vaults@crowding-3` | 109 | -82.37 | 0.114 | 2/6 |
| `ref_exchange@build-slots-4` | 90 | -7.90 | 0.016 | 1/6 |
| `ta_letterauction@contest` | 88 | -10.80 | 0.047 | 2/6 |
| `ta_liarsdice@rake-1` | 45 | -2.97 | 0.021 | 3/6 |
| `ta_pubgoods@mf-4` | 3 | +0.00 | 0.181 | 2/6 |
| `gen_icebound@steal-5-hard-fail` | 2 | -25.00 | 0.188 | 2/6 |
| `gen_quiet_sonar@loss-5` | 2 | +0.00 | 0.088 | 3/6 |
| `ref_commons@regen-30` | 2 | -0.75 | 0.329 | 5/6 |
| `ref_commons@regen-11` | 1 | +7.17 | 0.181 | 5/6 |
| `ref_commons@stock-300` | 1 | +35.56 | 0.196 | 3/6 |
| `ref_estate@bank-reserve-2` | 0 | -284.76 | 0.022 | 2/6 |

### The class flips

The arms where the engine stopped rewarding the exploit at the all-exploit corner. These are where a behavioural response is least ambiguous, because the shipped arm and the variant differ in kind and not only in level.

| arm | model | base class -> variant class | base | variant | delta |
|---|---|---|---:|---:|---:|
| `gen_frontline_depot@supply-4` | fleet-glm53 | dominant -> coalition | 0.833 | 0.562 | -0.271 |
| `gen_frontline_depot@supply-4` | fleet-kimi3 | dominant -> coalition | 1.000 | 0.562 | -0.438 |
| `gen_frontline_depot@supply-4` | fleet-qwen38 | dominant -> coalition | 1.000 | 0.521 | -0.479 |
| `gen_frontline_depot@supply-4` | gemini-flash | dominant -> coalition | 0.958 | 0.062 | -0.896 |
| `gen_frontline_depot@supply-4` | gpt-mini | dominant -> coalition | 0.469 | 0.427 | -0.042 |
| `gen_frontline_depot@supply-4` | haiku | dominant -> coalition | 0.365 | 0.604 | +0.240 |
| `gen_seven_seal@budget-13` | fleet-glm53 | dominant -> self-limiting | 0.988 | 0.425 | -0.563 |
| `gen_seven_seal@budget-13` | fleet-kimi3 | dominant -> self-limiting | 0.996 | 0.484 | -0.512 |
| `gen_seven_seal@budget-13` | fleet-qwen38 | dominant -> self-limiting | 0.956 | 0.397 | -0.560 |
| `gen_seven_seal@budget-13` | gemini-flash | dominant -> self-limiting | 1.000 | 0.246 | -0.754 |
| `gen_seven_seal@budget-13` | gpt-mini | dominant -> self-limiting | 0.067 | 0.020 | -0.048 |
| `gen_seven_seal@budget-13` | haiku | dominant -> self-limiting | 0.004 | 0.000 | -0.004 |
| `gen_seven_seal@budget-20` | fleet-glm53 | dominant -> self-limiting | 0.988 | 0.619 | -0.369 |
| `gen_seven_seal@budget-20` | fleet-kimi3 | dominant -> self-limiting | 0.996 | 0.679 | -0.317 |
| `gen_seven_seal@budget-20` | fleet-qwen38 | dominant -> self-limiting | 0.956 | 0.504 | -0.452 |
| `gen_seven_seal@budget-20` | gemini-flash | dominant -> self-limiting | 1.000 | 0.349 | -0.651 |
| `gen_seven_seal@budget-20` | gpt-mini | dominant -> self-limiting | 0.067 | 0.083 | +0.016 |
| `gen_seven_seal@budget-20` | haiku | dominant -> self-limiting | 0.004 | 0.000 | -0.004 |
| `gen_sovereign_vaults@crowding-18` | fleet-glm53 | dominant -> self-limiting | 0.233 | 0.392 | +0.158 |
| `gen_sovereign_vaults@crowding-18` | fleet-kimi3 | dominant -> self-limiting | 0.567 | 0.683 | +0.117 |
| `gen_sovereign_vaults@crowding-18` | fleet-qwen38 | dominant -> self-limiting | 0.642 | 0.233 | -0.408 |
| `gen_sovereign_vaults@crowding-18` | gemini-flash | dominant -> self-limiting | 0.000 | 0.000 | +0.000 |
| `gen_sovereign_vaults@crowding-18` | gpt-mini | dominant -> self-limiting | 0.033 | 0.058 | +0.025 |
| `gen_sovereign_vaults@crowding-18` | haiku | dominant -> self-limiting | 0.000 | 0.033 | +0.033 |
| `gen_sovereign_vaults@crowding-3` | fleet-glm53 | dominant -> no-temptation | 0.233 | 0.750 | +0.517 |
| `gen_sovereign_vaults@crowding-3` | fleet-kimi3 | dominant -> no-temptation | 0.567 | 0.558 | -0.008 |
| `gen_sovereign_vaults@crowding-3` | fleet-qwen38 | dominant -> no-temptation | 0.642 | 0.492 | -0.150 |
| `gen_sovereign_vaults@crowding-3` | gemini-flash | dominant -> no-temptation | 0.000 | 0.000 | +0.000 |
| `gen_sovereign_vaults@crowding-3` | gpt-mini | dominant -> no-temptation | 0.033 | 0.025 | -0.008 |
| `gen_sovereign_vaults@crowding-3` | haiku | dominant -> no-temptation | 0.000 | 0.000 | +0.000 |
| `ref_commons@regen-30` | fleet-glm53 | dominant -> coalition | 0.375 | 0.249 | -0.126 |
| `ref_commons@regen-30` | fleet-kimi3 | dominant -> coalition | 0.582 | 0.222 | -0.360 |
| `ref_commons@regen-30` | fleet-qwen38 | dominant -> coalition | 0.535 | 0.199 | -0.336 |
| `ref_commons@regen-30` | gemini-flash | dominant -> coalition | 0.905 | 0.167 | -0.738 |
| `ref_commons@regen-30` | gpt-mini | dominant -> coalition | 0.510 | 0.249 | -0.261 |
| `ref_commons@regen-30` | haiku | dominant -> coalition | 0.456 | 0.304 | -0.152 |
| `ref_exchange@build-slots-4` | fleet-glm53 | dominant -> self-limiting | 0.028 | 0.033 | +0.006 |
| `ref_exchange@build-slots-4` | fleet-kimi3 | dominant -> self-limiting | 0.000 | 0.000 | +0.000 |
| `ref_exchange@build-slots-4` | fleet-qwen38 | dominant -> self-limiting | 0.028 | 0.000 | -0.028 |
| `ref_exchange@build-slots-4` | gemini-flash | dominant -> self-limiting | 0.000 | 0.000 | +0.000 |
| `ref_exchange@build-slots-4` | gpt-mini | dominant -> self-limiting | 0.089 | 0.061 | -0.028 |
| `ref_exchange@build-slots-4` | haiku | dominant -> self-limiting | 0.072 | 0.039 | -0.033 |
| `ref_invoice@retainer-40` | fleet-glm53 | dominant -> self-limiting | 0.481 | 0.065 | -0.417 |
| `ref_invoice@retainer-40` | fleet-kimi3 | dominant -> self-limiting | 0.898 | 0.273 | -0.625 |
| `ref_invoice@retainer-40` | fleet-qwen38 | dominant -> self-limiting | 0.949 | 0.278 | -0.671 |
| `ref_invoice@retainer-40` | gemini-flash | dominant -> self-limiting | 1.000 | 0.671 | -0.329 |
| `ref_invoice@retainer-40` | gpt-mini | dominant -> self-limiting | 0.898 | 0.593 | -0.306 |
| `ref_invoice@retainer-40` | haiku | dominant -> self-limiting | 0.185 | 0.097 | -0.088 |
| `ref_invoice@retainer-40-tight` | fleet-glm53 | dominant -> coalition | 0.481 | 0.000 | -0.481 |
| `ref_invoice@retainer-40-tight` | fleet-kimi3 | dominant -> coalition | 0.898 | 0.139 | -0.759 |
| `ref_invoice@retainer-40-tight` | fleet-qwen38 | dominant -> coalition | 0.949 | 0.134 | -0.815 |
| `ref_invoice@retainer-40-tight` | gemini-flash | dominant -> coalition | 1.000 | 0.588 | -0.412 |
| `ref_invoice@retainer-40-tight` | gpt-mini | dominant -> coalition | 0.898 | 0.653 | -0.245 |
| `ref_invoice@retainer-40-tight` | haiku | dominant -> coalition | 0.185 | 0.102 | -0.083 |
