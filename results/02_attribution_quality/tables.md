# Selected result tables

[Guide](README.md) · [Data dictionary](../DATA_DICTIONARY.md). Display values are rounded. This page contains selected aggregate results; definitions and analysis scope are given in the guide.

## Original-loss deletion: robust and raw BO1

Source: formal original-loss deletion results. Magnitude-AUC difference, in metres. Higher values indicate stronger deletion separation.

| model | method | measure | n scenes | estimate | ci lower | ci upper |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | bo1_raw | abs_morf_minus_lerf | 29268 | 0.1045 | 0.1009 | 0.1081 |
| AutoBot | bo1_raw | abs_morf_minus_random | 29268 | 0.0516 | 0.0498 | 0.0534 |
| AutoBot | bo1_robust | abs_morf_minus_lerf | 29268 | 0.1043 | 0.1008 | 0.1080 |
| AutoBot | bo1_robust | abs_morf_minus_random | 29268 | 0.0515 | 0.0497 | 0.0533 |
| Wayformer | bo1_raw | abs_morf_minus_lerf | 27689 | 0.0377 | 0.0367 | 0.0386 |
| Wayformer | bo1_raw | abs_morf_minus_random | 27689 | 0.0184 | 0.0179 | 0.0189 |
| Wayformer | bo1_robust | abs_morf_minus_lerf | 27689 | 0.0368 | 0.0359 | 0.0378 |
| Wayformer | bo1_robust | abs_morf_minus_random | 27689 | 0.0182 | 0.0177 | 0.0187 |
| EMP-M | bo1_raw | abs_morf_minus_lerf | 27300 | 0.0198 | 0.0192 | 0.0204 |
| EMP-M | bo1_raw | abs_morf_minus_random | 27300 | 0.0096 | 0.0093 | 0.0099 |
| EMP-M | bo1_robust | abs_morf_minus_lerf | 27300 | 0.0189 | 0.0183 | 0.0195 |
| EMP-M | bo1_robust | abs_morf_minus_random | 27300 | 0.0094 | 0.0090 | 0.0097 |

## Aligned-baseline deletion and retention

Source: formal aligned-baseline attribution comparison. Phi and three comparison methods, two deletion metrics and three retention budgets; endpoint-normalized percentage scale.

| model name | method variant | metric name | n | mean | ci low | ci high |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | TBR-HI-Phi | morf_minus_lerf_percent_auc | 20171 | 76.2225 | 74.5002 | 77.9765 |
| AutoBot | TBR-HI-Phi | morf_minus_random_percent_auc | 20171 | 38.0438 | 37.0900 | 39.0454 |
| AutoBot | TBR-HI-Phi | sufficiency_retention_percent_0.20 | 20171 | 80.0757 | 77.8184 | 82.4112 |
| AutoBot | TBR-HI-Phi | sufficiency_retention_percent_0.30 | 20171 | 90.6012 | 88.5636 | 92.5563 |
| AutoBot | TBR-HI-Phi | sufficiency_retention_percent_0.50 | 20171 | 98.1342 | 96.8225 | 99.4796 |
| AutoBot | BPTShapley | morf_minus_lerf_percent_auc | 20171 | 75.9590 | 74.1911 | 77.8492 |
| AutoBot | BPTShapley | morf_minus_random_percent_auc | 20171 | 37.9588 | 36.9957 | 38.9306 |
| AutoBot | BPTShapley | sufficiency_retention_percent_0.20 | 20171 | 79.6276 | 77.1364 | 81.8729 |
| AutoBot | BPTShapley | sufficiency_retention_percent_0.30 | 20171 | 90.2867 | 88.2805 | 92.2557 |
| AutoBot | BPTShapley | sufficiency_retention_percent_0.50 | 20171 | 98.0043 | 96.7941 | 99.2242 |
| AutoBot | IntegratedGradients | morf_minus_lerf_percent_auc | 20171 | 73.1012 | 71.2870 | 75.0567 |
| AutoBot | IntegratedGradients | morf_minus_random_percent_auc | 20171 | 36.7031 | 35.7278 | 37.7181 |
| AutoBot | IntegratedGradients | sufficiency_retention_percent_0.20 | 20171 | 77.0234 | 75.0111 | 78.8663 |
| AutoBot | IntegratedGradients | sufficiency_retention_percent_0.30 | 20171 | 87.9101 | 85.9284 | 89.9192 |
| AutoBot | IntegratedGradients | sufficiency_retention_percent_0.50 | 20171 | 96.2386 | 94.8883 | 97.5856 |
| AutoBot | PhaseWinAgent | morf_minus_lerf_percent_auc | 20171 | 29.8291 | 27.3226 | 32.4270 |
| AutoBot | PhaseWinAgent | morf_minus_random_percent_auc | 20171 | 14.7849 | 13.2644 | 16.2677 |
| AutoBot | PhaseWinAgent | sufficiency_retention_percent_0.20 | 20171 | 45.3186 | 43.2729 | 47.5727 |
| AutoBot | PhaseWinAgent | sufficiency_retention_percent_0.30 | 20171 | 54.7938 | 52.6095 | 57.0752 |
| AutoBot | PhaseWinAgent | sufficiency_retention_percent_0.50 | 20171 | 68.0861 | 66.2987 | 69.8182 |
| Wayformer | TBR-HI-Phi | morf_minus_lerf_percent_auc | 20968 | 74.1944 | 72.8271 | 75.7349 |
| Wayformer | TBR-HI-Phi | morf_minus_random_percent_auc | 20968 | 37.0555 | 36.2473 | 37.8839 |
| Wayformer | TBR-HI-Phi | sufficiency_retention_percent_0.20 | 20968 | 76.0274 | 74.1265 | 77.7429 |
| Wayformer | TBR-HI-Phi | sufficiency_retention_percent_0.30 | 20968 | 88.1088 | 86.5318 | 89.7476 |
| Wayformer | TBR-HI-Phi | sufficiency_retention_percent_0.50 | 20968 | 98.2328 | 97.0790 | 99.3696 |
| Wayformer | BPTShapley | morf_minus_lerf_percent_auc | 20968 | 72.4496 | 71.0510 | 73.8886 |
| Wayformer | BPTShapley | morf_minus_random_percent_auc | 20968 | 36.0215 | 35.1910 | 36.8647 |
| Wayformer | BPTShapley | sufficiency_retention_percent_0.20 | 20968 | 74.8028 | 72.8891 | 76.6938 |
| Wayformer | BPTShapley | sufficiency_retention_percent_0.30 | 20968 | 87.4698 | 85.7646 | 89.0977 |
| Wayformer | BPTShapley | sufficiency_retention_percent_0.50 | 20968 | 97.1352 | 95.7514 | 98.4700 |
| Wayformer | IntegratedGradients | morf_minus_lerf_percent_auc | 20968 | 71.5563 | 70.1249 | 73.0933 |
| Wayformer | IntegratedGradients | morf_minus_random_percent_auc | 20968 | 35.5971 | 34.7480 | 36.4716 |
| Wayformer | IntegratedGradients | sufficiency_retention_percent_0.20 | 20968 | 73.7779 | 72.0550 | 75.4307 |
| Wayformer | IntegratedGradients | sufficiency_retention_percent_0.30 | 20968 | 85.9689 | 84.4407 | 87.5431 |
| Wayformer | IntegratedGradients | sufficiency_retention_percent_0.50 | 20968 | 96.8286 | 95.6680 | 98.0058 |
| Wayformer | PhaseWinAgent | morf_minus_lerf_percent_auc | 20968 | 30.1646 | 28.0405 | 32.1766 |
| Wayformer | PhaseWinAgent | morf_minus_random_percent_auc | 20968 | 15.2485 | 14.1056 | 16.3896 |
| Wayformer | PhaseWinAgent | sufficiency_retention_percent_0.20 | 20968 | 42.9821 | 40.6164 | 45.1628 |
| Wayformer | PhaseWinAgent | sufficiency_retention_percent_0.30 | 20968 | 53.4499 | 51.2527 | 55.5723 |
| Wayformer | PhaseWinAgent | sufficiency_retention_percent_0.50 | 20968 | 68.3152 | 66.3466 | 70.0224 |
| EMP-M | TBR-HI-Phi | morf_minus_lerf_percent_auc | 19654 | 70.8660 | 68.2836 | 73.2841 |
| EMP-M | TBR-HI-Phi | morf_minus_random_percent_auc | 19654 | 35.2247 | 33.8898 | 36.6044 |
| EMP-M | TBR-HI-Phi | sufficiency_retention_percent_0.20 | 19654 | 73.5298 | 70.4808 | 76.3881 |
| EMP-M | TBR-HI-Phi | sufficiency_retention_percent_0.30 | 19654 | 89.1063 | 86.0964 | 92.1214 |
| EMP-M | TBR-HI-Phi | sufficiency_retention_percent_0.50 | 19654 | 102.5689 | 100.0934 | 105.2585 |
| EMP-M | BPTShapley | morf_minus_lerf_percent_auc | 19654 | 70.2854 | 67.9478 | 72.5986 |
| EMP-M | BPTShapley | morf_minus_random_percent_auc | 19654 | 35.0397 | 33.6806 | 36.4175 |
| EMP-M | BPTShapley | sufficiency_retention_percent_0.20 | 19654 | 72.8740 | 69.9923 | 75.9289 |
| EMP-M | BPTShapley | sufficiency_retention_percent_0.30 | 19654 | 88.5225 | 85.5905 | 91.5342 |
| EMP-M | BPTShapley | sufficiency_retention_percent_0.50 | 19654 | 102.3346 | 99.6625 | 105.0362 |
| EMP-M | IntegratedGradients | morf_minus_lerf_percent_auc | 19654 | 60.7784 | 57.8953 | 63.4716 |
| EMP-M | IntegratedGradients | morf_minus_random_percent_auc | 19654 | 30.5501 | 29.1281 | 32.0034 |
| EMP-M | IntegratedGradients | sufficiency_retention_percent_0.20 | 19654 | 64.1907 | 61.3253 | 67.0782 |
| EMP-M | IntegratedGradients | sufficiency_retention_percent_0.30 | 19654 | 79.8979 | 76.8500 | 82.9419 |
| EMP-M | IntegratedGradients | sufficiency_retention_percent_0.50 | 19654 | 95.5806 | 93.0582 | 98.2562 |
| EMP-M | PhaseWinAgent | morf_minus_lerf_percent_auc | 19654 | 18.8454 | 15.9367 | 22.0016 |
| EMP-M | PhaseWinAgent | morf_minus_random_percent_auc | 19654 | 10.1040 | 8.4093 | 11.9897 |
| EMP-M | PhaseWinAgent | sufficiency_retention_percent_0.20 | 19654 | 35.3251 | 32.7794 | 37.7829 |
| EMP-M | PhaseWinAgent | sufficiency_retention_percent_0.30 | 19654 | 46.6013 | 43.6801 | 49.5921 |
| EMP-M | PhaseWinAgent | sufficiency_retention_percent_0.50 | 19654 | 64.0460 | 61.2070 | 67.2374 |


[Paired method comparisons](method_comparisons.md) give the corresponding differences and source BH q values. [Additional BO1 results](additional_bo1.md) retain the other TBR-HI representation.

## Original-loss reconstruction

Source: formal original-loss reconstruction results. Scene-mean RMSE in metres; lower is better. All six representations are shown.

| paper model | representation | n scenes | estimate | ci lower | ci upper |
| --- | --- | --- | --- | --- | --- |
| AutoBot | raw_support_le_1 | 30419 | 0.0053 | 0.0050 | 0.0056 |
| AutoBot | raw_support_le_2 | 30419 | 0.0003 | 0.0003 | 0.0004 |
| AutoBot | robust_full | 30419 | 0.0029 | 0.0028 | 0.0030 |
| AutoBot | robust_shapley_additive | 30419 | 0.0067 | 0.0065 | 0.0069 |
| AutoBot | robust_support_le_1 | 30419 | 0.0068 | 0.0066 | 0.0071 |
| AutoBot | robust_support_le_2 | 30419 | 0.0030 | 0.0029 | 0.0031 |
| Wayformer | raw_support_le_1 | 30130 | 0.0037 | 0.0035 | 0.0038 |
| Wayformer | raw_support_le_2 | 30130 | 0.0003 | 0.0003 | 0.0003 |
| Wayformer | robust_full | 30130 | 0.0085 | 0.0084 | 0.0087 |
| Wayformer | robust_shapley_additive | 30130 | 0.0097 | 0.0095 | 0.0098 |
| Wayformer | robust_support_le_1 | 30130 | 0.0098 | 0.0096 | 0.0100 |
| Wayformer | robust_support_le_2 | 30130 | 0.0086 | 0.0084 | 0.0087 |
| EMP-M | raw_support_le_1 | 30070 | 0.0071 | 0.0069 | 0.0073 |
| EMP-M | raw_support_le_2 | 30070 | 0.0011 | 0.0010 | 0.0011 |
| EMP-M | robust_full | 30070 | 0.0067 | 0.0066 | 0.0068 |
| EMP-M | robust_shapley_additive | 30070 | 0.0098 | 0.0096 | 0.0099 |
| EMP-M | robust_support_le_1 | 30070 | 0.0097 | 0.0096 | 0.0099 |
| EMP-M | robust_support_le_2 | 30070 | 0.0069 | 0.0068 | 0.0070 |

## Paired RMSE reduction from adding BO2

Source: formal paired reconstruction differences. BO1 minus BO1+BO2 RMSE; positive means improvement.

| paper model | kind | n scenes | estimate | ci lower | ci upper | q value |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | raw | 30419 | 0.0049 | 0.0047 | 0.0052 | 0.0005 |
| AutoBot | robust | 30419 | 0.0038 | 0.0035 | 0.0040 | 0.0005 |
| Wayformer | raw | 30130 | 0.0034 | 0.0032 | 0.0035 | 0.0005 |
| Wayformer | robust | 30130 | 0.0012 | 0.0012 | 0.0013 | 0.0005 |
| EMP-M | raw | 30070 | 0.0060 | 0.0059 | 0.0062 | 0.0005 |
| EMP-M | robust | 30070 | 0.0028 | 0.0027 | 0.0029 | 0.0005 |

## Additional representation and retention overview

The [BO1 extension](additional_bo1.md) contains its aligned point estimates,
paired comparisons and the five-representation retention figure. The Phi-based
main comparison follows Supplementary S3b.
