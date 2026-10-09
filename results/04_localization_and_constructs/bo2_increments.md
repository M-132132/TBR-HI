# BO2 response-localization increments

[Guide](README.md) · [Selected tables](tables.md) · [Definitions](../DATA_DICTIONARY.md)

The paired comparison is explicit BO2 minus the sum of absolute BO1 dependences
of the two players. A positive difference favors explicit BO2. All four metrics
and all three models are retained, including intervals that cross or lie below zero.
Intervals and valid scene counts come from the recorded paired analysis.

## Spatial response: Figure 5 paired results

The formal Figure 5 export uses the `all_pairs` records below. All three models
use 2,000 scene-bootstrap replicates. The point estimates, paired-scene counts
and intervals are taken directly from that paired analysis, with values rounded
to six decimals. The marginal scores in Supplementary S4b have their own
metric-valid populations; the paired differences are calculated within scenes.

| Model | Metric | Paired scenes | Difference | 95% CI | Bootstrap replicates |
| --- | --- | --- | --- | --- | --- |
| AutoBot | Top-1 | 24,129 | 0.016080 | [0.009201, 0.022422] | 2,000 |
| AutoBot | Hit@3 | 24,129 | 0.015210 | [0.010277, 0.019769] | 2,000 |
| AutoBot | NDCG@3 | 24,068 | 0.015050 | [0.012461, 0.017585] | 2,000 |
| AutoBot | Spearman | 23,946 | 0.018589 | [0.011840, 0.025248] | 2,000 |
| Wayformer | Top-1 | 22,329 | 0.057504 | [0.050562, 0.065073] | 2,000 |
| Wayformer | Hit@3 | 22,329 | 0.031439 | [0.025796, 0.036947] | 2,000 |
| Wayformer | NDCG@3 | 22,328 | 0.045107 | [0.041497, 0.048762] | 2,000 |
| Wayformer | Spearman | 22,179 | 0.034224 | [0.026391, 0.042216] | 2,000 |
| EMP-M | Top-1 | 21,315 | 0.027539 | [0.020548, 0.034670] | 2,000 |
| EMP-M | Hit@3 | 21,315 | 0.004035 | [-0.001501, 0.009571] | 2,000 |
| EMP-M | NDCG@3 | 21,261 | 0.014430 | [0.011473, 0.017298] | 2,000 |
| EMP-M | Spearman | 18,303 | -0.012303 | [-0.021961, -0.002130] | 2,000 |

## Temporal response: full-context paired update

These values use the formal full-context temporal-response update and 2,000
scene-bootstrap replicates. Their metric-specific populations are retained.

| Model | Metric | Paired scenes | Difference | 95% CI | Bootstrap replicates |
| --- | --- | --- | --- | --- | --- |
| AutoBot | Hit@3 | 24,129 | 0.011646 | [0.006920, 0.016041] | 2,000 |
| EMP-M | Hit@3 | 21,315 | 0.007506 | [0.002109, 0.012808] | 2,000 |
| Wayformer | Hit@3 | 22,329 | 0.032200 | [0.026378, 0.037845] | 2,000 |
| AutoBot | NDCG@3 | 23,910 | 0.012632 | [0.009895, 0.015366] | 2,000 |
| EMP-M | NDCG@3 | 21,307 | 0.014071 | [0.011051, 0.017186] | 2,000 |
| Wayformer | NDCG@3 | 22,324 | 0.043757 | [0.040100, 0.047551] | 2,000 |
| AutoBot | Spearman | 23,747 | 0.012576 | [0.005894, 0.019367] | 2,000 |
| EMP-M | Spearman | 18,314 | -0.010333 | [-0.020228, -0.000970] | 2,000 |
| Wayformer | Spearman | 22,167 | 0.033581 | [0.025503, 0.041536] | 2,000 |
| AutoBot | Top-1 | 24,129 | 0.011314 | [0.004433, 0.017821] | 2,000 |
| EMP-M | Top-1 | 21,315 | 0.030401 | [0.023129, 0.037204] | 2,000 |
| Wayformer | Top-1 | 22,329 | 0.054727 | [0.046845, 0.061894] | 2,000 |

## Additional scored-pair records

The retained `scored_pairs` source records have the same mean differences and
paired-scene counts as the spatial table above, with separately recorded
bootstrap intervals. AutoBot's records in this additional scope use 1,000
replicates; Wayformer and EMP-M use 2,000. These records belong to the same
analysis and provide an additional view of its reporting scope. The Figure 5
paired results use the 2,000-replicate `all_pairs` table above.

| Model | Metric | Paired scenes | Difference | 95% CI | Bootstrap replicates |
| --- | --- | --- | --- | --- | --- |
| AutoBot | Top-1 | 24,129 | 0.016080 | [0.009035, 0.022298] | 1,000 |
| AutoBot | Hit@3 | 24,129 | 0.015210 | [0.010444, 0.020019] | 1,000 |
| AutoBot | NDCG@3 | 24,068 | 0.015050 | [0.012599, 0.017706] | 1,000 |
| AutoBot | Spearman | 23,946 | 0.018589 | [0.011850, 0.025145] | 1,000 |
| Wayformer | Top-1 | 22,329 | 0.057504 | [0.049843, 0.064804] | 2,000 |
| Wayformer | Hit@3 | 22,329 | 0.031439 | [0.025706, 0.037173] | 2,000 |
| Wayformer | NDCG@3 | 22,328 | 0.045107 | [0.041476, 0.048749] | 2,000 |
| Wayformer | Spearman | 22,179 | 0.034224 | [0.026235, 0.042007] | 2,000 |
| EMP-M | Top-1 | 21,315 | 0.027539 | [0.020361, 0.034670] | 2,000 |
| EMP-M | Hit@3 | 21,315 | 0.004035 | [-0.001315, 0.009572] | 2,000 |
| EMP-M | NDCG@3 | 21,261 | 0.014430 | [0.011367, 0.017422] | 2,000 |
| EMP-M | Spearman | 18,303 | -0.012303 | [-0.021601, -0.002562] | 2,000 |
