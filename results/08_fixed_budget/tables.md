# Selected result tables

[Guide](README.md) · [Data dictionary](../DATA_DICTIONARY.md). Display values are rounded. This page contains selected aggregate results; definitions and analysis scope are given in the guide.

## Fixed-budget point estimates

Source: formal fixed-budget results. BO1 true-future low-clearance endpoint, threshold 1 m.

| paper model | selection strategy | audit budget | below low clearance count | below low clearance precision | low clearance lift |
| --- | --- | --- | --- | --- | --- |
| AutoBot | loss_attribution | 100 | 2 | 0.0200 | 0.4406 |
| AutoBot | loss_attribution | 300 | 9 | 0.0300 | 0.6609 |
| AutoBot | loss_attribution | 500 | 12 | 0.0240 | 0.5287 |
| AutoBot | safety_response | 100 | 2 | 0.0200 | 0.4406 |
| AutoBot | safety_response | 300 | 15 | 0.0500 | 1.1015 |
| AutoBot | safety_response | 500 | 29 | 0.0580 | 1.2777 |
| AutoBot | response_dominant_mismatch | 100 | 14 | 0.1400 | 3.0842 |
| AutoBot | response_dominant_mismatch | 300 | 38 | 0.1267 | 2.7905 |
| AutoBot | response_dominant_mismatch | 500 | 63 | 0.1260 | 2.7758 |
| Wayformer | loss_attribution | 100 | 4 | 0.0400 | 0.8567 |
| Wayformer | loss_attribution | 300 | 13 | 0.0433 | 0.9281 |
| Wayformer | loss_attribution | 500 | 23 | 0.0460 | 0.9852 |
| Wayformer | safety_response | 100 | 0 | 0 | 0 |
| Wayformer | safety_response | 300 | 3 | 0.0100 | 0.2142 |
| Wayformer | safety_response | 500 | 12 | 0.0240 | 0.5140 |
| Wayformer | response_dominant_mismatch | 100 | 8 | 0.0800 | 1.7134 |
| Wayformer | response_dominant_mismatch | 300 | 40 | 0.1333 | 2.8557 |
| Wayformer | response_dominant_mismatch | 500 | 67 | 0.1340 | 2.8699 |
| EMP-M | loss_attribution | 100 | 5 | 0.0500 | 1.0200 |
| EMP-M | loss_attribution | 300 | 19 | 0.0633 | 1.2920 |
| EMP-M | loss_attribution | 500 | 38 | 0.0760 | 1.5504 |
| EMP-M | safety_response | 100 | 2 | 0.0200 | 0.4080 |
| EMP-M | safety_response | 300 | 13 | 0.0433 | 0.8840 |
| EMP-M | safety_response | 500 | 27 | 0.0540 | 1.1016 |
| EMP-M | response_dominant_mismatch | 100 | 11 | 0.1100 | 2.2439 |
| EMP-M | response_dominant_mismatch | 300 | 41 | 0.1367 | 2.7879 |
| EMP-M | response_dominant_mismatch | 500 | 62 | 0.1240 | 2.5295 |

## Paired fixed-budget precision increments

Source: formal fixed-budget results. Two-stage minus comparator; original nine-test BH family is retained.

| model name | audit budget | comparator strategy | estimate | ci95 low | ci95 high | q bh |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | 100 | loss_attribution | 0.1200 | 0.0600 | 0.2100 | 0.0017 |
| AutoBot | 300 | loss_attribution | 0.0967 | 0.0600 | 0.1467 | 0.0009 |
| AutoBot | 500 | loss_attribution | 0.1020 | 0.0699 | 0.1340 | 0.0009 |
| AutoBot | 100 | safety_response | 0.1200 | 0.0600 | 0.2100 | 0.0020 |
| AutoBot | 300 | safety_response | 0.0767 | 0.0367 | 0.1267 | 0.0013 |
| AutoBot | 500 | safety_response | 0.0680 | 0.0320 | 0.1020 | 0.0013 |
| Wayformer | 100 | loss_attribution | 0.0400 | -0.0200 | 0.1100 | 0.3028 |
| Wayformer | 300 | loss_attribution | 0.0900 | 0.0400 | 0.1400 | 0.0019 |
| Wayformer | 500 | loss_attribution | 0.0880 | 0.0540 | 0.1220 | 0.0007 |
| Wayformer | 100 | safety_response | 0.0800 | 0.0300 | 0.1400 | 0.0079 |
| Wayformer | 300 | safety_response | 0.1233 | 0.0800 | 0.1667 | 0.0007 |
| Wayformer | 500 | safety_response | 0.1100 | 0.0760 | 0.1420 | 0.0007 |
| EMP-M | 100 | loss_attribution | 0.0600 | -0.0100 | 0.1400 | 0.1524 |
| EMP-M | 300 | loss_attribution | 0.0733 | 0.0267 | 0.1167 | 0.0052 |
| EMP-M | 500 | loss_attribution | 0.0480 | 0.0120 | 0.0880 | 0.0218 |
| EMP-M | 100 | safety_response | 0.0900 | 0.0200 | 0.1600 | 0.0247 |
| EMP-M | 300 | safety_response | 0.0933 | 0.0566 | 0.1433 | 0.0018 |
| EMP-M | 500 | safety_response | 0.0700 | 0.0340 | 0.1060 | 0.0011 |

## Random tie-policy sensitivity

Source: formal fixed-budget results. Intervals describe the tie-randomization distribution.

| model name | audit budget | stable key value | random tie median | random tie ci95 low | random tie ci95 high | exact tie min | exact tie max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AutoBot | 100 | 0.1400 | 0.0600 | 0.0200 | 0.1100 | 0 | 1 |
| AutoBot | 300 | 0.1267 | 0.0600 | 0.0367 | 0.0867 | 0 | 0.5400 |
| AutoBot | 500 | 0.1260 | 0.0600 | 0.0420 | 0.0800 | 0 | 0.3240 |
| Wayformer | 100 | 0.0800 | 0.0700 | 0.0200 | 0.1200 | 0 | 1 |
| Wayformer | 300 | 0.1333 | 0.0667 | 0.0433 | 0.0967 | 0 | 0.6467 |
| Wayformer | 500 | 0.1340 | 0.0680 | 0.0480 | 0.0900 | 0 | 0.3880 |
| EMP-M | 100 | 0.1100 | 0.0700 | 0.0300 | 0.1300 | 0 | 1 |
| EMP-M | 300 | 0.1367 | 0.0733 | 0.0467 | 0.1033 | 0 | 1 |
| EMP-M | 500 | 0.1240 | 0.0740 | 0.0520 | 0.0960 | 0 | 0.6520 |

## EMP-M size-standardized sensitivity

Source: extended EMP-M size-standardized budget table. Archived four-decimal precision; EMP-M only.

| audit budget | strategy precision | comparator | estimate | ci95 low | ci95 high | q bh |
| --- | --- | --- | --- | --- | --- | --- |
| 100 | 0.0991 | loss_attribution | 0.0504 | -0.0223 | 0.1243 | 0.1699 |
| 100 | 0.0991 | safety_response | 0.0797 | 0.0118 | 0.1385 | 0.0247 |
| 300 | 0.1191 | loss_attribution | 0.0598 | 0.0151 | 0.1029 | 0.0210 |
| 300 | 0.1191 | safety_response | 0.0768 | 0.0419 | 0.1245 | 0.0030 |
| 500 | 0.1121 | loss_attribution | 0.0425 | 0.0091 | 0.0802 | 0.0258 |
| 500 | 0.1121 | safety_response | 0.0624 | 0.0314 | 0.0980 | 0.0030 |

## EMP-M singleton-only sensitivity

Source: extended EMP-M singleton-budget table. Archived four-decimal precision; EMP-M only.

| audit budget | strategy precision | comparator | estimate | ci95 low | ci95 high | q bh |
| --- | --- | --- | --- | --- | --- | --- |
| 100 | 0.0800 | loss_attribution | 0.0700 | 0.0200 | 0.1300 | 0.0306 |
| 100 | 0.0800 | safety_response | 0.0500 | -0.0100 | 0.1200 | 0.1554 |
| 300 | 0.0933 | loss_attribution | 0.0567 | 0.0167 | 0.0934 | 0.0100 |
| 300 | 0.0933 | safety_response | 0.0567 | 0.0167 | 0.0967 | 0.0100 |
| 500 | 0.0880 | loss_attribution | 0.0460 | 0.0160 | 0.0760 | 0.0100 |
| 500 | 0.0880 | safety_response | 0.0420 | 0.0140 | 0.0740 | 0.0127 |
