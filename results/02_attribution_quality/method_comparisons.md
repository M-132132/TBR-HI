# Paired attribution-quality comparisons

[Guide](README.md) · [Main tables](tables.md) · [Definitions](../DATA_DICTIONARY.md)

The displayed comparison uses Phi and three comparison methods, matching
Supplementary S3b. Phi has the largest point estimate in each of the 15
model-by-metric groups. Pairwise statistical comparisons retain their own
intervals and BH q values below.

## Paired contrasts

Each difference is left method minus right method on common valid scenes.
Intervals use 2,000 scene-bootstrap replicates; empirical two-sided p uses
centering and the plus-one correction. Source BH q values use all ten method
pairs per model and metric, including BO1. The main page contains 90 contrasts;
the [BO1 extension](additional_bo1.md) contains the remaining 60. Selecting a
display does not recalculate the original testing family. Estimates and
intervals are rounded to four decimals, p/q to six decimals.

### AutoBot

| Metric | Left method | Right method | Paired scenes | Difference | 95% CI | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MoRF − LeRF AUC (%) | TBR-HI-Phi | BPTShapley | 20,171 | 0.2635 | [-0.1194, 0.6590] | 0.185907 | 0.206563 |
| MoRF − LeRF AUC (%) | TBR-HI-Phi | IntegratedGradients | 20,171 | 3.1213 | [1.7290, 4.4301] | 0.000500 | 0.001000 |
| MoRF − LeRF AUC (%) | TBR-HI-Phi | PhaseWinAgent | 20,171 | 46.3934 | [43.5079, 49.1856] | 0.000500 | 0.001000 |
| MoRF − LeRF AUC (%) | BPTShapley | IntegratedGradients | 20,171 | 2.8578 | [1.3011, 4.1200] | 0.001000 | 0.001249 |
| MoRF − LeRF AUC (%) | BPTShapley | PhaseWinAgent | 20,171 | 46.1299 | [43.2261, 48.7755] | 0.000500 | 0.001000 |
| MoRF − LeRF AUC (%) | IntegratedGradients | PhaseWinAgent | 20,171 | 43.2721 | [40.3717, 46.0409] | 0.000500 | 0.001000 |
| MoRF − random AUC (%) | TBR-HI-Phi | BPTShapley | 20,171 | 0.0850 | [-0.1345, 0.3125] | 0.430785 | 0.478650 |
| MoRF − random AUC (%) | TBR-HI-Phi | IntegratedGradients | 20,171 | 1.3407 | [0.3770, 2.0889] | 0.002999 | 0.004284 |
| MoRF − random AUC (%) | TBR-HI-Phi | PhaseWinAgent | 20,171 | 23.2589 | [21.8601, 24.7321] | 0.000500 | 0.001249 |
| MoRF − random AUC (%) | BPTShapley | IntegratedGradients | 20,171 | 1.2557 | [0.2160, 2.0265] | 0.007996 | 0.009995 |
| MoRF − random AUC (%) | BPTShapley | PhaseWinAgent | 20,171 | 23.1739 | [21.7905, 24.5484] | 0.000500 | 0.001249 |
| MoRF − random AUC (%) | IntegratedGradients | PhaseWinAgent | 20,171 | 21.9182 | [20.4086, 23.5345] | 0.000500 | 0.001249 |
| Retention 20% (%) | TBR-HI-Phi | BPTShapley | 20,171 | 0.4481 | [0.0942, 0.8535] | 0.024488 | 0.027209 |
| Retention 20% (%) | TBR-HI-Phi | IntegratedGradients | 20,171 | 3.0523 | [1.4739, 4.4500] | 0.001499 | 0.002142 |
| Retention 20% (%) | TBR-HI-Phi | PhaseWinAgent | 20,171 | 34.7571 | [32.0276, 37.2458] | 0.000500 | 0.001000 |
| Retention 20% (%) | BPTShapley | IntegratedGradients | 20,171 | 2.6042 | [1.1265, 4.1198] | 0.001999 | 0.002499 |
| Retention 20% (%) | BPTShapley | PhaseWinAgent | 20,171 | 34.3090 | [31.7329, 36.8547] | 0.000500 | 0.001000 |
| Retention 20% (%) | IntegratedGradients | PhaseWinAgent | 20,171 | 31.7048 | [29.3840, 34.0696] | 0.000500 | 0.001000 |
| Retention 30% (%) | TBR-HI-Phi | BPTShapley | 20,171 | 0.3145 | [-0.0746, 0.7225] | 0.124438 | 0.138264 |
| Retention 30% (%) | TBR-HI-Phi | IntegratedGradients | 20,171 | 2.6911 | [1.4424, 3.8016] | 0.000500 | 0.000833 |
| Retention 30% (%) | TBR-HI-Phi | PhaseWinAgent | 20,171 | 35.8074 | [33.4871, 38.1854] | 0.000500 | 0.000833 |
| Retention 30% (%) | BPTShapley | IntegratedGradients | 20,171 | 2.3766 | [1.1798, 3.4675] | 0.000500 | 0.000833 |
| Retention 30% (%) | BPTShapley | PhaseWinAgent | 20,171 | 35.4929 | [33.2057, 37.7920] | 0.000500 | 0.000833 |
| Retention 30% (%) | IntegratedGradients | PhaseWinAgent | 20,171 | 33.1163 | [30.7857, 35.4452] | 0.000500 | 0.000833 |
| Retention 50% (%) | TBR-HI-Phi | BPTShapley | 20,171 | 0.1300 | [-0.2419, 0.5625] | 0.515242 | 0.572492 |
| Retention 50% (%) | TBR-HI-Phi | IntegratedGradients | 20,171 | 1.8957 | [1.0124, 2.7824] | 0.000500 | 0.001000 |
| Retention 50% (%) | TBR-HI-Phi | PhaseWinAgent | 20,171 | 30.0481 | [28.0089, 31.9654] | 0.000500 | 0.001000 |
| Retention 50% (%) | BPTShapley | IntegratedGradients | 20,171 | 1.7657 | [0.8194, 2.6334] | 0.001000 | 0.001666 |
| Retention 50% (%) | BPTShapley | PhaseWinAgent | 20,171 | 29.9181 | [28.0030, 31.9071] | 0.000500 | 0.001000 |
| Retention 50% (%) | IntegratedGradients | PhaseWinAgent | 20,171 | 28.1524 | [26.0354, 30.1543] | 0.000500 | 0.001000 |

### Wayformer

| Metric | Left method | Right method | Paired scenes | Difference | 95% CI | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MoRF − LeRF AUC (%) | TBR-HI-Phi | BPTShapley | 20,968 | 1.7447 | [1.1404, 2.3605] | 0.000500 | 0.000625 |
| MoRF − LeRF AUC (%) | TBR-HI-Phi | IntegratedGradients | 20,968 | 2.6380 | [1.8346, 3.4951] | 0.000500 | 0.000625 |
| MoRF − LeRF AUC (%) | TBR-HI-Phi | PhaseWinAgent | 20,968 | 44.0297 | [41.6373, 46.7139] | 0.000500 | 0.000625 |
| MoRF − LeRF AUC (%) | BPTShapley | IntegratedGradients | 20,968 | 0.8933 | [-0.1285, 1.9269] | 0.092454 | 0.092454 |
| MoRF − LeRF AUC (%) | BPTShapley | PhaseWinAgent | 20,968 | 42.2850 | [39.7198, 44.9120] | 0.000500 | 0.000625 |
| MoRF − LeRF AUC (%) | IntegratedGradients | PhaseWinAgent | 20,968 | 41.3917 | [38.8324, 44.1686] | 0.000500 | 0.000625 |
| MoRF − random AUC (%) | TBR-HI-Phi | BPTShapley | 20,968 | 1.0340 | [0.6028, 1.5451] | 0.000500 | 0.000714 |
| MoRF − random AUC (%) | TBR-HI-Phi | IntegratedGradients | 20,968 | 1.4584 | [0.9056, 2.0597] | 0.000500 | 0.000714 |
| MoRF − random AUC (%) | TBR-HI-Phi | PhaseWinAgent | 20,968 | 21.8070 | [20.4178, 23.2445] | 0.000500 | 0.000714 |
| MoRF − random AUC (%) | BPTShapley | IntegratedGradients | 20,968 | 0.4244 | [-0.1459, 0.9889] | 0.144428 | 0.144428 |
| MoRF − random AUC (%) | BPTShapley | PhaseWinAgent | 20,968 | 20.7730 | [19.5030, 22.1263] | 0.000500 | 0.000714 |
| MoRF − random AUC (%) | IntegratedGradients | PhaseWinAgent | 20,968 | 20.3486 | [18.9937, 21.6799] | 0.000500 | 0.000714 |
| Retention 20% (%) | TBR-HI-Phi | BPTShapley | 20,968 | 1.2245 | [0.4763, 1.9597] | 0.002499 | 0.003123 |
| Retention 20% (%) | TBR-HI-Phi | IntegratedGradients | 20,968 | 2.2495 | [0.9171, 3.4516] | 0.001999 | 0.002856 |
| Retention 20% (%) | TBR-HI-Phi | PhaseWinAgent | 20,968 | 33.0453 | [30.5183, 35.5527] | 0.000500 | 0.000833 |
| Retention 20% (%) | BPTShapley | IntegratedGradients | 20,968 | 1.0250 | [-0.3493, 2.2752] | 0.124438 | 0.124438 |
| Retention 20% (%) | BPTShapley | PhaseWinAgent | 20,968 | 31.8207 | [29.6120, 34.1677] | 0.000500 | 0.000833 |
| Retention 20% (%) | IntegratedGradients | PhaseWinAgent | 20,968 | 30.7958 | [28.3279, 33.2078] | 0.000500 | 0.000833 |
| Retention 30% (%) | TBR-HI-Phi | BPTShapley | 20,968 | 0.6390 | [-0.1005, 1.3417] | 0.082959 | 0.082959 |
| Retention 30% (%) | TBR-HI-Phi | IntegratedGradients | 20,968 | 2.1399 | [0.9946, 3.1780] | 0.001000 | 0.001666 |
| Retention 30% (%) | TBR-HI-Phi | PhaseWinAgent | 20,968 | 34.6589 | [32.2018, 37.0815] | 0.000500 | 0.001000 |
| Retention 30% (%) | BPTShapley | IntegratedGradients | 20,968 | 1.5009 | [0.4130, 2.5376] | 0.005497 | 0.006872 |
| Retention 30% (%) | BPTShapley | PhaseWinAgent | 20,968 | 34.0199 | [31.5940, 36.7220] | 0.000500 | 0.001000 |
| Retention 30% (%) | IntegratedGradients | PhaseWinAgent | 20,968 | 32.5190 | [30.0394, 35.0647] | 0.000500 | 0.001000 |
| Retention 50% (%) | TBR-HI-Phi | BPTShapley | 20,968 | 1.0976 | [0.2906, 2.0874] | 0.017491 | 0.024988 |
| Retention 50% (%) | TBR-HI-Phi | IntegratedGradients | 20,968 | 1.4042 | [0.7255, 2.0394] | 0.000500 | 0.000833 |
| Retention 50% (%) | TBR-HI-Phi | PhaseWinAgent | 20,968 | 29.9175 | [27.8085, 32.0839] | 0.000500 | 0.000833 |
| Retention 50% (%) | BPTShapley | IntegratedGradients | 20,968 | 0.3066 | [-0.7506, 1.2481] | 0.522239 | 0.522239 |
| Retention 50% (%) | BPTShapley | PhaseWinAgent | 20,968 | 28.8200 | [26.7620, 30.8862] | 0.000500 | 0.000833 |
| Retention 50% (%) | IntegratedGradients | PhaseWinAgent | 20,968 | 28.5134 | [26.5902, 30.6954] | 0.000500 | 0.000833 |

### EMP-M

| Metric | Left method | Right method | Paired scenes | Difference | 95% CI | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
