# Reproduction scope and environments

## What the repository implements

| Component | Inputs | Output |
| --- | --- | --- |
| Loss-table decomposition | Complete finite loss tables and ordered BRT players | Robust dividends, behavioral-support allocations, and D |
| Trajectory audit | In-memory histories, a conditional-trajectory baseline family, and caller-supplied prediction callbacks | Loss-game dependence and full-context risk-proxy responses |
| Synthetic example | Artificial trajectories and the included illustrative predictor | A CPU demonstration of the method interface |
| Empirical result presentation | Precomputed formal aggregate statistics | Readable Markdown tables and two overview figures |

The empirical tables and figures present paper results. The synthetic example
demonstrates the API and has no empirical paper-result interpretation. Dataset
readers, model implementations, weights and experiment pipelines are supplied
separately by the caller. CSV exports, per-scene result files and result-generation
scripts are outside this repository's contents. The accompanying Supplementary
Data provides the formal source statistics for the submission analyses.

## Dependency requirements and environment reference

The package declares Python >= 3.10, NumPy >= 1.24 and PyTorch >= 2.0.
The recorded standalone core-check environment is:

| Component | Version |
| --- | --- |
| Operating system | Windows, 64 bit |
| Python | 3.10.10 |
| NumPy | 2.2.6 |
| PyTorch | 2.8.0+cpu |

These versions describe the standalone package environment. The three models'
paper experiments use their respective model environments. Minimum dependency
versions specify installation requirements; they do not document checks across
every version or hardware configuration.

## Commands

From the repository root, install the package and run its illustrative CPU example:

```bash
python -m pip install -e .
python examples/synthetic_demo.py
```

This example uses artificial trajectories. It does not run the benchmark models,
reproduce scene-bootstrap inference or regenerate the published result figures.

## Table and figure conventions

Result tables display precomputed estimates, metric-valid scene counts and source
confidence intervals. Values are rounded for reading. No additional precision or
uncertainty is inferred from archived display-precision results. Paired differences
use common valid scenes and must not be reconstructed from separately valid
marginal means. Analysis-specific candidate rules and BH families are described
in the [result definitions](../results/DATA_DICTIONARY.md).

The behavior figure shows occurrence shares and allocated BO1 mass shares. The
behavioral-support composition table instead uses pre-allocation mean absolute
dividend masses across BO1, BO2 and higher orders: its shares are ratios of means.
The retention figure shows scene-equal means, confidence intervals and metric-valid
scene counts under the aligned K=1 comparison. Stable and Lateral denote stable
motion and lateral maneuver. PNG and vector PDF views are included for both figures.

The [result index](../results/README.md) links all eight topics. Additional
[player-count/size sensitivity](../results/04_localization_and_constructs/player_count_results.md)
and [common-set comparisons](../results/04_localization_and_constructs/common_analysis_sets.md)
correspond to Supplementary Data D12–D15.
