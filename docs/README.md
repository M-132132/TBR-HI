# Documentation

## Start with the method

1. Read [method definitions](method.md) for BRT players, the conditional-trajectory
   loss game, robust Harsanyi decomposition and surrogate safety responses.
2. Read the [input contract](input_contract.md) for coordinate frames, trajectory
   masks, player membership, baseline coverage and caller responsibilities.
3. Use the [API reference](api.md) to select an interface and interpret its outputs.
4. Follow [model adapter guidance](model_adapters.md) to connect the same audited
   predictor to target and environment callbacks.

The API reference also covers [player construction configuration](api.md#player-construction-configuration),
[optional dividend details](api.md#optional-detail-rows) and the
[module map](api.md#module-map).

The [synthetic example](../examples/synthetic_demo.py) demonstrates the trajectory
interface on artificial inputs. [Reproduction scope](reproducibility.md) records
dependencies, the standalone environment and empirical table conventions.

## Read the paper results

The [result index](../results/README.md) organizes eight analysis topics:

- [Attribution quality](../results/02_attribution_quality/README.md) separates the
  Phi-based comparison, additional BO1 representation and original-loss validation.
- [Player size and candidate count](../results/04_localization_and_constructs/player_count_results.md)
  gives D12–D14 sensitivity and coverage.
- [Common analysis sets](../results/04_localization_and_constructs/common_analysis_sets.md)
  gives D15 matched component means and paired contrasts.
- [BO2 localization increments](../results/04_localization_and_constructs/bo2_increments.md)
  gives Figure 5 comparisons with candidate scopes and bootstrap counts.

Tables and figures are precomputed aggregates. Dataset preparation, model
training and the empirical analysis pipelines are supplied separately by the caller.
