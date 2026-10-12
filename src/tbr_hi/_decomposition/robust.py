"""Robust Harsanyi aggregation over forecast baseline families."""

import math
from typing import Dict, List, Sequence, Tuple

from ..players import BRTPlayer as BRPlayer
from .coalition_table import CoalitionKey, CoalitionValueTable, coalition_key, coalition_key_text
from .projection import (
    behavior_support,
    compute_mobius_dividends,
)


def coalition_ids_from_mask(mask: int, player_ids: Sequence[str]) -> Tuple[str, ...]:
    """
    功能：把 bitmask 转换为 player ID coalition。
    输入：
      - mask (int)：coalition bitmask
      - player_ids (Sequence[str])：player ID 顺序
    输出：
      - (Tuple[str, ...])：coalition player ID 元组
    """
    return tuple(
        str(player_id)
        for index, player_id in enumerate(player_ids)
        if int(mask) & (1 << index)
    )


def canonical_coalition_key_from_mask(mask: int, player_ids: Sequence[str]) -> CoalitionKey:
    """
    功能：把 bitmask 转换成 CoalitionValueTable 使用的规范 coalition key。
    输入：
      - mask (int)：coalition bitmask
      - player_ids (Sequence[str])：player ID 顺序
    输出：
      - (CoalitionKey)：按 coalition_key 规范排序后的 player ID 元组
    """
    return coalition_key(coalition_ids_from_mask(mask, player_ids))


def robust_dividend_value(
    mean_value: float,
    sigma_value: float,
    robust_lambda: float,
) -> float:
    """
    功能：执行 baseline-family robust Harsanyi dividend 收缩。
    输入：
      - mean_value (float)：跨 baseline member 的 dividend 加权均值
      - sigma_value (float)：跨 baseline member 的 dividend 加权 population std
      - robust_lambda (float)：收缩强度
    输出：
      - (float)：robust dividend
    """
    mean_value = float(mean_value)
    sigma_value = float(sigma_value)
    if not math.isfinite(mean_value) or not math.isfinite(sigma_value):
        return float("nan")
    shrink = max(abs(mean_value) - float(robust_lambda) * float(sigma_value), 0.0)
    if mean_value > 0.0:
        return float(shrink)
    if mean_value < 0.0:
        return float(-shrink)
    return 0.0


def finite_number(value: float) -> bool:
    """
    功能：判断数值是否为有限浮点数。
    输入：
      - value (float)：待检查数值
    输出：
      - (bool)：不是 NaN/Inf 时返回 True
    """
    return math.isfinite(float(value))


def reconstruct_value_table_from_dividends(
    player_ids: Sequence[str],
    track_sets_by_key: Dict[CoalitionKey, List[int]],
    dividends_by_mask: Dict[int, float],
) -> CoalitionValueTable:
    """
    功能：用 Harsanyi dividends 通过 zeta transform 重建 coalition value table。
    输入：
      - player_ids (Sequence[str])：player ID 顺序
      - track_sets_by_key (Dict[CoalitionKey, List[int]])：coalition 对应 track 集合
      - dividends_by_mask (Dict[int, float])：bitmask 到 dividend 的映射
    输出：
      - (CoalitionValueTable)：由 dividends 重建的 value table
    """
    value_by_key = {}
    coalition_count = 1 << len(player_ids)
    for mask in range(coalition_count):
        value = 0.0
        submask = mask
        while True:
            value += float(dividends_by_mask.get(submask, 0.0))
            if submask == 0:
                break
            submask = (submask - 1) & mask
        key = canonical_coalition_key_from_mask(mask, player_ids)
        value_by_key[key] = float(value)
    return CoalitionValueTable(
        player_ids=list(player_ids),
        value_by_key=value_by_key,
        track_sets_by_key={
            key: list(track_sets_by_key[key])
            for key in value_by_key
        },
    )


def compute_robust_harsanyi(
    players: Sequence[BRPlayer],
    member_value_tables: Sequence[CoalitionValueTable],
    baseline_names: Sequence[str],
    baseline_weights: Sequence[float],
    robust_lambda: float,
    reconstruct_table: bool = True,
    *, include_details: bool = True,
) -> Dict:
    """
    功能：对基线族的每个 Harsanyi 股利做加权均值、方差和鲁棒收缩。
    输入：
      - players (Sequence[BRPlayer])：当前场景的有效 BRT 玩家
      - member_value_tables (Sequence[CoalitionValueTable])：逐基线成员的联盟值表
      - baseline_names (Sequence[str])：基线成员名称
      - baseline_weights (Sequence[float])：基线成员权重
      - robust_lambda (float)：鲁棒收缩强度
      - reconstruct_table (bool)：是否重建完整值表；行为支持分解不需要此表
      - include_details (bool)：是否构造逐联盟和逐基线明细，默认保留全部明细
    输出：
      - (Dict)：股利、收缩余量、检查摘要和可选明细及值表；不重建时值表为 None
    """
    player_ids = list(member_value_tables[0].player_ids)
    players_by_id = {
        player.block_id: player
        for player in players
    }
    ordered_players = [
        players_by_id[player_id]
        for player_id in player_ids
    ]
    weights = [float(weight) for weight in baseline_weights]
    total_weight = float(sum(weights))
    if total_weight == 0.0:
        weights = [1.0 for _ in weights]
        total_weight = float(sum(weights))
    weights = [float(weight) / total_weight for weight in weights]

    member_dividends = [
        compute_mobius_dividends(table)
        for table in member_value_tables
    ]
    coalition_count = 1 << len(player_ids)
    robust_dividends = {}
    robust_rows = []
    member_rows = []
    withheld_dividends = []
    checks = {
        "robust_lambda": float(robust_lambda),
        "baseline_member_count": int(len(member_value_tables)),
        "nonfinite_member_dividend_count": 0,
        "nonfinite_robust_dividend_count": 0,
        "finite_abs_withheld_dividend_count": 0,
        "zeroed_robust_dividend_count": 0,
        "finite_total_abs_withheld_dividend": 0.0,
        "total_abs_withheld_dividend": 0.0,
    }

    for member_index, dividends in enumerate(member_dividends):
        for mask in range(coalition_count):
            checks["nonfinite_member_dividend_count"] += int(
                not finite_number(dividends[mask])
            )
            if include_details:
                key = canonical_coalition_key_from_mask(mask, player_ids)
                member_rows.append(
                    {
                        "baseline_member_index": int(member_index),
                        "baseline_member_name": str(baseline_names[member_index]),
                        "baseline_member_weight": float(weights[member_index]),
                        "coalition_mask": int(mask),
                        "coalition_key": coalition_key_text(key),
                        "coalition_size": int(len(key)),
                        "harsanyi_dividend": float(dividends[mask]),
                    }
                )

    for mask in range(coalition_count):
        values = [
            float(dividends[mask])
            for dividends in member_dividends
        ]
        mean_value = float(
            sum(weight * value for weight, value in zip(weights, values))
        )
        if finite_number(mean_value) and all(finite_number(value) for value in values):
            variance = float(
                sum(
                    weight * (value - mean_value) ** 2
                    for weight, value in zip(weights, values)
                )
            )
            sigma_value = math.sqrt(max(0.0, variance))
        else:
            sigma_value = float("nan")
        robust_value = robust_dividend_value(
            mean_value=mean_value,
            sigma_value=sigma_value,
            robust_lambda=robust_lambda,
        )
        robust_dividends[int(mask)] = float(robust_value)
        withheld = float(mean_value - robust_value)
        abs_withheld = abs(withheld)
        withheld_dividends.append(withheld)
        checks["nonfinite_robust_dividend_count"] += int(
            not finite_number(mean_value)
            or not finite_number(sigma_value)
            or not finite_number(robust_value)
        )
        checks["finite_abs_withheld_dividend_count"] += int(finite_number(abs_withheld))
        checks["zeroed_robust_dividend_count"] += int(
            finite_number(mean_value) and finite_number(robust_value)
            and mean_value != 0.0 and robust_value == 0.0
        )
        if include_details:
            key = canonical_coalition_key_from_mask(mask, player_ids)
            robust_rows.append(
                {
                    "coalition_mask": int(mask),
                    "coalition_key": coalition_key_text(key),
                    "coalition_size": int(len(key)),
                    "behavior_support": coalition_key_text(
                        behavior_support(mask, ordered_players)
                    ),
                    "mean_dividend": float(mean_value),
                    "sigma_dividend": float(sigma_value),
                    "robust_dividend": float(robust_value),
                    "withheld_dividend": withheld,
                    "abs_withheld_dividend": abs_withheld,
                    "member_dividends": list(values),
                }
            )

    checks["finite_total_abs_withheld_dividend"] = float(
        sum(abs(value) for value in withheld_dividends if finite_number(abs(value)))
    )
    checks["total_abs_withheld_dividend"] = float(
        sum(abs(value) for value in withheld_dividends)
    )
    shrinkage_remainder = sum(withheld_dividends[1:])

    robust_table = None
    if reconstruct_table:
        robust_table = reconstruct_value_table_from_dividends(
            player_ids=player_ids,
            track_sets_by_key=member_value_tables[0].track_sets_by_key,
            dividends_by_mask=robust_dividends,
        )
    return {
        "robust_value_table": robust_table,
        "robust_dividends_by_mask": robust_dividends,
        "robust_dividend_rows": robust_rows,
        "member_dividend_rows": member_rows,
        "shrinkage_remainder": shrinkage_remainder,
        "checks": checks,
    }
