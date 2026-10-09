# Attribution quality

The tables show original-loss deletion, aligned-baseline deletion/retention and original-loss reconstruction. Retention uses 20%, 30% and 50% vehicle budgets.

## Interpretation

The main aligned comparison uses Phi and three comparison methods, following Supplementary S3b. BO1 is retained as an additional representation. The original statistical protocol corrects all 10 method pairs per model and metric; selecting a display does not define a new testing family. Higher deletion/retention values and lower reconstruction errors have different meanings. Main-text Table 2 entity-localization method-comparison results are outside this collection.

## Readable tables

[Open selected tables](tables.md). This page includes:

- Original-loss deletion: robust and raw BO1
- Aligned-baseline deletion and retention
- Original-loss reconstruction
- Paired RMSE reduction from adding BO2
- Additional representation and retention overview

Results are precomputed aggregate statistics displayed as Markdown tables and existing figures. This repository contains no CSV exports or per-scene result files.

See the [definitions](../DATA_DICTIONARY.md) for units, metric directions, cohort rules and inference conventions, and [coverage notes](../RELEASE_NOTES.md) for the result-selection scope.

## Additional reading

- [Paired method comparisons](method_comparisons.md): 90 contrasts among Phi and the three reference methods.
- [BO1 extension](additional_bo1.md): 15 aligned estimates, 60 remaining contrasts and the unchanged five-representation retention overview.

Both pages retain the original ten-test BH family for each model and metric.
