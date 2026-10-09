# Model adapters

TBR-HI separates the mathematical method from model loading, dataset readers, and
training frameworks. Users supply prediction callbacks around a loaded model.
The included illustrative predictor demonstrates the interface without requiring
any third-party model implementation.

## Target prediction

The adapter receives a `History` and combines it with fixed model context. It must:

1. Write positions, velocities, accelerations, headings, and validity masks into
   the existing vehicle slots.
2. Keep the target's true history, map context, slot identities, and other static
   inputs fixed across coalitions.
3. Recreate model-specific trajectory features affected by a changed history.
4. Return target trajectories and probabilities as `Prediction` in the fixed
   main-target coordinate frame.

For models returning the usual dictionary interface, the final conversion is:

```python
from tbr_hi.interfaces import Prediction

prediction = Prediction(
    output["predicted_trajectory"][0, :, :40, :2],
    output["predicted_probability"][0],
)
```

This conversion assumes batch size one and positions already expressed in the
main-target frame. It does not perform model input construction or coordinate conversion.
An optional `predict_many(histories)` callback enables batched coalition evaluation.
It returns predictions in the same order as the supplied histories. Set the loaded
model to evaluation mode before either callback is used. The method's
`torch.inference_mode()` context does not itself call `model.eval()`.

## Environment prediction for baselines

The baseline callback receives the earlier true history ending at the replacement
window's first frame. It predicts eligible environment vehicles using the same model
as the target callback. Re-centering each environment vehicle as a prediction target
and transforming its output into the common main-target frame are adapter operations.
The returned anchor is the vehicle's true position at the end of the earlier window.

The family builder handles per-vehicle probability ranking, shared identity/anchor
matching, rank-wise member assembly, and motion-feature reconstruction. It retains
up to six jointly available ranks with uniform family weights.
It records requested K, actual K and shared coverage through `family.summary()`.
The paper's main-setting analysis uses actual K=6. Reduced prefixes and empty
coverage keep their reported counts and are separate eligibility outcomes.
It checks finiteness over every forecast position exported by this callback.
Export the intended 20-step replacement horizon in the paper setting, including
when a model natively predicts 60 steps. This makes the baseline coverage check
refer to the actual replacement window.

## Model-specific settings used in the paper

| Setting | AutoBot | Wayformer | EMP-M |
|---|---|---|---|
| Earlier true history | 21 frames | 21 frames | 21 frames |
| Environment prediction path | 20-step adapted prediction | Native 60-step prediction, first 20 exported | Native 60-step prediction, first 20 exported |
| Baseline history | True initial anchor + 20 predicted positions | Same | Same |
| Environment coverage | At least 19 valid frames in the 20-frame replacement interval | Same | Same |
| Main target evaluation | First 40 future frames | First 40 future frames | First 40 future frames |
| Target modes / requested family members | 6 / 6 | 6 / 6 | 6 / 6 |

The 19-frame rule uses true trajectory availability in the replacement interval.
It does not allow the baseline model to condition on those later positions.
All predicted positions used for replacement must be finite.

The package provides a common callback contract rather than loading these model
implementations or checkpoints. Native input encodings, target selection, and
coordinate transformations must follow the corresponding model implementation.

## Synthetic example

`examples/synthetic_demo.py` defines a single `IllustrativePredictor` object. Its
`target` and `environment` methods call the same prediction rule with different
targets and output horizons. This makes the baseline-generation chronology and
same-model requirement explicit without introducing dataset or experiment code.
