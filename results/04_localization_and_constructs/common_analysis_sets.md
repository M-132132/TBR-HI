# Common analysis sets

[Guide](README.md) · [Player count and size](player_count_results.md) · [Definitions](../DATA_DICTIONARY.md)

These tables display the 126 component estimates, 48 paired contrasts and
24 coverage records in Supplementary Data D15. They accompany Figure 7a–d and
Supplementary S5a–d. Estimates and intervals are rounded to four decimals, p/q to
six decimals. NA denotes an unavailable statistic. No per-scene records are included.

Top-1 requires at least two candidates; Hit@3 and NDCG@3 at least four; Spearman
at least three and nonconstant variables. NDCG also requires positive ideal DCG.
Each direct construct comparison retains scenes valid for both sides of that
metric. Component means, intervals and paired differences use the same scenes
and bootstrap indices (2,000 scene-bootstrap replicates). Different comparisons
can therefore have different valid scene counts, even within the same panel.
The descriptive relations in [Selected tables](tables.md) retain their separate
analysis scopes and must not be substituted for these paired component means.

## Panel a: dependence–response and dependence–future-risk

Players have finite D, Rs, Rt, Gs and Gt. Spatial and temporal comparisons separately intersect their metric-valid scenes. The eight paired tests (two dimensions × four metrics) form BH family A per model.

### Panel a: AutoBot

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| D → Rs | Top-1 | localization | 29,237 | 124,152 | 0.6381 [0.6329, 0.6436] |
| D → Gs | Top-1 | localization | 29,237 | 124,152 | 0.3521 [0.3464, 0.3575] |
| D → Rs | Hit@3 | localization | 18,628 | 96,223 | 0.8872 [0.8828, 0.8917] |
| D → Gs | Hit@3 | localization | 18,628 | 96,223 | 0.6949 [0.6881, 0.7015] |
| D → Rs | NDCG@3 | localization | 18,628 | 96,223 | 0.8610 [0.8582, 0.8637] |
| D → Gs | NDCG@3 | localization | 18,628 | 96,223 | 0.5531 [0.5483, 0.5579] |
| D → Rs | Spearman | localization | 25,320 | 116,298 | 0.5510 [0.5448, 0.5570] |
| D → Gs | Spearman | localization | 25,320 | 116,298 | 0.1663 [0.1596, 0.1731] |
| D → Rt | Top-1 | localization | 29,237 | 124,152 | 0.7074 [0.7019, 0.7127] |
| D → Gt | Top-1 | localization | 29,237 | 124,152 | 0.3640 [0.3584, 0.3692] |
| D → Rt | Hit@3 | localization | 18,628 | 96,223 | 0.9352 [0.9315, 0.9387] |
| D → Gt | Hit@3 | localization | 18,628 | 96,223 | 0.6980 [0.6912, 0.7045] |
| D → Rt | NDCG@3 | localization | 18,464 | 95,464 | 0.8860 [0.8835, 0.8885] |
| D → Gt | NDCG@3 | localization | 18,464 | 95,464 | 0.5895 [0.5851, 0.5939] |
| D → Rt | Spearman | localization | 24,939 | 114,794 | 0.6366 [0.6314, 0.6419] |
| D → Gt | Spearman | localization | 24,939 | 114,794 | 0.1747 [0.1682, 0.1817] |

#### Paired comparisons

| Left relation − right relation | Metric | Paired scenes | Left mean | Right mean | Difference [95% CI] | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D → Rs − D → Gs | Top-1 | 29,237 | 0.6381 | 0.3521 | 0.2860 [0.2785, 0.2933] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | Hit@3 | 18,628 | 0.8872 | 0.6949 | 0.1923 [0.1846, 0.2000] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | NDCG@3 | 18,628 | 0.8610 | 0.5531 | 0.3079 [0.3026, 0.3131] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | Spearman | 25,320 | 0.5510 | 0.1663 | 0.3847 [0.3759, 0.3930] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Top-1 | 29,237 | 0.7074 | 0.3640 | 0.3434 [0.3358, 0.3507] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Hit@3 | 18,628 | 0.9352 | 0.6980 | 0.2372 [0.2299, 0.2446] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | NDCG@3 | 18,464 | 0.8860 | 0.5895 | 0.2965 [0.2917, 0.3014] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Spearman | 24,939 | 0.6366 | 0.1747 | 0.4620 [0.4541, 0.4698] | 0.000500 | 0.000500 |

### Panel a: Wayformer

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| D → Rs | Top-1 | localization | 27,618 | 113,292 | 0.6928 [0.6874, 0.6983] |
| D → Gs | Top-1 | localization | 27,618 | 113,292 | 0.4611 [0.4552, 0.4669] |
| D → Rs | Hit@3 | localization | 15,814 | 83,056 | 0.8995 [0.8948, 0.9039] |
| D → Gs | Hit@3 | localization | 15,814 | 83,056 | 0.7897 [0.7835, 0.7959] |
| D → Rs | NDCG@3 | localization | 15,814 | 83,056 | 0.8582 [0.8546, 0.8614] |
| D → Gs | NDCG@3 | localization | 15,814 | 83,056 | 0.6541 [0.6489, 0.6593] |
| D → Rs | Spearman | localization | 22,431 | 102,901 | 0.5948 [0.5889, 0.6007] |
| D → Gs | Spearman | localization | 22,431 | 102,901 | 0.3260 [0.3189, 0.3331] |
| D → Rt | Top-1 | localization | 27,618 | 113,292 | 0.6922 [0.6869, 0.6978] |
| D → Gt | Top-1 | localization | 27,618 | 113,292 | 0.3977 [0.3921, 0.4035] |
| D → Rt | Hit@3 | localization | 15,814 | 83,056 | 0.8974 [0.8927, 0.9024] |
| D → Gt | Hit@3 | localization | 15,814 | 83,056 | 0.7229 [0.7160, 0.7297] |
| D → Rt | NDCG@3 | localization | 15,781 | 82,920 | 0.8579 [0.8545, 0.8613] |
| D → Gt | NDCG@3 | localization | 15,781 | 82,920 | 0.6129 [0.6081, 0.6177] |
| D → Rt | Spearman | localization | 22,297 | 102,462 | 0.5952 [0.5895, 0.6005] |
| D → Gt | Spearman | localization | 22,297 | 102,462 | 0.2036 [0.1964, 0.2110] |

#### Paired comparisons

| Left relation − right relation | Metric | Paired scenes | Left mean | Right mean | Difference [95% CI] | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D → Rs − D → Gs | Top-1 | 27,618 | 0.6928 | 0.4611 | 0.2316 [0.2244, 0.2388] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | Hit@3 | 15,814 | 0.8995 | 0.7897 | 0.1098 [0.1024, 0.1171] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | NDCG@3 | 15,814 | 0.8582 | 0.6541 | 0.2040 [0.1984, 0.2095] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | Spearman | 22,431 | 0.5948 | 0.3260 | 0.2688 [0.2608, 0.2767] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Top-1 | 27,618 | 0.6922 | 0.3977 | 0.2944 [0.2869, 0.3022] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Hit@3 | 15,814 | 0.8974 | 0.7229 | 0.1745 [0.1669, 0.1823] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | NDCG@3 | 15,781 | 0.8579 | 0.6129 | 0.2450 [0.2394, 0.2508] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Spearman | 22,297 | 0.5952 | 0.2036 | 0.3916 [0.3836, 0.4001] | 0.000500 | 0.000500 |

### Panel a: EMP-M

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| D → Rs | Top-1 | localization | 27,209 | 104,191 | 0.5643 [0.5583, 0.5705] |
| D → Gs | Top-1 | localization | 27,209 | 104,191 | 0.3622 [0.3564, 0.3679] |
| D → Rs | Hit@3 | localization | 14,179 | 70,988 | 0.8256 [0.8190, 0.8316] |
| D → Gs | Hit@3 | localization | 14,179 | 70,988 | 0.6902 [0.6826, 0.6977] |
| D → Rs | NDCG@3 | localization | 14,179 | 70,988 | 0.7797 [0.7759, 0.7836] |
| D → Gs | NDCG@3 | localization | 14,179 | 70,988 | 0.5398 [0.5342, 0.5451] |
| D → Rs | Spearman | localization | 18,597 | 80,325 | 0.4481 [0.4406, 0.4551] |
| D → Gs | Spearman | localization | 18,597 | 80,325 | 0.2182 [0.2096, 0.2263] |
| D → Rt | Top-1 | localization | 27,209 | 104,191 | 0.5584 [0.5525, 0.5642] |
| D → Gt | Top-1 | localization | 27,209 | 104,191 | 0.3676 [0.3615, 0.3736] |
| D → Rt | Hit@3 | localization | 14,179 | 70,988 | 0.8158 [0.8096, 0.8217] |
| D → Gt | Hit@3 | localization | 14,179 | 70,988 | 0.6788 [0.6710, 0.6863] |
| D → Rt | NDCG@3 | localization | 14,148 | 70,860 | 0.7745 [0.7701, 0.7785] |
| D → Gt | NDCG@3 | localization | 14,148 | 70,860 | 0.5798 [0.5749, 0.5846] |
| D → Rt | Spearman | localization | 18,472 | 79,916 | 0.4468 [0.4394, 0.4542] |
| D → Gt | Spearman | localization | 18,472 | 79,916 | 0.1684 [0.1602, 0.1768] |

#### Paired comparisons

| Left relation − right relation | Metric | Paired scenes | Left mean | Right mean | Difference [95% CI] | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D → Rs − D → Gs | Top-1 | 27,209 | 0.5643 | 0.3622 | 0.2021 [0.1943, 0.2098] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | Hit@3 | 14,179 | 0.8256 | 0.6902 | 0.1353 [0.1265, 0.1443] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | NDCG@3 | 14,179 | 0.7797 | 0.5398 | 0.2399 [0.2342, 0.2456] | 0.000500 | 0.000500 |
| D → Rs − D → Gs | Spearman | 18,597 | 0.4481 | 0.2182 | 0.2299 [0.2197, 0.2398] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Top-1 | 27,209 | 0.5584 | 0.3676 | 0.1908 [0.1829, 0.1989] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Hit@3 | 14,179 | 0.8158 | 0.6788 | 0.1370 [0.1277, 0.1469] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | NDCG@3 | 14,148 | 0.7745 | 0.5798 | 0.1946 [0.1885, 0.2003] | 0.000500 | 0.000500 |
| D → Rt − D → Gt | Spearman | 18,472 | 0.4468 | 0.1684 | 0.2784 [0.2679, 0.2886] | 0.000500 | 0.000500 |

## Panel b: prediction-based-reference calibration

The five-variable player cohort additionally requires finite Ps and Pt. P–G and R–G comparisons intersect their metric-valid scenes. The eight paired tests form BH family B per model. P–G calibrates construct correspondence; response magnitude is a different quantity from future risk.

### Panel b: AutoBot

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| Ps → Gs | Top-1 | localization | 29,237 | 124,152 | 0.9350 [0.9321, 0.9380] |
| Rs → Gs | Top-1 | localization | 29,237 | 124,152 | 0.3618 [0.3562, 0.3674] |
| Ps → Gs | Hit@3 | localization | 18,628 | 96,223 | 0.9989 [0.9984, 0.9994] |
| Rs → Gs | Hit@3 | localization | 18,628 | 96,223 | 0.7067 [0.7006, 0.7131] |
| Ps → Gs | NDCG@3 | localization | 18,628 | 96,223 | 0.9896 [0.9889, 0.9904] |
| Rs → Gs | NDCG@3 | localization | 18,628 | 96,223 | 0.5657 [0.5608, 0.5708] |
| Ps → Gs | Spearman | localization | 25,320 | 116,298 | 0.9677 [0.9663, 0.9690] |
| Rs → Gs | Spearman | localization | 25,320 | 116,298 | 0.1843 [0.1778, 0.1916] |
| Pt → Gt | Top-1 | localization | 29,237 | 124,152 | 0.8614 [0.8572, 0.8653] |
| Rt → Gt | Top-1 | localization | 29,237 | 124,152 | 0.3643 [0.3587, 0.3699] |
| Pt → Gt | Hit@3 | localization | 18,628 | 96,223 | 0.9939 [0.9928, 0.9949] |
| Rt → Gt | Hit@3 | localization | 18,628 | 96,223 | 0.6957 [0.6891, 0.7023] |
| Pt → Gt | NDCG@3 | localization | 18,564 | 95,952 | 0.9632 [0.9617, 0.9647] |
| Rt → Gt | NDCG@3 | localization | 18,564 | 95,952 | 0.5900 [0.5855, 0.5943] |
| Pt → Gt | Spearman | localization | 24,936 | 114,785 | 0.8882 [0.8852, 0.8911] |
| Rt → Gt | Spearman | localization | 24,936 | 114,785 | 0.1727 [0.1657, 0.1798] |

#### Paired comparisons

| Left relation − right relation | Metric | Paired scenes | Left mean | Right mean | Difference [95% CI] | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ps → Gs − Rs → Gs | Top-1 | 29,237 | 0.9350 | 0.3618 | 0.5732 [0.5672, 0.5794] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | Hit@3 | 18,628 | 0.9989 | 0.7067 | 0.2922 [0.2858, 0.2984] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | NDCG@3 | 18,628 | 0.9896 | 0.5657 | 0.4239 [0.4187, 0.4287] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | Spearman | 25,320 | 0.9677 | 0.1843 | 0.7834 [0.7761, 0.7899] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Top-1 | 29,237 | 0.8614 | 0.3643 | 0.4971 [0.4901, 0.5037] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Hit@3 | 18,628 | 0.9939 | 0.6957 | 0.2982 [0.2914, 0.3048] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | NDCG@3 | 18,564 | 0.9632 | 0.5900 | 0.3732 [0.3687, 0.3777] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Spearman | 24,936 | 0.8882 | 0.1727 | 0.7155 [0.7080, 0.7232] | 0.000500 | 0.000500 |

### Panel b: Wayformer

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| Ps → Gs | Top-1 | localization | 27,618 | 113,292 | 0.9201 [0.9169, 0.9233] |
| Rs → Gs | Top-1 | localization | 27,618 | 113,292 | 0.4650 [0.4591, 0.4708] |
| Ps → Gs | Hit@3 | localization | 15,814 | 83,056 | 0.9994 [0.9991, 0.9997] |
| Rs → Gs | Hit@3 | localization | 15,814 | 83,056 | 0.8222 [0.8161, 0.8282] |
| Ps → Gs | NDCG@3 | localization | 15,814 | 83,056 | 0.9854 [0.9845, 0.9863] |
| Rs → Gs | NDCG@3 | localization | 15,814 | 83,056 | 0.6709 [0.6661, 0.6759] |
| Ps → Gs | Spearman | localization | 22,441 | 102,937 | 0.9605 [0.9589, 0.9620] |
| Rs → Gs | Spearman | localization | 22,441 | 102,937 | 0.3712 [0.3645, 0.3779] |
| Pt → Gt | Top-1 | localization | 27,618 | 113,292 | 0.8366 [0.8325, 0.8409] |
| Rt → Gt | Top-1 | localization | 27,618 | 113,292 | 0.4063 [0.4005, 0.4121] |
| Pt → Gt | Hit@3 | localization | 15,814 | 83,056 | 0.9934 [0.9920, 0.9946] |
| Rt → Gt | Hit@3 | localization | 15,814 | 83,056 | 0.7415 [0.7343, 0.7485] |
| Pt → Gt | NDCG@3 | localization | 15,781 | 82,920 | 0.9499 [0.9481, 0.9518] |
| Rt → Gt | NDCG@3 | localization | 15,781 | 82,920 | 0.6226 [0.6180, 0.6275] |
| Pt → Gt | Spearman | localization | 22,307 | 102,498 | 0.8479 [0.8441, 0.8517] |
| Rt → Gt | Spearman | localization | 22,307 | 102,498 | 0.2311 [0.2238, 0.2390] |

#### Paired comparisons

| Left relation − right relation | Metric | Paired scenes | Left mean | Right mean | Difference [95% CI] | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ps → Gs − Rs → Gs | Top-1 | 27,618 | 0.9201 | 0.4650 | 0.4551 [0.4487, 0.4614] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | Hit@3 | 15,814 | 0.9994 | 0.8222 | 0.1772 [0.1712, 0.1834] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | NDCG@3 | 15,814 | 0.9854 | 0.6709 | 0.3145 [0.3096, 0.3192] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | Spearman | 22,441 | 0.9605 | 0.3712 | 0.5893 [0.5825, 0.5960] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Top-1 | 27,618 | 0.8366 | 0.4063 | 0.4303 [0.4239, 0.4366] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Hit@3 | 15,814 | 0.9934 | 0.7415 | 0.2519 [0.2448, 0.2591] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | NDCG@3 | 15,781 | 0.9499 | 0.6226 | 0.3273 [0.3225, 0.3322] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Spearman | 22,307 | 0.8479 | 0.2311 | 0.6168 [0.6092, 0.6246] | 0.000500 | 0.000500 |

### Panel b: EMP-M

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| Ps → Gs | Top-1 | localization | 27,209 | 104,191 | 0.8891 [0.8854, 0.8927] |
| Rs → Gs | Top-1 | localization | 27,209 | 104,191 | 0.4099 [0.4042, 0.4158] |
| Ps → Gs | Hit@3 | localization | 14,179 | 70,988 | 0.9995 [0.9991, 0.9999] |
| Rs → Gs | Hit@3 | localization | 14,179 | 70,988 | 0.7548 [0.7480, 0.7618] |
| Ps → Gs | NDCG@3 | localization | 14,179 | 70,988 | 0.9739 [0.9725, 0.9752] |
| Rs → Gs | NDCG@3 | localization | 14,179 | 70,988 | 0.6001 [0.5946, 0.6056] |
| Ps → Gs | Spearman | localization | 21,321 | 92,414 | 0.9284 [0.9259, 0.9311] |
| Rs → Gs | Spearman | localization | 21,321 | 92,414 | 0.2651 [0.2575, 0.2725] |
| Pt → Gt | Top-1 | localization | 27,209 | 104,191 | 0.8241 [0.8195, 0.8284] |
| Rt → Gt | Top-1 | localization | 27,209 | 104,191 | 0.3863 [0.3804, 0.3922] |
| Pt → Gt | Hit@3 | localization | 14,179 | 70,988 | 0.9935 [0.9922, 0.9948] |
| Rt → Gt | Hit@3 | localization | 14,179 | 70,988 | 0.7225 [0.7149, 0.7297] |
| Pt → Gt | NDCG@3 | localization | 14,148 | 70,860 | 0.9495 [0.9475, 0.9514] |
| Rt → Gt | NDCG@3 | localization | 14,148 | 70,860 | 0.6099 [0.6049, 0.6145] |
| Pt → Gt | Spearman | localization | 21,187 | 91,977 | 0.8125 [0.8082, 0.8167] |
| Rt → Gt | Spearman | localization | 21,187 | 91,977 | 0.1928 [0.1852, 0.2006] |

#### Paired comparisons

| Left relation − right relation | Metric | Paired scenes | Left mean | Right mean | Difference [95% CI] | p | BH q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ps → Gs − Rs → Gs | Top-1 | 27,209 | 0.8891 | 0.4099 | 0.4791 [0.4729, 0.4860] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | Hit@3 | 14,179 | 0.9995 | 0.7548 | 0.2447 [0.2376, 0.2516] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | NDCG@3 | 14,179 | 0.9739 | 0.6001 | 0.3738 [0.3683, 0.3794] | 0.000500 | 0.000500 |
| Ps → Gs − Rs → Gs | Spearman | 21,321 | 0.9284 | 0.2651 | 0.6633 [0.6557, 0.6711] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Top-1 | 27,209 | 0.8241 | 0.3863 | 0.4377 [0.4307, 0.4446] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Hit@3 | 14,179 | 0.9935 | 0.7225 | 0.2710 [0.2637, 0.2785] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | NDCG@3 | 14,148 | 0.9495 | 0.6099 | 0.3395 [0.3347, 0.3449] | 0.000500 | 0.000500 |
| Pt → Gt − Rt → Gt | Spearman | 21,187 | 0.8125 | 0.1928 | 0.6197 [0.6113, 0.6282] | 0.000500 | 0.000500 |

## Panel c: historical exposure against the same response target

D, Rs, Rt, Hs and Ht use common valid players and the historical five-variable nonconstant scene cohort. All three rankings are evaluated against the same response target. These are the Figure 7c component means; paired historical comparisons are in [Selected tables](tables.md).

### Panel c: AutoBot

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| Hs → Rs | Spearman | spearman | 25,051 | 115,481 | 0.1118 [0.1047, 0.1190] |
| Ht → Rs | Spearman | spearman | 25,051 | 115,481 | 0.1527 [0.1457, 0.1593] |
| D → Rs | Spearman | spearman | 25,051 | 115,481 | 0.5550 [0.5490, 0.5612] |
| Hs → Rt | Spearman | spearman | 25,051 | 115,481 | 0.1043 [0.0972, 0.1114] |
| Ht → Rt | Spearman | spearman | 25,051 | 115,481 | 0.1496 [0.1426, 0.1569] |
| D → Rt | Spearman | spearman | 25,051 | 115,481 | 0.6366 [0.6312, 0.6416] |

### Panel c: Wayformer

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| Hs → Rs | Spearman | spearman | 22,516 | 103,641 | 0.3202 [0.3133, 0.3273] |
| Ht → Rs | Spearman | spearman | 22,516 | 103,641 | 0.2291 [0.2217, 0.2361] |
| D → Rs | Spearman | spearman | 22,516 | 103,641 | 0.5953 [0.5894, 0.6011] |
| Hs → Rt | Spearman | spearman | 22,516 | 103,641 | 0.3121 [0.3052, 0.3190] |
| Ht → Rt | Spearman | spearman | 22,516 | 103,641 | 0.2240 [0.2168, 0.2312] |
| D → Rt | Spearman | spearman | 22,516 | 103,641 | 0.5957 [0.5902, 0.6013] |

### Panel c: EMP-M

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| Hs → Rs | Spearman | spearman | 18,711 | 81,232 | 0.1942 [0.1856, 0.2025] |
| Ht → Rs | Spearman | spearman | 18,711 | 81,232 | 0.1637 [0.1553, 0.1724] |
| D → Rs | Spearman | spearman | 18,711 | 81,232 | 0.4504 [0.4429, 0.4576] |
| Hs → Rt | Spearman | spearman | 18,711 | 81,232 | 0.1974 [0.1891, 0.2058] |
| Ht → Rt | Spearman | spearman | 18,711 | 81,232 | 0.1604 [0.1518, 0.1687] |
| D → Rt | Spearman | spearman | 18,711 | 81,232 | 0.4482 [0.4407, 0.4554] |

## Panel d: historical-exposure adjustment

Raw and adjusted estimates use the same valid complete-case scenes with at least five players, controlling both Hs and Ht. These are the S5d/Figure 7d intervals. The independently resampled ≥5/≥8 D14 sensitivity record is in [Player count and size](player_count_results.md).

### Panel d: AutoBot

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| D → Rs | Spearman | unadjusted | 10,727 | NA | 0.5629 [0.5551, 0.5706] |
| D → Rs | Spearman | partial | 10,727 | NA | 0.5258 [0.5154, 0.5354] |
| D → Rt | Spearman | unadjusted | 10,727 | NA | 0.6487 [0.6423, 0.6553] |
| D → Rt | Spearman | partial | 10,727 | NA | 0.6075 [0.5988, 0.6169] |

### Panel d: Wayformer

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| D → Rs | Spearman | unadjusted | 9,141 | NA | 0.5996 [0.5927, 0.6064] |
| D → Rs | Spearman | partial | 9,141 | NA | 0.5212 [0.5103, 0.5318] |
| D → Rt | Spearman | unadjusted | 9,141 | NA | 0.6036 [0.5967, 0.6105] |
| D → Rt | Spearman | partial | 9,141 | NA | 0.5358 [0.5253, 0.5456] |

### Panel d: EMP-M

| Relation | Metric | Statistic | Valid scenes | Player observations | Mean [95% CI] |
| --- | --- | --- | --- | --- | --- |
| D → Rs | Spearman | unadjusted | 6,482 | NA | 0.4403 [0.4300, 0.4505] |
| D → Rs | Spearman | partial | 6,482 | NA | 0.3871 [0.3729, 0.4013] |
| D → Rt | Spearman | unadjusted | 6,482 | NA | 0.4402 [0.4305, 0.4504] |
| D → Rt | Spearman | partial | 6,482 | NA | 0.3851 [0.3707, 0.3990] |

## Coverage before metric-specific scene filtering

`core_five_variable_queue` is the finite five-variable player intersection;
`positive_control_strict_queue` additionally requires Ps and Pt. Stage coverage
counts do not give the final n for every localization metric. Excluded-player
counts refer to the corresponding matching/finite-value stage.

| Model | Stage | Player records | Scenes | Excluded player records |
| --- | --- | --- | --- | --- |
| AutoBot | D_Rs_Rt | 124,573 | 29,268 | 0 |
| AutoBot | Gs | 125,723 | 30,418 | 0 |
| AutoBot | Gt | 125,723 | 30,418 | 0 |
| AutoBot | core_key_intersection_before_finite | 124,573 | 29,268 | 0 |
| AutoBot | core_five_variable_queue | 124,183 | 29,268 | 390 |
| AutoBot | Ps | 124,183 | 29,268 | 0 |
| AutoBot | Pt | 124,183 | 29,268 | 0 |
| AutoBot | positive_control_strict_queue | 124,183 | 29,268 | 0 |
| Wayformer | D_Rs_Rt | 114,080 | 27,689 | 0 |
| Wayformer | Gs | 116,521 | 30,130 | 0 |
| Wayformer | Gt | 116,521 | 30,130 | 0 |
| Wayformer | core_key_intersection_before_finite | 114,080 | 27,689 | 0 |
| Wayformer | core_five_variable_queue | 113,363 | 27,689 | 717 |
| Wayformer | Ps | 113,363 | 27,689 | 0 |
| Wayformer | Pt | 113,363 | 27,689 | 0 |
| Wayformer | positive_control_strict_queue | 113,363 | 27,689 | 0 |
| EMP-M | D_Rs_Rt | 105,231 | 27,300 | 0 |
| EMP-M | Gs | 108,001 | 30,070 | 0 |
| EMP-M | Gt | 108,001 | 30,070 | 0 |
| EMP-M | core_key_intersection_before_finite | 105,231 | 27,300 | 0 |
| EMP-M | core_five_variable_queue | 104,282 | 27,300 | 949 |
| EMP-M | Ps | 104,282 | 27,300 | 0 |
| EMP-M | Pt | 104,282 | 27,300 | 0 |
| EMP-M | positive_control_strict_queue | 104,282 | 27,300 | 0 |
