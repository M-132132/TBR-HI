# Method definitions

## BRT players

A BRT player is an environment-vehicle group defined by a behavior category and a
target-conditioned physical relevance tier. It may contain multiple vehicles.
Six categories are used: acceleration, deceleration, lateral maneuver, turning,
stable motion, and stationary. The code label `steady_motion` denotes stable motion.
Main-label precedence follows the supplied rules.
At least eight valid historical frames are required for behavior classification;
they need not form one continuous segment.

The primary-label priority is stationary, lateral maneuver, turning,
acceleration, deceleration, then stable motion. The default primary-label mapping is:

| Behavior category | Primary labels |
|---|---|
| Acceleration | `accelerate` |
| Deceleration | `decelerate` |
| Lateral maneuver | `lane_change_left`, `lane_change_right`, `overtake` |
| Turning | `left_turn`, `right_turn`, `u_turn` |
| Stable motion | `straight`, `cruise_low`, `cruise_high` |
| Stationary | `parked` |

`label_behaviors` also reports auxiliary labels such as `hard_brake`, `blocked`,
`yielding`, and `stop_go`. `build_players` reads only the selected `primary_label`;
these auxiliary labels do not by themselves assign a vehicle to deceleration.
The default behavior-family mapping contains the primary labels in the table.
Vehicles without a mapped primary label are not assigned to a BRT player.

Stationary has two rule branches. Whole-window stationary requires mean speed
at most 0.30 m/s, maximum speed at most 0.80 m/s and displacement at most 2 m.
Terminal stopping requires speed at the last valid frame at most 0.70 m/s,
a low-speed fraction of at least 0.50 and a moving fraction of at most 0.50.
The fractions use valid frames with speed below 0.70 m/s and above 2 m/s,
respectively. A vehicle that moved earlier and then stopped can therefore have
primary label `parked`. The auxiliary label `stopped_after_deceleration`
additionally requires initial speed at least 2 m/s, terminal speed at most
0.70 m/s and a speed decrease of at least 1.20 m/s. `parked` names a rule-based
motion category, not a parking location or an assertion that the vehicle stayed
still throughout the window.

Acceleration evidence uses speed differences within contiguous valid segments.
Net speed change, displacement and lateral displacement use the first and last
valid frames. Heading is unwrapped in the time-ordered valid-frame sequence;
heading change uses its endpoints, and stop/go transitions compare adjacent
states in that sequence. Path length connects adjacent valid positions and is
a descriptive metric. Path length, straightness and `duration_s` are not inputs
to the primary-label rules. `duration_s` is `(valid_frame_count - 1) * dt`;
`valid_time_span_s` uses the original first/last frame indices. The reported
segment and missing-frame fields describe historical coverage without changing
the behavior rules or excluding players.

Behavior interaction evidence is computed between eligible vehicles in each
vehicle's heading frame. Target-conditioned physical relevance is computed
separately against the designated target in the fixed target frame. The two
calculations supply the behavior and physical-tier dimensions of a BRT player.

The physical relevance score combines historical minimum distance, a TTCE/DCA term,
the lateral corridor, and radial closing speed with weights 0.30, 0.25, 0.20, and
0.25. Relative velocity is fitted over up to eight recent jointly valid historical
frames. Scores at least 0.40 define the core tier; scores from 0.25 to below 0.40
define the support tier; smaller scores define the background tier. The internal
labels are `core_relevant`, `candidate_context`, and `background_weak`.

`PlayerGroupingConfig` supplies those two BRT tier boundaries to `build_players`
and `group_players`. `InteractionConfig` supplies the scoring parameters; its
`threshold` only labels the separate relevant/weak diagnostic. `BehaviorConfig`
supplies the primary-label family mapping. All defaults reproduce the player
definitions above; custom mappings or boundaries define a different player space.

Player grouping records both mean and maximum member relevance. The retained
`physical_score` field and `mean_physical_score` property are means;
`max_physical_score` is the physical reference score for response localization.

## Conditional-trajectory loss game

Let \(\mathbb I\) be the common valid BRT player set and k index baseline members. The audited
model generates each conditional trajectory from an earlier true history ending
at the replacement-window anchor. For coalition S, players in S are restored to
their true histories; other active players use baseline k. Target history and
context outside the active players stay fixed.

For the minADE loss L, the value is

\[
v_k(S)=L_k(\varnothing)-L_k(S).
\]

The best target mode is selected separately in each coalition loss. The complete
coalition table is evaluated exactly. Möbius inversion gives

\[
d_k(T)=\sum_{S\subseteq T}(-1)^{|T|-|S|}v_k(S).
\]

For normalized baseline weights w, the implementation computes

\[
\mu_T=\sum_k w_k d_k(T),\qquad
\sigma_T=\sqrt{\sum_k w_k[d_k(T)-\mu_T]^2},
\]

\[
\widetilde d(T)=\operatorname{sign}(\mu_T)
\max(|\mu_T|-\lambda\sigma_T,0),\qquad \lambda=0.25.
\]

The weighted standard deviation is a population standard deviation. The signed
shrinkage remainder is the sum of `mu - robust_dividend` over nonempty coalitions;
it is reported separately from higher-order behavioral dependence.

The public decomposition projects the robust dividends directly onto behavioral
supports. It does not reconstruct a complete robust coalition value table that
would then be discarded. Member dividends, weighted means and standard deviations,
shrinkage, and projected outputs follow the same definitions above.

`include_details=False` omits per-coalition and per-member dividend tables while
retaining the projected quantities, shrinkage remainder and numerical summaries.
It changes output detail, not the loss game or decomposition definitions.

## Behavioral support projection

The support of T is the set of **distinct behavior categories** represented in T.
Its cardinality is the behavioral support order, independent of the vehicle count
and player count.

- For support order one, divide each robust dividend equally among its participating
  players. BO1 includes same-behavior interactions between several players.
- For support `{b,c}`, divide each robust dividend equally among the
  `|T intersect B_b| * |T intersect B_c|` participating cross-behavior player pairs.
- Retain support orders three and above as higher-order joint behavioral dependence.

The common-entity model dependence is `D_i = abs(BO1_i)`. BO1 is distinct from a
full-order Shapley allocation. Signed BO1, BO2, higher-order support contributions,
and the shrinkage remainder recover the baseline-averaged full-context loss improvement.

## Surrogate safety responses

Surrogate safety response calculation starts at the full ground-truth historical context.
Let `r_k(-A)` be a spatial or temporal risk proxy after replacing the histories
of players A with baseline k. All environment true future trajectories stay fixed.

For player i and a cross-behavior pair i,j:

\[
\Delta_{k,i}=r_k(-i)-r(\varnothing),
\]

\[
\Delta_{k,ij}=r_k(-\{i,j\})-r_k(-i)-r_k(-j)+r(\varnothing).
\]

Here `r(empty)` denotes no replacement, hence the complete true context. The signed
response is the weighted mean of these differences. Localization strength is

\[
R=\left|\sum_k w_k\Delta_k\right|.
\]

The absolute value is applied after averaging, preserving cancellation between
opposite signed responses across baseline members.

The response API also reports the weighted population variance from equation (19b):

\[
\sigma_\rho^2=\sum_k w_k(\Delta_k-\mu_\rho)^2,
\qquad \mu_\rho=\sum_k w_k\Delta_k.
\]

`variance` stores this value and `std` its square root. These describe baseline
member variation. They do not shrink R or represent scene-bootstrap uncertainty.

The spatial risk proxy uses the minimum signed oriented-box clearance across
environment vehicles and future frames, a softplus transformation with a 1 m
clearance threshold and 1 m scale, and the target model's mode probabilities.
Disjoint boxes use their Euclidean boundary distance; overlapping boxes use the
signed separation-axis margin. Predicted target heading follows trajectory
tangents, retaining the previous heading at zero speed.
When there is no jointly valid environment geometry for a target mode, its
minimum clearance is infinite and its spatial proxy contribution is zero.

The temporal proxy uses positive TTCE and corresponding DCE for approaching
relative motion at consecutive valid future samples. The score is
`exp(-TTCE / 4 s) * exp(-DCE / 4 m)`. It is maximized over environment vehicles
and future samples within each target mode, then averaged using the mode probabilities.
With no valid approaching sample, the temporal proxy contribution is zero.

Both supplied proxies consider all valid environment vehicles. The response is
indexed by the player whose **history is replaced**; the most critical vehicle
in the future proxy need not be a member of that player. Entity-matched G/H/P
measurements in the empirical results use their separately defined entity scope.

Model dependence and surrogate safety response share the model, BRT mapping, and
baseline family, while using different quantities and operations. They are not
statistically independent. Response strength measures sensitivity of the selected
safety-related outputs to historical context; it does not establish accident
probability or overall model safety.

## Method scope

The package supplies the calculations above. Dataset-level localization metrics,
comparisons against other explanation methods, G/H/P construct analyses, bootstrap
inference, historical-exposure adjustment, mismatch analyses, and fixed-budget
experiments are separate research procedures.
