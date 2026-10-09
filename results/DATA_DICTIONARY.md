# Result definitions

## Presentation conventions

Results are precomputed aggregate Markdown tables and figures. Numeric values
use a decimal point; counts are integers, even where an older table displays
an integer-valued decimal. Estimates and confidence intervals are rounded for
reading. Blank cells and NA/nan mean unavailable or inapplicable; zero means zero.
No CSV exports or per-scene records are included.

Model identifiers denote AutoBot (autobot), Wayformer (wayformer) and EMP-M
(emp or emp_m). Behaviors are acceleration, deceleration, lateral maneuver,
turning, stable motion (steady_motion) and stationary. Physical tiers are
core relevance (CR/core_relevant), support relevance (SR/support_relevant;
legacy candidate_context) and background (BG/background; legacy background_weak).
Stable and Lateral are the figure labels for stable motion and lateral maneuver.

## Constructs and entity levels

| Quantity | Meaning | Scale |
| --- | --- | --- |
| D / BO1 strength | Absolute allocated single-behavior loss-side dependence | minADE-derived units, metres |
| BO2 strength | Absolute allocated cross-behavior player-pair dependence | minADE-derived units, metres |
| Rs / Rt | Absolute baseline-weighted first- or second-order risk-proxy response | Specified spatial or temporal proxy units |
| Gs / Gt | Ground-truth future-trajectory risk proxy | Specified proxy scale |
| Hs / Ht | Ground-truth historical spatial or TTCE–DCE proximity measure | Specified proximity scale |
| Ps / Pt | Entity-matched full-context prediction risk proxy | Specified proxy scale |
| Minimum clearance | Signed OBB boundary distance | Metres |
| Low-clearance duration | Duration below the specified clearance threshold | Seconds |

A BRT player can contain several surrounding vehicles. Behavioral support order
counts distinct behavior classes in an interaction. Vehicle, player/group and
cross-behavior pair are different entity levels. Equal-share vehicle projection
divides absolute BO1 player strength by its member count. Physical relevance
ranking for response localization uses the maximum member relevance in a player.
Rs/Rt take the absolute value after averaging signed differences across baselines.
D and R share the audited model, entity mapping and baseline family.

## Dependence structure

Occurrence counts count player or pair appearances. Cumulative absolute BO1/BO2
is summed projected dependence; mean absolute dependence describes strength per
occurrence. Shares are fractions unless labeled percent. Occurrence share,
cumulative mass share and per-occurrence mean have different denominators.

Pre-allocation support composition in S2b divides each order's scene-mean absolute
dividend mass by the sum over BO1, BO2 and higher orders: a ratio of means, not
a mean of scene shares. It uses K=6, uniform weights and lambda=0 or 0.25 on
each model's complete-case cohort. The behavior figure's allocated BO1 mass
share has a different denominator. Coalition size counts players, not behaviors.

## Attribution quality and reconstruction

Original-loss deletion ranks players by robust or raw BO1 and evaluates minADE
changes. Magnitude-AUC differences (MoRF minus LeRF or random) are in metres;
larger values indicate stronger deletion separation. This protocol requires at
least two active players.

The aligned method comparison fixes forecast rank 1, K=1 and no shrinkage,
with common BRT players and six-mode minADE over 40 future steps. Phi is the
full-order player projection; BO1 retains single-behavior support. Comparison
methods are BPTShapley, Integrated Gradients and PhaseWinAgent. Endpoint-normalized
deletion/retention values are percentage scales; larger is better. They are
not prediction accuracy and are not clipped to [0,100]. Retention restores
whole players from all replacement; 20/30/50% budgets are vehicle fractions,
with curve interpolation and intact tied-player blocks. Metric-valid n reflects
endpoint filtering. Highest point estimates and significant paired advantages
are different statements.

Original-loss reconstruction averages per-scene MAE/RMSE over nonempty coalitions.
Displayed RMSE is in metres and lower is better. Raw and robust BO1, BO1+BO2 and
full representations keep their explicit targets. Paired RMSE reduction is
RMSE(BO1) minus RMSE(BO1+BO2); positive means improvement. Shrinkage does not
exactly reconstruct the original loss.

## Robustness

K, weight policy and lambda identify baseline variants. Mass means use the
recorded complete-case scenes. Withheld mass and the numerical reconstruction
residual have separate definitions. Variant-difference quantiles are not bootstrap
confidence intervals. K-ranking stability uses Spearman and Top-3 overlap on
common keys. The displayed spatial parameter table reports within-scene Spearman;
it does not evaluate temporal proxy parameters.

## Localization and common analysis sets

Top-1 is top-ranked target agreement. Hit@3 records whether the maximum target
is captured among the first three ranked entities. NDCG@3 uses nonnegative target
scores as relevance. Spearman is within-scene rank correlation. Values are
scene-equal means under their declared validity and tie rules.

For primary nontrivial common-entity analyses, Top-1 requires at least two
candidates, Hit@3/NDCG@3 at least four, and Spearman at least three with
nonconstant variables. NDCG requires positive ideal DCG. Main response
localization has its own target-specific population. Descriptive, all-valid
and paired common-set estimates keep their explicit analysis scopes.

Future-state construct comparisons require finite D, Rs, Rt, Gs and Gt;
prediction-reference comparisons additionally require Ps and Pt. Each direct
comparison intersects metric-valid scenes. Paired means and difference intervals
use those same scenes; subtracting independently valid marginal means is invalid.
The [D15 page](04_localization_and_constructs/common_analysis_sets.md) gives the
components, comparison families and coverage used in Figure 7a–d.

Historical same-target comparisons rank the same response by D, Hs and Ht.
Their paired differences are dependence minus historical-proximity ranking.
Joint adjustment rank-regresses D and the response on both Hs and Ht within
each scene, then correlates residuals on common complete-case scenes.

## Single-vehicle and candidate-count sensitivity

The [D12–D14 page](04_localization_and_constructs/player_count_results.md) gives
the source definitions and metric-specific counts. D12 retains only one-member
BRT players, preserving their original D/R and reranking them. D13 uses all
players before singleton filtering, split by 2, 3, 4 or ≥5 candidates. Random
scores are frozen before filtering. The @3 budget is min(3,n); Hit@3 equals one
for two or three candidates. Its zero paired differences remain in the BH family.
These sensitivity analyses use at least two candidates and differ from the
primary nontrivial @3 eligibility rule. Constant/zero-response coverage is shown.

D14 uses ≥5 and ≥8 common complete players, five finite/nonconstant variables,
a full-rank intercept/Hs/Ht rank-control matrix and centered residual norms
above 1e-10 for D, Rs and Rt. Raw, adjusted and raw-minus-adjusted values use
the same valid scenes within a threshold. Thresholds are nested samples;
their means are not directly subtracted for paired inference. D14 ≥5 confidence
intervals use independent resampling from those in S5d/Figure 7d.

## Behavior response profiles

Overall behavior profiles average tiers within each scene before averaging scenes.
Absolute and signed responses have distinct meanings. The stationary-tier view
shows the same behavior across CR, SR and BG. Effective scene counts identify
the estimable population. Positive BO1 signed response means the risk proxy
increases after replacement; BO2 signs describe second-order deviations from
the sum of single replacements. They do not assign crash responsibility.

## Mismatch, risk strata and fixed budgets

High-set nulls preserve scene-level marginal sizes. HH lift is observed HH
divided by expected HH; mismatch/null ratios and quadrant agreement describe
set correspondence. P upper bounds in the archived null table are bounds,
not exact p values. Response-to-risk ratios divide the specified response
summary by max(ground-truth scene spatial risk, epsilon); floor counts and
epsilon remain explicit. These ratios are descriptive scale diagnostics.

Traffic-state candidate-count adjustment standardizes high-risk-minus-control
performance over exact shared support. Negative differences indicate lower
localization in the high-risk group. This differs from D13's within-stratum
D-versus-reference comparisons. Status fields identify estimable effects.

Fixed-budget strategies rank dependence, response or response-dominant mismatch.
The two-stage rule sorts mismatch first, then response and stable entity keys
for ties. Ground-truth future clearance below 1 m defines a hit. Precision is
hits/budget; lift divides precision by population hit rate. Tie-randomization
intervals summarize 2,000 alternative tie orders; exact min/max give feasible
tie-boundary extremes. They differ from paired scene-bootstrap intervals.
Player-size composition and size-standardized/singleton budget tables are EMP-M
only, at archived display precision.

## Statistical inference

Valid/paired/effective scene counts give the estimable population; entity counts
are not independent scenes. Principal response and paired analyses use 2,000
scene-bootstrap replicates. Some legacy quadrant/reference statistics use 1,000.
Paired intervals come from within-scene differences, not component-interval
subtraction. Unreported uncertainty is not inferred from rounded values.

| Analysis | Testing-family convention |
| --- | --- |
| Aligned attribution comparisons | Centered, plus-one, two-sided empirical p; BH over all 10 method pairs per model and metric |
| Raw-loss reconstruction increment | Two comparisons (raw and robust) per model |
| Historical same-response ranking | Eight comparisons per model |
| D12 singleton localization | 16 comparisons per model |
| D13 candidate-count localization | 64 comparisons per model, including constant Hit@3 differences |
| D14 threshold sensitivity | Separate four-test families per model for adjusted means and raw-minus-adjusted differences |
| D15 construct comparisons | Separate eight-test families A and B per model |
| Fixed budgets | Original nine-test BH family per model and metric |
| Conditional high sets | Unadjusted exploratory empirical p; archived table gives bounds |

Selecting a display does not redefine its source testing family.

The Phi-based [quality-comparison page](02_attribution_quality/method_comparisons.md)
and [additional BO1 page](02_attribution_quality/additional_bo1.md) jointly retain
all 150 source contrasts. Phi represents TBR-HI in the main aligned view.
The [BO2 increment page](04_localization_and_constructs/bo2_increments.md) states
spatial scope and bootstrap counts explicitly. The Figure 5 spatial `all_pairs`
results and the temporal paired results use 2,000 replicates for all three
models. The additional `scored_pairs` records retain 1,000 replicates for
AutoBot and 2,000 for Wayformer/EMP-M, with their separately recorded intervals.
