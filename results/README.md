# TBR-HI empirical results

This collection accompanies *Safety-sensitive traffic context in multi-agent
trajectory prediction: A behavior-structured audit of model dependence*.
It presents selected aggregate results from the submission supplement and
extended analyses of AutoBot, Wayformer and EMP-M as readable tables and figures.
The repository contains no CSV exports or per-scene result files.

## Browse by research question

| Topic | Question | Start here |
| --- | --- | --- |
| 01. Behavior structure | How are dependence, occurrence frequency, behavior and physical tier related? | [Guide](01_behavior_structure/README.md) · [Tables](01_behavior_structure/tables.md) |
| 02. Attribution quality | How well do scores order deletion and retention, and how much loss information does BO2 retain? | [Guide](02_attribution_quality/README.md) · [Tables](02_attribution_quality/tables.md) |
| 03. Robustness | How do baseline size, weights, shrinkage, endpoint-difference filtering and proxy parameters affect the results? | [Guide](03_robustness/README.md) · [Tables](03_robustness/tables.md) |
| 04. Localization and constructs | How do dependence, response, future risk and historical exposure relate on matched entities? | [Guide](04_localization_and_constructs/README.md) · [Tables](04_localization_and_constructs/tables.md) |
| 05. Behavior response profiles | Which behaviors and physical tiers characterize sensitive contexts? | [Guide](05_behavior_response_profiles/README.md) · [Tables](05_behavior_response_profiles/tables.md) |
| 06. Mismatch and diagnostics | What do high-set correspondence, mismatch, signed responses and scale diagnostics show? | [Guide](06_mismatch_and_diagnostics/README.md) · [Tables](06_mismatch_and_diagnostics/tables.md) |
| 07. Risk and player size | How do traffic-state strata and player size affect interpretation? | [Guide](07_risk_and_player_size/README.md) · [Tables](07_risk_and_player_size/tables.md) |
| 08. Fixed-budget analysis | What happens under Top-100/300/500 budgets, alternative tie policies and size restrictions? | [Guide](08_fixed_budget/README.md) · [Tables](08_fixed_budget/tables.md) |

## Relationship to the paper and supplement

This collection provides readable versions of selected paper and supplementary
statistics together with extended analyses. Repeated estimates preserve the
same underlying analysis; intervals, valid counts and full metric tables help
readers interpret the concise figures and printed tables.

| Repository results | Paper or supplementary counterpart |
| --- | --- |
| Behavior contributions and support composition | Section 5.1, Figure 3 and Supplementary S2a–b; occurrence and median statistics add detail |
| Original-loss deletion and aligned deletion/retention | Supplementary S3a–b and Data D4/D10–D11; additional BO1 estimates and all paired contrasts are retained |
| BO1 response localization and BO2 increments | Figures 4–5 and Supplementary S4a–c; paired increments retain their explicit scope |
| Construct relations and historical-exposure comparisons | Figure 7, Supplementary S5a–d and Data D7–D9/D15; descriptive and paired common sets are separately identified |
| Single-vehicle players and candidate-count sensitivity | Supplementary S4e–f, S5d and Data D12–D14; this page displays all four metrics and coverage |
| Behavior and physical-tier response profiles | Paper Table 3, Supplementary S6 and Data D1–D3 |
| Fixed-budget results and tie policies | Figure 10, Supplementary S7 and its fixed-budget source data; EMP-M size-restricted analyses add detail |

Original-loss reconstruction, conditional high-set tables, quadrant agreement,
response-to-risk scale diagnostics, candidate-adjusted traffic-state effects and
EMP-M player-size analyses extend the printed supplementary tables. Main-text
Table 2 entity-localization comparisons are outside this collection. The formal
Supplementary Data supplies source statistics for the submission analyses;
this repository presents selected aggregates without CSV or per-scene exports.

## Player size, candidate count and common analysis sets

- [D12–D14 tables](04_localization_and_constructs/player_count_results.md):
  single-vehicle BRT players, 2/3/4/≥5 candidate strata and ≥5/≥8 historical-exposure
  adjustment. All four localization metrics, paired comparisons and coverage are shown.
- [D15 tables](04_localization_and_constructs/common_analysis_sets.md):
  the common-set component estimates, paired comparisons and coverage for Figure 7a–d.

These pages correspond to Supplementary S4e, S4f and S5a–d. The accompanying
Supplementary Data contains their formal source statistics. This collection
displays aggregate results; it does not provide benchmark inference or
scene-bootstrap rerun pipelines.

## Read the results correctly

- A BRT player is a group of surrounding vehicles, labeled by behavior and
  target-conditioned physical-relevance tier. Behavioral support order counts
  distinct behavior classes. It does not count member vehicles or players.
- D is loss-side model dependence. Rs and Rt are absolute spatial and temporal
  surrogate safety responses. Signed finite differences are averaged across the
  baseline family before taking their absolute value.
- Gs/Gt describe ground-truth future trajectories; Hs/Ht are historical exposure
  measures; Ps/Pt are entity-matched risk proxies of the full-context prediction.
  These quantities answer different questions.
- Keep model, entity level, target, candidate population, evaluation scope and
  valid-scene count together. Paired differences cannot generally be recovered
  by subtracting separately valid marginal means.
- Estimates, intervals and p/q are rounded for reading. NA and blank cells mean
  unavailable or inapplicable, not zero. Archived display-precision tables are
  identified in their notes.

See [definitions](DATA_DICTIONARY.md), [coverage notes](RELEASE_NOTES.md) and
[reproduction scope](../docs/reproducibility.md). Raw AV2, Waymo and nuScenes
trajectories, model weights and full experiment caches are outside this package.

## Detailed comparison views

- [Attribution-quality paired comparisons](02_attribution_quality/method_comparisons.md)
  use Phi as the main TBR-HI representation; [additional BO1 results](02_attribution_quality/additional_bo1.md)
  retain the other representation and the five-representation retention overview.
- [BO2 localization increments](04_localization_and_constructs/bo2_increments.md)
  show the Figure 5 spatial and temporal paired results with 2,000 bootstrap
  replicates per model, followed by the additional scored-pair records.
