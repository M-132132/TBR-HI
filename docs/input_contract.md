# Input and output contract

## Coordinate frame and time

All positions, velocities, accelerations, forecasts, anchors, and future geometry
must use the same coordinate frame. For the supplied spatial proxy, the prediction
target is at `(0, 0)` with heading zero at the prediction origin. The x-axis is the
target's longitudinal direction and the y-axis points left. Units are metres,
seconds, and radians. Historical frames are regularly spaced.
Timestamps are finite and strictly increasing, with at least two frames and a
positive sampling interval. Tensor shapes and evaluation horizons agree across
the history, prediction, and true-future inputs.

The paper uses 21 historical frames at 10 Hz. An earlier 21-frame true history ends
at the first frame of the replacement window. The following 20 predicted positions,
together with that shared true anchor, form a baseline history of 21 frames. The
main loss and safety evaluation use the first 40 future frames (4 s).

## Caller responsibilities

The API assumes inputs meeting this contract. The dataclasses describe their
fields; they do not validate arrays or repair numerical inputs. Prepare these
inputs in the model adapter before calling the method.

| Input | Required convention |
|---|---|
| Player identities | Unique `block_id` values in a fixed player order |
| Player membership | Nonempty, disjoint groups of environment-vehicle slots; no target slot |
| Baseline family | At least one member; histories, weights, and names have the same length |
| Family weights | Finite, nonnegative, with a strictly positive sum |
| Shrinkage | Finite `robust_lambda >= 0`; the primary setting is 0.25 |
| Target mode probabilities | Finite, nonnegative, with a strictly positive sum |
| Target evaluation | At least one valid true-future frame in the minADE evaluation window |
| Numeric arrays | Finite values in used trajectories and finite padding in invalid entries |

Weights need not sum to one on input: both the loss decomposition and response
operators normalize them. Use the same weights for both operations. A negative
weight or negative shrinkage coefficient does not represent the stated method.

## `History`

| Field | Shape | Meaning |
|---|---|---|
| `xy` | `[N,T,2]` | Positions |
| `valid` | `[N,T]` | Boolean true-history validity |
| `velocity` | `[N,T,2]` | Model-input velocity channels |
| `heading` | `[N,T]` | Model-input heading in radians |
| `acceleration` | `[N,T,2]` | Model-input acceleration channels |
| `timestamps` | `[T]` | Scene time axis in seconds |
| `vehicle_mask` | `[N]` | Boolean indicator of vehicle slots |
| `target_index` | scalar | Target vehicle slot |
| `object_ids` | length N or `None` | Stable object identities |

Slots remain fixed throughout an audit. Exclude non-vehicle slots from BRT players.
Keep unused array entries finite (for example, zero padding) and mark them invalid.
`target_index` identifies an existing vehicle slot. Supplied object identities
uniquely identify the vehicle slots used for matching.
Callers provide the same native kinematic features used by their model for the true
history. Behavior labeling uses the supplied speed and heading; scalar acceleration
evidence is computed from speed differences within contiguous valid segments.

Behavior eligibility requires at least eight valid frames in total; continuity
is reported separately. `label_behaviors` includes `valid_segment_count`,
`longest_valid_segment_frames`, `internal_missing_frame_count`,
`missing_history_frame_count`, `last_history_frame_valid` and
`valid_time_span_s` in each vehicle's `kinematics`. Internal missing frames are
invalid slots between the first and last valid frames; total missing frames also
include invalid prefixes and suffixes. A last-valid-frame speed need not be the
speed at the prediction origin when the final history slot is invalid.
These coverage fields are descriptive and do not add a continuity filter.

The behavior protocol uses the first/last valid frames for net changes and the
time-ordered valid sequence for heading unwrapping and stop/go transitions.
Retain the original time axis and masks. Requiring a continuous eight-frame
segment, or changing how gap-spanning changes are computed, defines a different
behavior protocol and a different player space.

Static vehicle dimensions, categorical channels, target history, maps, and other
model context belong to the adapter's fixed context. Reconstruct any additional
model-specific channels affected by trajectory replacement in the adapter. In the
paper, baseline size/category channels are anchored to the first historical frame;
time encodings and timestamps retain the common window time axis.

## BRT players and manual baseline families

`build_players` groups vehicles by the selected primary behavior label and physical
relevance tier. Its groups have unique IDs and disjoint membership. When supplying
`BRTPlayer` objects directly, preserve these same properties. Several players may
share a behavior label, but a vehicle belongs to only one player. Keep the player
order identical in all bitmask tables and replacement dictionaries.

The default `BehaviorConfig` maps primary labels into the six paper categories.
Custom mappings use disjoint primary-label sets; unmapped labels are excluded.
`PlayerGroupingConfig` supplies `core_threshold` and `support_threshold`, with
`core_threshold >= support_threshold`. Defaults are 0.40 and 0.25. Scoring
parameters belong to `InteractionConfig`; its relevant/weak diagnostic threshold
does not set the BRT tiers. These optional construction arguments are described
in the [API reference](api.md#player-construction-configuration).

`physical_score` and `mean_physical_score` denote the member mean.
`max_physical_score` denotes the member maximum used for the paper's physical
reference ranking. `group_players` supplies both. When constructing players
manually, provide the maximum explicitly for that ranking; its default is None.

A manually supplied `BaselineFamily` uses the same slots, time axis, coordinate
frame, and tensor layout as the true `History`. Its `available_tracks` contains
only environment slots covered by **every** family member. Each member preserves
the target history and all fixed context. Names, weights, and histories describe
the same ordered members.

## Prediction callbacks

`predict_target(history)` returns `Prediction(xy, probability)`:

- `xy`: `[M,F,2]`, finite target future positions, with at least one mode and
  enough frames for the selected evaluation horizon.
- `probability`: `[M]`, finite, nonnegative mode probabilities with positive sum.

Use the audited model in evaluation mode with deterministic inference. Each input
replacement is forwarded again, including its mode probabilities. The package does
not choose the loss-minimizing mode from the full context and reuse it for other
coalitions: minADE reselects its mode for every coalition.
An optional `predict_many(histories)` returns exactly one `Prediction` for each
input, in the same order; its coalition `batch_size` is a positive integer.
Callbacks preserve their input tensors and fixed context across calls.

`predict_environment(earlier_history)` returns `EnvironmentForecast`:

- `xy`: `[E,M,F,2]`, with at least 20 future positions in the paper setting.
- `probability`: `[E,M]`, finite, nonnegative per-vehicle mode probabilities,
  with a positive sum in each row and at least one mode.
- `anchors`: `[E,2]`, true positions at the end of the earlier history.
- `object_ids`: length E, or `None` if stable identities are unavailable.

The callback uses the same audited model to forecast each eligible environment
vehicle as a target where needed. Its only history input is the earlier true history.
It must not read the later replacement window or the future evaluation targets.
Coordinate conversion into the fixed main-target frame is the adapter's responsibility.

Modes are ranked by each vehicle's own probability. Baseline member k combines
rank k across matched vehicles; it is not a sample from a joint probability model.
The default family has up to six members and uniform weights. Availability is reduced
to the common finite mode prefix. Identity matching also checks a 0.25 m anchor
tolerance; without identities, anchor-distance matching is greedy. Matching is shared
across all ranks. Histories must contain at least 19 valid frames after the anchor
for a vehicle to be eligible under the supplied paper setting.
The requested `member_count` is a positive integer.

`family.summary()` records `requested_member_count`, `actual_member_count`,
stored `member_count`, shared-track count and whether the actual count matches
the request. Main-setting analysis requires six actual members with uniform
weights and at least one retained whole player. Record the returned summary;
requesting six members does not turn a shorter common prefix into K=6.
Manual families can provide `requested_member_count`; its default is None.

The finite-mode check covers the entire forecast horizon exported by the callback.
A nonfinite top-ranked trajectory excludes that forecast vehicle; a nonfinite
later rank ends its usable prefix. These are coverage exclusions, not replacements
of missing coordinates with zero. In the paper adapters, the environment callback
exports the 20 positions used to form the baseline history.

Every replaced trajectory has its velocity, heading, and acceleration reconstructed
from anchor-plus-prediction positions. Its replacement mask is fully valid. All
vehicles in a BRT player must have baseline coverage; otherwise the entire player
is excluded and its vehicles remain at their true histories.

### Empty coverage

When no forecast vehicle can be matched, the family builder returns one unchanged
history with weight one and `available_tracks = frozenset()`. This preserves the
family container; it represents **no auditable players**.
Its stored `member_count` is 1 and `actual_member_count` is 0.

`compute_model_dependence` and `compute_safety_responses` apply whole-player coverage
and return `players` and `excluded_players`. An empty retained player list can
also arise when some vehicles have coverage but no complete player does. In this
case, `D` is empty and the response `single` and `pair` lists are empty. The
empty-player loss game has zero contribution by construction. Do not count it as
an empirical scene demonstrating zero dependence or zero response. Dataset-level
analysis must record this eligibility outcome separately.

## Loss table API

`losses_by_baseline[k][mask]` is the minADE loss for baseline k and the coalition
whose restored true-history players are the set bits in `mask`. Bit i always
refers to `players[i]`. For n players, each of K rows has exactly `2**n` finite
numeric losses and K is positive. Column zero restores no active player; column `2**n - 1`
restores all active players. Vehicles outside the active players remain fixed at
their true histories. Baseline weights are normalized inside the decomposition.

## Fixed true future context

`FutureContext` contains `xy [N,F,2]`, `valid [N,F]`, `heading [N,F]`,
`length [N]`, `width [N]`, `geometry_valid [N,F]`, and `target_index`.
Use vehicle slots only, or mark other slots invalid. The target index refers to
this future array. All future arrays remain fixed during history replacement.
The spatial proxy uses dimensions and geometry validity as well as position validity.
The temporal proxy uses consecutive valid positional samples. Tensors participating
in a calculation share device and floating-point dtype.

Position and geometry validity arrays are Boolean. Dimensions are finite and
positive for valid vehicle geometry. Coordinates and headings remain finite even
in invalid slots. The selected horizon has at least two frames for the temporal
proxy; `dt`, the spatial softplus scale, and the temporal decay scales are positive.

`min_ade` requires a nonempty target-future validity mask within its evaluation
window. It multiplies distances by that mask, so NaN padding does not become a
valid zero contribution. Provide finite padding and exclude targets with no valid
evaluation frame before calling the loss game.

If the spatial proxy has no jointly valid target/environment geometry in a mode,
that mode's minimum clearance is infinite and its proxy contribution is zero.
If no valid approaching relative-motion sample exists, the temporal contribution
is zero. These are the proxy definitions. They do not establish low traffic risk
when the necessary trajectory or geometry information is absent. Common-entity
empirical analyses apply their own validity conditions rather than filling missing
entity measurements with zero.

## Results

- `behavior_order_one_effects`: signed and absolute BO1 values per BRT player.
- `D`: absolute BO1 model dependence on common valid players.
- `behavior_order_two_pair_allocations`: BO2 allocations to cross-behavior player pairs.
- `behavior_support_effects`: contributions by distinct behavior support.
- `scene_order_summary`: BO1, BO2, higher-order dependence, and shrinkage remainder.
- `robust_dividends`: member mean, weighted population standard deviation, robust
  dividend, and withheld amount for each coalition.
- Response `single` and `pair`: signed weighted response, absolute weighted response,
  signed member responses, weighted population `variance` and its square-root `std`.
  `absolute` is the absolute value **after** averaging.
- `baseline_member_count`: input loss-table or replacement-value member count.
- High-level `baseline_summary`: requested/actual/stored counts, weights and shared coverage.
- Dependence `target_valid_frame_count`: valid frames in the selected minADE window.

### Loss summary keys

Both dependence entry points default to `include_details=True`. Setting it to
False omits `robust_dividends` and `member_dividends`, retaining D, allocations,
support contributions, scene summaries and both check dictionaries. The
trajectory entry point retains the loss tables and eligibility information.
Consumers that read the omitted keys use the default detailed mode.

In the decomposition output, `scene_order_summary["total_response"]` is a retained
software key for the **signed loss-game contribution**:

\[
\texttt{total_response}=\sum_{T\ne\varnothing}\widetilde d(T).
\]

Its unit is metres, inherited from minADE. It is not Rs or Rt. The signed
`shrinkage_remainder` is added to it to give
`mean_full_context_loss_improvement`, the weighted mean of
`L_k(empty) - L_k(full)`. A signed remainder can be negative; it is not an absolute
mass. Surrogate safety responses are returned separately by the response API.

For `response_from_replacements`, each baseline dictionary contains `()` for the
full context, `(i,)` for every retained player, and `(i,j)` with i < j for every
cross-behavior pair. Values are finite scalars. These indices refer to the same
ordered player list across all dictionaries.

High-level functions return retained and excluded players explicitly. Call the loss
and response calculations with the same original player set and baseline family to
keep the common-entity mapping identical.
