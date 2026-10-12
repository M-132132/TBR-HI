# API reference

## Entry points

| Task | Import and call | Inputs |
| --- | --- | --- |
| Decompose existing losses | `from tbr_hi import decompose_loss_tables` | Ordered players, K complete loss-table rows, weights and lambda |
| Construct BRT players | `from tbr_hi.behavior import build_players` | `History` and optional label, family, relevance and grouping configuration |
| Construct baselines | `from tbr_hi.baselines import build_baseline_family` | Replacement history, earlier history and same-model environment callback |
| Evaluate model dependence | `from tbr_hi.coalition import compute_model_dependence` | History, players, family, target callback, true future and mask |
| Evaluate surrogate safety responses | `from tbr_hi.safety import compute_safety_responses` | The same history/players/family, target callback and fixed-future proxy |
| Use precomputed replacement values | `from tbr_hi.safety.response import response_from_replacements` | Players, per-member proxy dictionaries and weights |

The top-level loss-table entry point imports the Python standard library only.
Trajectory APIs use NumPy/PyTorch. [The input contract](input_contract.md) gives
valid shapes, units and numerical inputs; these APIs assume that contract.

## Input containers

`History`, `Prediction`, `EnvironmentForecast` and `BaselineFamily` are defined
in `tbr_hi.interfaces`. `FutureContext` is exported from `tbr_hi.safety`.
Positions, velocities, headings, timestamps and future geometry share one fixed
target coordinate frame. The paper uses 21 historical frames, 20 baseline
forecast positions after the true anchor and the first 40 target-future frames.

### Behavior labels and history coverage

`from tbr_hi.behavior import label_behaviors` returns each eligible vehicle's
`primary_label`, auxiliary `categories`/`all_labels`, and `kinematics`.
Only the primary label defines the behavior dimension used by `build_players`.
The stationary rules include both whole-window stationary and terminal stopping;
their thresholds and precedence are in [method definitions](method.md).

| Coverage field in `kinematics` | Meaning |
| --- | --- |
| `valid_frame_count` | Number of valid historical slots; eligibility uses at least eight |
| `valid_segment_count` | Number of contiguous valid segments |
| `longest_valid_segment_frames` | Number of frames in the longest segment |
| `internal_missing_frame_count` | Invalid slots between first and last valid frames |
| `missing_history_frame_count` | All invalid slots, including prefixes and suffixes |
| `last_history_frame_valid` | Whether the final history slot is valid |
| `valid_time_span_s` | Elapsed time between first and last valid frames on the original axis |
| `duration_s` | Retained `(valid_frame_count - 1) * dt` metric |

Coverage fields do not replace the motion features, add a continuity filter or
enter the primary-label rules. `duration_s` and `valid_time_span_s` can differ
when the history has internal gaps.

### Player construction configuration

The configurations in `tbr_hi.config` separate primary-label rules, behavior
families, physical-relevance scoring and player tiers:

| Configuration | Argument to `build_players` | Role and paper default |
| --- | --- | --- |
| `AnalyzerConfig` | `behavior_config` | Label rules and history eligibility; `min_valid_frames=8`, with the thresholds in `BehaviorThresholds` |
| `BehaviorConfig` | `family_config` | Map primary labels into the six behavior families; None selects the default mapping |
| `InteractionConfig` | `relevance_config` | Physical-relevance score scales, weights and velocity fitting |
| `PlayerGroupingConfig` | `grouping_config` | BRT tier boundaries; `core_threshold=0.40`, `support_threshold=0.25` |

```python
from tbr_hi.behavior import build_players
from tbr_hi.config import BehaviorConfig, PlayerGroupingConfig

players = build_players(
    history,
    family_config=BehaviorConfig(),
    grouping_config=PlayerGroupingConfig(core_threshold=0.40, support_threshold=0.25),
)
```

`group_players(behaviors, physical_scores, grouping_config=...)` uses the same
tier configuration when labels and scores are supplied directly.
`InteractionConfig.threshold` controls the `interaction_level` relevant/weak
diagnostic returned by `compute_target_interactions`; player tiers use
`PlayerGroupingConfig`. The two settings serve separate purposes.

Only the selected primary label enters `BehaviorConfig.families`. Unmapped
labels are excluded; auxiliary labels do not assign a family. Use disjoint
primary-label sets in a custom mapping. If sets overlap, the first matching
family in mapping order is selected. Custom families or tier boundaries define
a different BRT player protocol from the paper defaults.

The following constructor fields are accepted for compatibility and have no
effect in this package's in-memory behavior interface:

| Fields | Interface behavior |
| --- | --- |
| `AnalyzerConfig.dt_default` | Time spacing is read from `History.timestamps` |
| `AnalyzerConfig.allowed_object_types` | Vehicle eligibility uses `History.vehicle_mask` |
| `AnalyzerConfig.processed_kinematic_source` | Motion features are supplied through `History` |
| `BehaviorConfig.unknown_family` | Unmapped primary labels are excluded, with no fallback player group |
| `BehaviorThresholds.congested_ratio_min`, `congested_mean_speed_max`, `lanechange_ratio_min`, `turning_ratio_min`, `interaction_ratio_min`, `risk_ratio_min` | Scene-level tags are not computed |

### Player scores

`BRTPlayer` stores `block_id`, `behavior_id`, `relevance_level` and `track_indices`.
Its `vehicle_count` is the number of member vehicles.

| Field | Meaning | Use |
| --- | --- | --- |
| `physical_score` | Mean member relevance; retained API name | Descriptive group mean |
| `mean_physical_score` | Property returning `physical_score` | Explicit group-mean name |
| `max_physical_score` | Maximum member relevance | Paper physical-relevance reference ranking |

`group_players` calculates both scores. A manually constructed player defaults
`max_physical_score` to None: supply the maximum when using that reference ranking.
A player's mean is not a substitute for its maximum.

### Baseline counts and coverage

The builder ranks each vehicle's modes by probability, matches entities once and
assembles common ranks with uniform weights. It records the requested count while
preserving the source implementation's common-prefix selection.

| Field or method | Meaning |
| --- | --- |
| `requested_member_count` | Requested K; builder default 6, manual-family default None |
| `member_count` | Number of stored histories |
| `actual_member_count` | Stored count if shared environment coverage is nonempty; otherwise 0 |
| `available_tracks` | Environment slots covered by every member |
| `summary()` | Requested/actual/stored counts, covered-track count, weights and whether actual count equals the request |

With no covered environment vehicle, the container stores one unchanged history:
`member_count=1`, `actual_member_count=0`. This is a placeholder, not a one-member
empirical audit. Whole-player coverage is applied by the dependence and response
APIs. A covered vehicle need not form a complete covered BRT player; retain the
excluded and retained player lists alongside the family summary.

The paper's main setting requires six actual members and uniform weights. Record
`summary()` and retain this K=6 eligibility in the caller's analysis. A reduced
common-prefix family is a different setting. Set `requested_member_count` when
supplying a manual family if that comparison is required.

## Dependence outputs

| Key from `decompose_loss_tables` | Meaning |
| --- | --- |
| `baseline_member_count` | Input loss-table row count |
| `D` | Player-ID mapping to absolute BO1 model dependence |
| `behavior_order_one_effects` | Signed and absolute allocated single-behavior dependence |
| `behavior_order_two_pair_allocations` | Allocated cross-behavior pair dependence |
| `behavior_support_effects` | Contributions by distinct behavior support |
| `scene_order_summary` | BO1, BO2, higher-order dependence and shrinkage remainder |
| `robust_dividends` | Per-coalition mean, population standard deviation, robust dividend and withheld contribution |
| `member_dividends` | Per-baseline Harsanyi dividends |
| `checks` | BO1/BO2 allocation consistency, joint contribution conservation and player/support counts |
| `robust_checks` | Baseline count, finite-dividend diagnostics and robust-shrinkage counts/masses |

`compute_model_dependence` also returns `players`, `excluded_players`,
`losses_by_baseline`, `baseline_summary` and `target_valid_frame_count`.
The last count uses the selected minADE evaluation window. Exclude targets with
no valid future frame before evaluating the loss game.

### Optional detail rows

Both dependence entry points accept the keyword-only option
`include_details=True`. The default includes all existing output fields.
With `include_details=False`, `robust_dividends` and `member_dividends` are
omitted. D, BO1/BO2 allocations, behavioral-support contributions, scene
summaries, `checks` and `robust_checks` are retained. The trajectory entry point
also retains its loss tables, coverage and valid-frame information.

```python
summary = decompose_loss_tables(
    players, losses_by_baseline, weights, include_details=False,
)
print(summary["D"])
print(summary["scene_order_summary"])
```

Summary mode skips construction of per-coalition/per-member dividend rows and
the unused coalition track-set mapping. The same weighted means, population
standard deviations, shrinkage and behavioral-support projection are computed
in both modes. Complete loss tables and dividends are still required; exact
decomposition remains exponential in the player count.

BO1 can contain several same-behavior players and differs from full-order Shapley
allocation. `scene_order_summary.total_response` is a retained name for signed
loss-game contribution in metres, not Rs/Rt. Adding `shrinkage_remainder` gives
`mean_full_context_loss_improvement`.

## Response outputs

`response_from_replacements` returns `single`, `pair`, `baseline_member_count`
and normalized `baseline_weights`. Pair entries contain different behaviors only.

| Entry field | Definition |
| --- | --- |
| `block_id` or `left_block_id`/`right_block_id` | Replaced player or pair |
| `member_responses` | Signed first-/second-order differences for each member |
| `signed` | Weighted mean of those differences |
| `absolute` | Absolute value of that mean |
| `variance` | Weighted population variance around the signed mean, equation (19b) |
| `std` | Square root of that variance |

For normalized weights w and differences delta, variance is
`sum(w[k] * (delta[k] - signed)**2)`. It describes variation across baseline
members, not a bootstrap interval or standard error. The response is not shrunk
using this variance. Opposite signed member responses can cancel before `absolute`.

`compute_safety_responses` also returns `players`, `excluded_players`,
`baseline_summary` and `replacement_values`. A proxy callback takes `Prediction`
and holds `FutureContext` fixed in its closure:

```python
from tbr_hi.safety import compute_safety_responses, spatial_proxy

spatial = compute_safety_responses(
    history, players, family, predict_target,
    lambda prediction: spatial_proxy(prediction, future_context),
)
print(spatial["baseline_summary"])
for row in spatial["single"]:
    print(row["block_id"], row["absolute"], row["variance"])
```

Precomputed member dictionaries use `()` for full context, `(i,)` for single
replacement and `(i,j)` (i < j) for each cross-behavior pair, with the same ordered
player list across all members.

## Module map

| Modules | Responsibility |
| --- | --- |
| `config` | Label, family, relevance-score and player-tier configurations |
| `behavior`, `_behavior.features`, `_behavior.rules` | Behavior entry points, kinematic evidence and primary labels |
| `relevance`, `players` | Physical relevance, tiers, grouping and coverage |
| `interfaces`, `baselines` | Contracts, matching, baselines and kinematic reconstruction |
| `coalition`, `_decomposition.coalition_table` | Coalition evaluation and loss tables |
| `decomposition`, `_decomposition.robust`, `_decomposition.projection` | Dividends, robust aggregation and support allocation |
| `projection` | Public exports of the behavioral-support projection functions |
| `safety.geometry`, `safety.temporal`, `safety.proxies`, `safety._schema` | Fixed-future geometry and risk proxies |
| `safety.response` | Single/pair differences and weighted summaries |

The `_behavior` and `_decomposition` packages contain internal implementations;
their `__init__.py` files do not eagerly import submodules. Existing imports from
`tbr_hi.projection` remain available through explicit exports. Private module
paths are not part of the public API. Dataset-level G/H/P,
localization statistics, historical adjustment, mismatch queues and fixed-budget
comparisons belong to the empirical procedures described in the paper.
Their selected results are in the [result index](../results/README.md).
