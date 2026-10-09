# Selected result tables

[Guide](README.md) · [Data dictionary](../DATA_DICTIONARY.md). Display values are rounded. This page contains selected aggregate results; definitions and analysis scope are given in the guide.

## Conditional high-set correspondence

Source: extended conditional high-set table. Archived display precision. p is an upper bound on the unadjusted empirical value.

| paper model | relation name | entity count | observed hh | expected hh | hh lift | mismatch null ratio | p upper bound |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AutoBot | vehicle_Gs_D | 271628 | 14759 | 7670.5100 | 1.9240 | 0.7960 | 0.0005 |
| AutoBot | player_Gs_D_available | 125331 | 11476 | 9150.6100 | 1.2540 | 0.8910 | 0.0005 |
| AutoBot | player_Gs_D_common | 124183 | 10328 | 8002.6100 | 1.2910 | 0.8910 | 0.0005 |
| AutoBot | player_Gs_Rs_common | 124183 | 10613 | 8002.6100 | 1.3260 | 0.8770 | 0.0005 |
| AutoBot | pair_Gs_BO2_common | 183435 | 8073 | 6833.2000 | 1.1810 | 0.9490 | 0.0005 |
| AutoBot | pair_Gs_Rs_common | 183435 | 8038 | 6833.2000 | 1.1760 | 0.9510 | 0.0005 |
| Wayformer | vehicle_Gs_D | 272607 | 18812 | 8924.7700 | 2.1080 | 0.7040 | 0.0005 |
| Wayformer | player_Gs_D_available | 115792 | 15251 | 10494.3600 | 1.4530 | 0.7580 | 0.0005 |
| Wayformer | player_Gs_D_common | 113363 | 12822 | 8065.3600 | 1.5900 | 0.7580 | 0.0005 |
| Wayformer | player_Gs_Rs_common | 113363 | 12931 | 8065.3600 | 1.6030 | 0.7520 | 0.0005 |
| Wayformer | pair_Gs_BO2_common | 176544 | 8326 | 6331.3500 | 1.3150 | 0.9130 | 0.0005 |
| Wayformer | pair_Gs_Rs_common | 176544 | 8218 | 6331.3500 | 1.2980 | 0.9180 | 0.0005 |
| EMP-M | vehicle_Gs_D | 218076 | 15052 | 8864.9600 | 1.6980 | 0.7820 | 0.0005 |
| EMP-M | player_Gs_D_available | 107032 | 12696 | 11130.5100 | 1.1410 | 0.9170 | 0.0005 |
| EMP-M | player_Gs_D_common | 104282 | 9946 | 8380.5100 | 1.1870 | 0.9170 | 0.0005 |
| EMP-M | player_Gs_Rs_common | 104282 | 11243 | 8380.5100 | 1.3420 | 0.8490 | 0.0005 |
| EMP-M | pair_Gs_BO2_common | 146868 | 6679 | 5977.7700 | 1.1170 | 0.9650 | 0.0005 |
| EMP-M | pair_Gs_Rs_common | 146868 | 6693 | 5977.7700 | 1.1200 | 0.9640 | 0.0005 |
| AutoBot | player_D_Rs_common | 124183 | 18656 | 8002.6100 | 2.3310 | 0.4990 | 0.0005 |
| AutoBot | pair_BO2_Rs_common | 183435 | 16442 | 6833.2000 | 2.4060 | 0.6080 | 0.0005 |
| Wayformer | player_D_Rs_common | 113363 | 19226 | 8065.3600 | 2.3840 | 0.4320 | 0.0005 |
| Wayformer | pair_BO2_Rs_common | 176544 | 17315 | 6331.3500 | 2.7350 | 0.5230 | 0.0005 |
| EMP-M | player_D_Rs_common | 104282 | 15448 | 8380.5100 | 1.8430 | 0.6270 | 0.0005 |
| EMP-M | pair_BO2_Rs_common | 146868 | 11432 | 5977.7700 | 1.9120 | 0.7260 | 0.0005 |

## Quadrant agreement

Source: formal quadrant agreement results. Scene-bootstrap intervals on the stated entity population.

| paper model | relation id | cohort name | metric name | estimate | ci95 low | ci95 high |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | vehicle_factual_risk_vs_attribution | available | high_set_jaccard | 0.2109 | 0.2076 | 0.2144 |
| AutoBot | vehicle_factual_risk_vs_attribution | available | phi_mcc | 0.2278 | 0.2225 | 0.2334 |
| AutoBot | group_factual_risk_vs_attribution_available | available | high_set_jaccard | 0.2324 | 0.2287 | 0.2365 |
| AutoBot | group_factual_risk_vs_attribution_available | available | phi_mcc | 0.1776 | 0.1713 | 0.1844 |
| AutoBot | group_factual_risk_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.2142 | 0.2101 | 0.2181 |
| AutoBot | group_factual_risk_vs_attribution_triad_common | triad_common | phi_mcc | 0.1532 | 0.1463 | 0.1599 |
| AutoBot | group_safety_response_vs_attribution | triad_common | high_set_jaccard | 0.4676 | 0.4616 | 0.4735 |
| AutoBot | group_safety_response_vs_attribution | triad_common | phi_mcc | 0.5254 | 0.5180 | 0.5322 |
| AutoBot | group_factual_risk_vs_safety_response | triad_common | high_set_jaccard | 0.2214 | 0.2171 | 0.2252 |
| AutoBot | group_factual_risk_vs_safety_response | triad_common | phi_mcc | 0.1659 | 0.1586 | 0.1723 |
| AutoBot | pair_safety_response_vs_attribution_available | available | high_set_jaccard | 0.3550 | 0.3502 | 0.3601 |
| AutoBot | pair_safety_response_vs_attribution_available | available | phi_mcc | 0.4264 | 0.4201 | 0.4329 |
| AutoBot | pair_exposure_risk_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.1479 | 0.1448 | 0.1511 |
| AutoBot | pair_exposure_risk_vs_attribution_triad_common | triad_common | phi_mcc | 0.1048 | 0.0992 | 0.1105 |
| AutoBot | pair_safety_response_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.3557 | 0.3504 | 0.3608 |
| AutoBot | pair_safety_response_vs_attribution_triad_common | triad_common | phi_mcc | 0.4269 | 0.4199 | 0.4336 |
| AutoBot | pair_exposure_risk_vs_safety_response | triad_common | high_set_jaccard | 0.1472 | 0.1440 | 0.1504 |
| AutoBot | pair_exposure_risk_vs_safety_response | triad_common | phi_mcc | 0.1034 | 0.0978 | 0.1093 |
| Wayformer | vehicle_factual_risk_vs_attribution | available | high_set_jaccard | 0.2853 | 0.2815 | 0.2893 |
| Wayformer | vehicle_factual_risk_vs_attribution | available | phi_mcc | 0.3417 | 0.3363 | 0.3473 |
| Wayformer | group_factual_risk_vs_attribution_available | available | high_set_jaccard | 0.3384 | 0.3333 | 0.3434 |
| Wayformer | group_factual_risk_vs_attribution_available | available | phi_mcc | 0.3316 | 0.3242 | 0.3389 |
| Wayformer | group_factual_risk_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.3007 | 0.2958 | 0.3054 |
| Wayformer | group_factual_risk_vs_attribution_triad_common | triad_common | phi_mcc | 0.2883 | 0.2806 | 0.2954 |
| Wayformer | group_safety_response_vs_attribution | triad_common | high_set_jaccard | 0.5306 | 0.5245 | 0.5370 |
| Wayformer | group_safety_response_vs_attribution | triad_common | phi_mcc | 0.5940 | 0.5871 | 0.6011 |
| Wayformer | group_factual_risk_vs_safety_response | triad_common | high_set_jaccard | 0.3041 | 0.2990 | 0.3090 |
| Wayformer | group_factual_risk_vs_safety_response | triad_common | phi_mcc | 0.2935 | 0.2859 | 0.3011 |
| Wayformer | pair_safety_response_vs_attribution_available | available | high_set_jaccard | 0.4157 | 0.4100 | 0.4212 |
| Wayformer | pair_safety_response_vs_attribution_available | available | phi_mcc | 0.5056 | 0.4988 | 0.5122 |
| Wayformer | pair_exposure_risk_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.1652 | 0.1616 | 0.1687 |
| Wayformer | pair_exposure_risk_vs_attribution_triad_common | triad_common | phi_mcc | 0.1406 | 0.1344 | 0.1466 |
| Wayformer | pair_safety_response_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.4181 | 0.4123 | 0.4236 |
| Wayformer | pair_safety_response_vs_attribution_triad_common | triad_common | phi_mcc | 0.5078 | 0.5009 | 0.5142 |
| Wayformer | pair_exposure_risk_vs_safety_response | triad_common | high_set_jaccard | 0.1627 | 0.1592 | 0.1661 |
| Wayformer | pair_exposure_risk_vs_safety_response | triad_common | phi_mcc | 0.1362 | 0.1301 | 0.1420 |
| EMP-M | vehicle_factual_risk_vs_attribution | available | high_set_jaccard | 0.2534 | 0.2497 | 0.2574 |
| EMP-M | vehicle_factual_risk_vs_attribution | available | phi_mcc | 0.2818 | 0.2760 | 0.2876 |
| EMP-M | group_factual_risk_vs_attribution_available | available | high_set_jaccard | 0.2678 | 0.2632 | 0.2724 |
| EMP-M | group_factual_risk_vs_attribution_available | available | phi_mcc | 0.1969 | 0.1895 | 0.2044 |
| EMP-M | group_factual_risk_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.2227 | 0.2184 | 0.2269 |
| EMP-M | group_factual_risk_vs_attribution_triad_common | triad_common | phi_mcc | 0.1387 | 0.1311 | 0.1461 |
| EMP-M | group_safety_response_vs_attribution | triad_common | high_set_jaccard | 0.3944 | 0.3886 | 0.4000 |
| EMP-M | group_safety_response_vs_attribution | triad_common | phi_mcc | 0.4117 | 0.4036 | 0.4193 |
| EMP-M | group_factual_risk_vs_safety_response | triad_common | high_set_jaccard | 0.2592 | 0.2549 | 0.2638 |
| EMP-M | group_factual_risk_vs_safety_response | triad_common | phi_mcc | 0.2031 | 0.1956 | 0.2105 |
| EMP-M | pair_safety_response_vs_attribution_available | available | high_set_jaccard | 0.2802 | 0.2753 | 0.2851 |
| EMP-M | pair_safety_response_vs_attribution_available | available | phi_mcc | 0.3192 | 0.3120 | 0.3263 |
| EMP-M | pair_exposure_risk_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.1482 | 0.1446 | 0.1517 |
| EMP-M | pair_exposure_risk_vs_attribution_triad_common | triad_common | phi_mcc | 0.0996 | 0.0933 | 0.1057 |
| EMP-M | pair_safety_response_vs_attribution_triad_common | triad_common | high_set_jaccard | 0.2837 | 0.2788 | 0.2887 |
| EMP-M | pair_safety_response_vs_attribution_triad_common | triad_common | phi_mcc | 0.3227 | 0.3154 | 0.3297 |
| EMP-M | pair_exposure_risk_vs_safety_response | triad_common | high_set_jaccard | 0.1486 | 0.1450 | 0.1520 |
| EMP-M | pair_exposure_risk_vs_safety_response | triad_common | phi_mcc | 0.1003 | 0.0940 | 0.1064 |

## Response-to-risk scale

Source: formal response-to-risk scale diagnostics. Maximum entity response divided by floored ground-truth scene risk; descriptive only.

| paper model | order name | scene count | epsilon | factual risk floored count | ratio median | ratio q90 | ratio ge 1 rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AutoBot | bo1 | 29268 | 1.000e-06 | 1387 | 0.0042 | 0.2127 | 0.0372 |
| AutoBot | bo2 | 24129 | 1.000e-06 | 806 | 0.0010 | 0.0771 | 0.0114 |
| Wayformer | bo1 | 27689 | 1.000e-06 | 868 | 0.0171 | 1.0548 | 0.1021 |
| Wayformer | bo2 | 22329 | 1.000e-06 | 390 | 0.0025 | 0.0577 | 0.0185 |
| EMP-M | bo1 | 27300 | 1.000e-06 | 848 | 0.0231 | 0.6185 | 0.0820 |
| EMP-M | bo2 | 21315 | 1.000e-06 | 370 | 0.0071 | 0.1283 | 0.0358 |
