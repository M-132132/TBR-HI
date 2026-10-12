"""Public behavioral-support projection API."""

from ._decomposition.projection import (
    EPS,
    aggregate_behavior_support_order,
    behavior_support,
    compute_behavior_support_order,
    compute_mobius_dividends,
)

__all__ = [
    'EPS',
    'aggregate_behavior_support_order',
    'behavior_support',
    'compute_behavior_support_order',
    'compute_mobius_dividends',
]
