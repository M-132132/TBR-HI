"""Exact loss-game decomposition with the server's robust Harsanyi calculation."""

from ._decomposition.coalition_table import CoalitionValueTable, coalition_key
from ._decomposition.robust import compute_robust_harsanyi
from ._decomposition.projection import aggregate_behavior_support_order


def decompose_loss_tables(
    players, losses_by_baseline, weights=None, robust_lambda=0.25,
    *, include_details=True,
):
    """
    功能：把逐基线完整 minADE 损失表转换为稳健 Harsanyi 和行为支持分解。
    输入：
      - players (Sequence[BRTPlayer])：ID 唯一、成员互不重叠的玩家，顺序对应 bit 位
      - losses_by_baseline (Sequence[Sequence[float]])：[K,2**N] 有限损失表，K 至少为 1
      - weights (Sequence[float] | None)：有限非负权重且总和为正，缺省为均匀权重
      - robust_lambda (float)：有限非负股利收缩强度，默认 0.25
      - include_details (bool)：是否返回逐联盟和逐基线股利明细，默认 True
    输出：
      - (dict)：BO1、BO2、高阶行为支持、收缩余量、D、检查摘要和可选股利明细
    """
    count = len(losses_by_baseline)
    weights = [1.0 / count] * count if weights is None else list(weights)
    ids = [p.block_id for p in players]
    keys = [coalition_key(ids[i] for i in range(len(ids)) if mask & (1 << i))
            for mask in range(1 << len(ids))]
    tracks = {}
    if include_details:
        tracks = {
            key: sorted(track for p in players if p.block_id in key for track in p.track_indices)
            for key in keys
        }
    tables = [CoalitionValueTable(
        ids, {key: float(losses[0] - losses[mask]) for mask, key in enumerate(keys)}, tracks,
    ) for losses in losses_by_baseline]
    robust = compute_robust_harsanyi(
        players, tables, [f'baseline_{k + 1}' for k in range(count)], weights, robust_lambda,
        reconstruct_table=False,
        include_details=include_details,
    )
    projection = aggregate_behavior_support_order(players, robust['robust_dividends_by_mask'])
    withheld = robust['shrinkage_remainder']
    projection['scene_order_summary']['shrinkage_remainder'] = withheld
    projection['scene_order_summary']['mean_full_context_loss_improvement'] = (
        projection['scene_order_summary']['total_response'] + withheld
    )
    result = {
        **projection,
        'baseline_member_count': count,
        'D': {row['block_id']: row['abs_behavior_order_one_value']
              for row in projection['behavior_order_one_effects']},
    }
    if include_details:
        result['robust_dividends'] = robust['robust_dividend_rows']
        result['member_dividends'] = robust['member_dividend_rows']
    result['robust_checks'] = robust['checks']
    return result
