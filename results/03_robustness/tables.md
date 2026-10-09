# Selected result tables

[Guide](README.md) · [Data dictionary](../DATA_DICTIONARY.md). Display values are rounded. This page contains selected aggregate results; definitions and analysis scope are given in the guide.

## Behavioral-support composition (Supplementary S2b)

Source: formal baseline-family ablation. K=6 and uniform weights on each model's common complete-case scenes. Shares are ratios of pre-allocation mean absolute dividend masses across all three support orders. Lambda=0 denotes no shrinkage; lambda=0.25 is the primary setting.

| Model | Lambda | Scenes | BO1: mean (m); share | BO2: mean (m); share | BO≥3: mean (m); share |
| --- | --- | --- | --- | --- | --- |
| AutoBot | 0 | 30488 | 0.164409; 89.68% | 0.016492; 9.00% | 0.002426; 1.32% |
| AutoBot | 0.2500 | 30488 | 0.159435; 90.07% | 0.015465; 8.74% | 0.002103; 1.19% |
| Wayformer | 0 | 30540 | 0.064418; 83.55% | 0.010824; 14.04% | 0.001860; 2.41% |
| Wayformer | 0.2500 | 30540 | 0.049875; 85.72% | 0.007234; 12.43% | 0.001071; 1.84% |
| EMP-M | 0 | 30543 | 0.064780; 61.01% | 0.029033; 27.34% | 0.012367; 11.65% |
| EMP-M | 0.2500 | 30543 | 0.049858; 65.35% | 0.019425; 25.46% | 0.007012; 9.19% |

## Baseline and shrinkage: BO1 mass

Source: formal baseline-family ablation. Each row keeps its complete-case scene count.

| paper model | variant id | scene count | mean | median |
| --- | --- | --- | --- | --- |
| AutoBot | k1_uniform_lam0.25 | 30488 | 0.1653 | 0.0207 |
| AutoBot | k3_uniform_lam0.25 | 30488 | 0.1604 | 0.0198 |
| AutoBot | k6_mean_probability_lam0.25 | 30488 | 0.1597 | 0.0197 |
| AutoBot | k6_uniform_lam0 | 30488 | 0.1644 | 0.0208 |
| AutoBot | k6_uniform_lam0.1 | 30488 | 0.1624 | 0.0204 |
| AutoBot | k6_uniform_lam0.25 | 30488 | 0.1594 | 0.0197 |
| AutoBot | k6_uniform_lam0.5 | 30488 | 0.1546 | 0.0186 |
| Wayformer | k1_uniform_lam0.25 | 30540 | 0.0592 | 0.0166 |
| Wayformer | k3_uniform_lam0.25 | 30540 | 0.0482 | 0.0136 |
| Wayformer | k6_mean_probability_lam0.25 | 30540 | 0.0454 | 0.0128 |
| Wayformer | k6_uniform_lam0 | 30540 | 0.0644 | 0.0231 |
| Wayformer | k6_uniform_lam0.1 | 30540 | 0.0584 | 0.0199 |
| Wayformer | k6_uniform_lam0.25 | 30540 | 0.0499 | 0.0155 |
| Wayformer | k6_uniform_lam0.5 | 30540 | 0.0374 | 0.0091 |
| EMP-M | k1_uniform_lam0.25 | 30543 | 0.0728 | 0.0305 |
| EMP-M | k3_uniform_lam0.25 | 30543 | 0.0545 | 0.0233 |
| EMP-M | k6_mean_probability_lam0.25 | 30543 | 0.0505 | 0.0209 |
| EMP-M | k6_uniform_lam0 | 30543 | 0.0648 | 0.0315 |
| EMP-M | k6_uniform_lam0.1 | 30543 | 0.0584 | 0.0272 |
| EMP-M | k6_uniform_lam0.25 | 30543 | 0.0499 | 0.0215 |
| EMP-M | k6_uniform_lam0.5 | 30543 | 0.0381 | 0.0132 |

## K-ranking stability

Source: formal K-ranking stability results. Aggregate structure comparison between K=3 and K=6.

| paper model | comparison | metric | value | common key count |
| --- | --- | --- | --- | --- |
| AutoBot | BO1 behavior | rank_spearman_common_keys | 1 | 6 |
| AutoBot | BO1 behavior | top3_overlap_rate | 1 | 6 |
| AutoBot | BO1 behavior-tier | rank_spearman_common_keys | 1 | 18 |
| AutoBot | BO1 behavior-tier | top3_overlap_rate | 1 | 18 |
| AutoBot | BO2 behavior-pair | rank_spearman_common_keys | 0.9964 | 15 |
| AutoBot | BO2 behavior-pair | top3_overlap_rate | 1 | 15 |
| AutoBot | BO2 tier-pair | rank_spearman_common_keys | 1 | 3 |
| AutoBot | BO2 tier-pair | top3_overlap_rate | 1 | 3 |
| Wayformer | BO1 behavior | rank_spearman_common_keys | 0.8857 | 6 |
| Wayformer | BO1 behavior | top3_overlap_rate | 0.6667 | 6 |
| Wayformer | BO1 behavior-tier | rank_spearman_common_keys | 0.9835 | 18 |
| Wayformer | BO1 behavior-tier | top3_overlap_rate | 1 | 18 |
| Wayformer | BO2 behavior-pair | rank_spearman_common_keys | 0.9893 | 15 |
| Wayformer | BO2 behavior-pair | top3_overlap_rate | 0.6667 | 15 |
| Wayformer | BO2 tier-pair | rank_spearman_common_keys | 1 | 3 |
| Wayformer | BO2 tier-pair | top3_overlap_rate | 1 | 3 |
| EMP-M | BO1 behavior | rank_spearman_common_keys | 1 | 6 |
| EMP-M | BO1 behavior | top3_overlap_rate | 1 | 6 |
| EMP-M | BO1 behavior-tier | rank_spearman_common_keys | 0.9979 | 18 |
| EMP-M | BO1 behavior-tier | top3_overlap_rate | 1 | 18 |
| EMP-M | BO2 behavior-pair | rank_spearman_common_keys | 1 | 15 |
| EMP-M | BO2 behavior-pair | top3_overlap_rate | 1 | 15 |
| EMP-M | BO2 tier-pair | rank_spearman_common_keys | 1 | 3 |
| EMP-M | BO2 tier-pair | top3_overlap_rate | 1 | 3 |

## Spatial proxy settings

Source: formal spatial-proxy parameter analysis. Within-scene Spearman.

| paper model | order name | setting name | safe clearance m | temperature m | value | valid count |
| --- | --- | --- | --- | --- | --- | --- |
| AutoBot | bo1 | main | 1 | 1 | 0.5466 | 29220 |
| AutoBot | bo1 | clearance_050 | 0.5000 | 1 | 0.5467 | 29215 |
| AutoBot | bo1 | clearance_150 | 1.5000 | 1 | 0.5471 | 29214 |
| AutoBot | bo1 | temperature_050 | 1 | 0.5000 | 0.5458 | 29182 |
| AutoBot | bo1 | temperature_200 | 1 | 2 | 0.5461 | 29205 |
| Wayformer | bo1 | main | 1 | 1 | 0.5859 | 27607 |
| Wayformer | bo1 | clearance_050 | 0.5000 | 1 | 0.5861 | 27606 |
| Wayformer | bo1 | clearance_150 | 1.5000 | 1 | 0.5865 | 27608 |
| Wayformer | bo1 | temperature_050 | 1 | 0.5000 | 0.5863 | 27593 |
| Wayformer | bo1 | temperature_200 | 1 | 2 | 0.5879 | 27607 |
| EMP-M | bo1 | main | 1 | 1 | 0.4459 | 23911 |
| EMP-M | bo1 | clearance_050 | 0.5000 | 1 | 0.4458 | 23911 |
| EMP-M | bo1 | clearance_150 | 1.5000 | 1 | 0.4460 | 23911 |
| EMP-M | bo1 | temperature_050 | 1 | 0.5000 | 0.4475 | 23899 |
| EMP-M | bo1 | temperature_200 | 1 | 2 | 0.4465 | 23911 |
| AutoBot | bo2 | main | 1 | 1 | 0.4537 | 23959 |
| AutoBot | bo2 | clearance_050 | 0.5000 | 1 | 0.4540 | 23987 |
| AutoBot | bo2 | clearance_150 | 1.5000 | 1 | 0.4521 | 23977 |
| AutoBot | bo2 | temperature_050 | 1 | 0.5000 | 0.4564 | 23991 |
| AutoBot | bo2 | temperature_200 | 1 | 2 | 0.4482 | 23911 |
| Wayformer | bo2 | main | 1 | 1 | 0.5304 | 22249 |
| Wayformer | bo2 | clearance_050 | 0.5000 | 1 | 0.5308 | 22243 |
| Wayformer | bo2 | clearance_150 | 1.5000 | 1 | 0.5315 | 22244 |
| Wayformer | bo2 | temperature_050 | 1 | 0.5000 | 0.5315 | 22244 |
| Wayformer | bo2 | temperature_200 | 1 | 2 | 0.5307 | 22224 |
| EMP-M | bo2 | main | 1 | 1 | 0.3637 | 18466 |
| EMP-M | bo2 | clearance_050 | 0.5000 | 1 | 0.3638 | 18466 |
| EMP-M | bo2 | clearance_150 | 1.5000 | 1 | 0.3652 | 18466 |
| EMP-M | bo2 | temperature_050 | 1 | 0.5000 | 0.3674 | 18462 |
| EMP-M | bo2 | temperature_200 | 1 | 2 | 0.3641 | 18466 |
