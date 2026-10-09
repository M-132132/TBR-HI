# TBR-HI

**Target-conditioned Behavior–Relevance Harsanyi Interaction**

TBR-HI is a behavior-structured auditing framework for multi-agent trajectory
prediction. It decomposes model context dependence in a space of behavior–relevance–tier
(BRT) players and computes risk-proxy responses on the same entities.

The accompanying paper is *Safety-sensitive traffic context in multi-agent
trajectory prediction: A behavior-structured audit of model dependence*.

## Contents

- Behavior rules, target-conditioned physical relevance, and BRT player construction.
- Conditional-trajectory baseline families with entity matching and kinematic reconstruction.
- Exact minADE coalition games, Harsanyi dividends, and robust aggregation across baselines.
- Single-behavior dependence, two-behavior interactions, and higher-order joint behavior dependence.
- Spatial and temporal risk proxies and full-context risk-proxy response operators.
- A CPU example using artificial trajectories and an illustrative predictor.
- [Documentation](docs/README.md): method definitions, input contract, API and model adapters.
- [Empirical results](results/README.md): readable aggregate result tables and
  overview figures for eight analysis topics, including player-count sensitivity.

The package accepts in-memory trajectories and prediction callbacks. Dataset readers,
dataset preparation, model training, pretrained weights, benchmark runners, and
scene-level statistical-inference pipelines are outside this repository's scope.
The results directory supplies precomputed statistics as Markdown tables and
figures, including readable versions of paper and supplementary results as well
as extended analyses. The [result index](results/README.md) identifies their
correspondence. It contains no CSV exports or per-scene result files.

## Installation

Python 3.10 or newer, NumPy, and PyTorch are required. From this directory:

```bash
python -m pip install -e .
python examples/synthetic_demo.py
```

The example runs on a CPU and uses no dataset files or pretrained models. Its numbers
illustrate the API; they are not empirical results from the paper.

## Decompose an existing loss table

The table API uses only the Python standard library at import time:

```python
from tbr_hi import BRTPlayer, decompose_loss_tables

players = [
    BRTPlayer("a", "acceleration", "core_relevant", (1, 2), 0.6),
    BRTPlayer("b", "steady_motion", "candidate_context", (3,), 0.3),
]
# Columns follow bitmask order: empty, {a}, {b}, {a,b}.
# Each row contains minADE losses for one conditional-trajectory baseline.
result = decompose_loss_tables(
    players,
    losses_by_baseline=[[4.0, 3.0, 3.5, 1.5], [4.2, 3.0, 3.6, 1.5]],
    weights=[0.5, 0.5],
    robust_lambda=0.25,
)
print(result["D"])
print(result["behavior_order_two_pair_allocations"])
```

## Connect a trajectory predictor

1. Supply true histories as `History` objects in one fixed target coordinate frame.
2. Provide `predict_target(history) -> Prediction` and an environment prediction callback
   using the **same audited model** on the earlier true history.
3. Call `build_players` and `build_baseline_family`; retain `family.summary()`
   with requested/actual baseline counts and shared coverage.
4. Call `compute_model_dependence` with the target's true future and validity mask.
5. Call `compute_safety_responses` with a proxy that holds environment true futures fixed.

The full-context response calculation is a separate operation from loss-game
decomposition. Neither response strength nor dependence strength is an accident probability.

See [the API reference](docs/api.md), [the input contract](docs/input_contract.md), [method definitions](docs/method.md),
and [model adapter guidance](docs/model_adapters.md) for shapes, equations, and the
AutoBot, Wayformer, and EMP-M adaptations used in the paper.
The input contract specifies unique player IDs, disjoint vehicle groups, finite
numeric inputs, positive-sum nonnegative weights, and valid target evaluation
frames. Empty whole-player coverage means there are no auditable players.

See [reproduction scope and environments](docs/reproducibility.md) for the
standalone environment reference and the result-table conventions.

## Computational scope

For `n` common valid BRT players and `K` baseline members, exact loss-game evaluation
uses `K * 2**n` coalition losses. `compute_model_dependence` accepts an optional
`predict_many` callback for batched model inference. The Möbius inversion step
uses `O(K * n * 2**n)` arithmetic. The decomposition projects robust dividends
directly, skipping an unused complete value-table reconstruction by submask
enumeration that would require `O(3**n)` work.

For p cross-behavior player pairs, each call to `compute_safety_responses` uses
`1 + K * (n + p)` target predictions: one full-context prediction and the single
and pair replacements. Results describe the chosen model, baseline family, and
player space. Exact loss-game evaluation remains exponential in the player count.

## Citation

Please cite the accompanying TBR-HI paper when using this method. The software
version is available as `tbr_hi.__version__`.
