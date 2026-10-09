# API reference

## Entry points

| Task | Import and call | Inputs |
| --- | --- | --- |
| Decompose existing losses | `from tbr_hi import decompose_loss_tables` | Ordered players, K complete loss-table rows, weights and lambda |
| Construct BRT players | `from tbr_hi.behavior import build_players` | `History` and optional behavior/relevance configuration |
| Construct baselines | `from tbr_hi.baselines import build_baseline_family` | Replacement history, earlier history and same-model environment callback |
| Evaluate model dependence | `from tbr_hi.coalition import compute_model_dependence` | History, players, family, target callback, true future and mask |
| Evaluate risk-proxy responses | `from tbr_hi.safety import compute_safety_responses` | The same history/players/family, target callback and fixed-future proxy |
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
| `robust_checks` | Numerical decomposition consistency summaries |

`compute_model_dependence` also returns `players`, `excluded_players`,
`losses_by_baseline`, `baseline_summary` and `target_valid_frame_count`.
The last count uses the selected minADE evaluation window. Exclude targets with
no valid future frame before evaluating the loss game.

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
| `config`, `behavior`, `_behavior_rules`, `_behavior_features` | Thresholds, kinematic evidence and primary labels |
| `relevance`, `players` | Physical relevance, tiers, grouping and coverage |
| `interfaces`, `baselines` | Contracts, matching, baselines and kinematic reconstruction |
| `coalition`, `_coalition_table` | Coalition evaluation and loss tables |
| `decomposition`, `_robust`, `projection` | Dividends, robust aggregation and support allocation |
| `safety.geometry`, `safety.temporal`, `safety.proxies`, `safety._schema` | Fixed-future geometry and risk proxies |
| `safety.response` | Single/pair differences and weighted summaries |

Modules beginning with `_` support the documented APIs. Dataset-level G/H/P,
localization statistics, historical adjustment, mismatch queues and fixed-budget
comparisons belong to the empirical procedures described in the paper.
Their selected results are in the [result index](../results/README.md).
