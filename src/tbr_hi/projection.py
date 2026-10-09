"""Behavior-support-order decomposition for TBR-HI coalition games."""

import math
from typing import Dict, Sequence, Tuple

from .players import tier_family_from_tier
from .players import BRTPlayer as BRPlayer
from ._coalition_table import CoalitionValueTable


EPS = 1e-12


def _tier_rank(tier: str) -> int:
    """
    功能：返回物理相关性层级的稳定排序值。
    输入：
      - tier (str)：物理相关性层级
    输出：
      - (int)：层级排序值
    """
    ranks = {
        "relevant": 0,
        "core_relevant": 0,
        "candidate_context": 1,
        "weak": 2,
        "background_weak": 2,
    }
    return ranks.get(str(tier), 3)


def _player_sort_key(player: BRPlayer) -> Tuple:
    """
    功能：生成 BRT player 的稳定排序键。
    输入：
      - player (BRPlayer)：行为物理层级 player
    输出：
      - (Tuple)：behavior、tier 和 block ID 组成的排序键
    """
    return (
        str(player.behavior_id),
        _tier_rank(player.relevance_level),
        str(player.block_id),
    )


def _coalition_ids(mask: int, player_ids: Sequence[str]) -> Tuple[str, ...]:
    """
    功能：把 bitmask 转换为对应的 player ID coalition。
    输入：
      - mask (int)：联盟 bitmask
      - player_ids (Sequence[str])：bit 位顺序对应的 player ID
    输出：
      - (Tuple[str, ...])：mask 中包含的 player ID
    """
    return tuple(
        str(player_id)
        for index, player_id in enumerate(player_ids)
        if mask & (1 << index)
    )


def compute_mobius_dividends(
    value_table: CoalitionValueTable,
) -> Dict[int, float]:
    """
    功能：对完整 coalition value table 执行 fast Möbius transform。
    输入：
      - value_table (CoalitionValueTable)：包含全部 2^M 个联盟值的共享表
    输出：
      - (Dict[int, float])：联盟 bitmask 到 Harsanyi dividend 的映射
    """
    player_ids = list(value_table.player_ids)
    coalition_count = 1 << len(player_ids)
    dividends = [
        float(value_table.value(_coalition_ids(mask, player_ids)))
        for mask in range(coalition_count)
    ]
    for bit in range(len(player_ids)):
        for mask in range(coalition_count):
            if mask & (1 << bit):
                dividends[mask] -= dividends[mask ^ (1 << bit)]
    return {
        int(mask): float(value)
        for mask, value in enumerate(dividends)
    }


def behavior_support(mask: int, players: Sequence[BRPlayer]) -> Tuple[str, ...]:
    """
    功能：返回一个联盟中实际出现的不同行为集合。
    输入：
      - mask (int)：联盟 bitmask
      - players (Sequence[BRPlayer])：与 bit 位顺序一致的 BRT players
    输出：
      - (Tuple[str, ...])：排序去重后的 behavior ID
    """
    return tuple(
        sorted(
            {
                str(player.behavior_id)
                for index, player in enumerate(players)
                if mask & (1 << index)
            }
        )
    )


def _mobius_reconstruction_gap_max(
    value_table: CoalitionValueTable,
    dividends_by_mask: Dict[int, float],
) -> float:
    """
    功能：用 fast zeta transform 重建联盟值并返回最大绝对误差。
    输入：
      - value_table (CoalitionValueTable)：原始完整联盟价值表
      - dividends_by_mask (Dict[int, float])：Möbius dividends
    输出：
      - (float)：全部联盟上的最大重建误差
    """
    player_ids = list(value_table.player_ids)
    coalition_count = 1 << len(player_ids)
    reconstructed = [
        float(dividends_by_mask[mask])
        for mask in range(coalition_count)
    ]
    for bit in range(len(player_ids)):
        for mask in range(coalition_count):
            if mask & (1 << bit):
                reconstructed[mask] += reconstructed[mask ^ (1 << bit)]
    return max(
        abs(
            reconstructed[mask]
            - float(value_table.value(_coalition_ids(mask, player_ids)))
        )
        for mask in range(coalition_count)
    )


def _tier_pair_family(left_tier: str, right_tier: str) -> str:
    """
    功能：把两个物理层级转换为 FF、FB 或 BB pair 家族。
    输入：
      - left_tier (str)：左侧 player 的物理层级
      - right_tier (str)：右侧 player 的物理层级
    输出：
      - (str)：FF、FB 或 BB
    """
    left_family = tier_family_from_tier(left_tier)
    right_family = tier_family_from_tier(right_tier)
    if left_family == "foreground" and right_family == "foreground":
        return "FF"
    if left_family == "background" and right_family == "background":
        return "BB"
    return "FB"


def _allocation_type(value: float) -> str:
    """
    功能：根据 behavior-order-two 分配值生成符号标签。
    输入：
      - value (float)：behavior-order-two tier-pair 分配值
    输出：
      - (str)：positive、negative 或 near_zero
    """
    if float(value) > EPS:
        return "positive"
    if float(value) < -EPS:
        return "negative"
    return "near_zero"


def _cross_behavior_pairs(players: Sequence[BRPlayer]) -> Dict[Tuple[str, str], float]:
    """
    功能：初始化全部跨行为 BRT tier pair 的零值映射。
    输入：
      - players (Sequence[BRPlayer])：BRT players
    输出：
      - (Dict[Tuple[str, str], float])：规范 block pair 到零值的映射
    """
    ordered = sorted(players, key=_player_sort_key)
    pairs = {}
    for left_index, left in enumerate(ordered):
        for right in ordered[left_index + 1:]:
            if left.behavior_id != right.behavior_id:
                pairs[(left.block_id, right.block_id)] = 0.0
    return pairs


def aggregate_behavior_support_order(
    players: Sequence[BRPlayer],
    dividends_by_mask: Dict[int, float],
) -> Dict:
    """
    功能：按行为支持阶数把 dividends 聚合为 BO1、BO2 和高阶残差。
    输入：
      - players (Sequence[BRPlayer])：与 dividend bit 位顺序一致的 BRT players
      - dividends_by_mask (Dict[int, float])：联盟 bitmask 到 dividend 的映射
    输出：
      - (Dict)：BO1、BO2、行为支持效应、场景汇总和一致性检查
    """
    players_by_id = {
        player.block_id: player
        for player in players
    }
    behavior_order_one = {
        player.block_id: 0.0
        for player in players
    }
    behavior_order_two = _cross_behavior_pairs(players)
    support_values: Dict[Tuple[str, ...], float] = {}
    support_dividend_counts: Dict[Tuple[str, ...], int] = {}

    for mask in range(1, 1 << len(players)):
        dividend = float(dividends_by_mask[mask])
        coalition_indices = [
            index
            for index in range(len(players))
            if mask & (1 << index)
        ]
        support = behavior_support(mask, players)
        support_values[support] = support_values.get(support, 0.0) + dividend
        support_dividend_counts[support] = support_dividend_counts.get(support, 0) + 1

        if len(support) == 1:
            share = dividend / len(coalition_indices)
            for index in coalition_indices:
                behavior_order_one[players[index].block_id] += share
        elif len(support) == 2:
            left_behavior, right_behavior = support
            left_players = [
                players[index]
                for index in coalition_indices
                if players[index].behavior_id == left_behavior
            ]
            right_players = [
                players[index]
                for index in coalition_indices
                if players[index].behavior_id == right_behavior
            ]
            share = dividend / (len(left_players) * len(right_players))
            for left in left_players:
                for right in right_players:
                    behavior_order_two[(left.block_id, right.block_id)] += share

    ordered_players = sorted(players, key=_player_sort_key)
    behavior_abs_denominators = {}
    for player in ordered_players:
        behavior = str(player.behavior_id)
        behavior_abs_denominators[behavior] = (
            behavior_abs_denominators.get(behavior, 0.0)
            + abs(behavior_order_one[player.block_id])
        )

    order_one_rows = []
    for player in ordered_players:
        value = float(behavior_order_one[player.block_id])
        behavior_total = float(support_values.get((player.behavior_id,), 0.0))
        denominator = float(behavior_abs_denominators[player.behavior_id])
        attribution_share = 0.0 if denominator == 0.0 else abs(value) / denominator
        order_one_rows.append(
            {
                "block_id": player.block_id,
                "behavior_id": player.behavior_id,
                "physical_tier": player.relevance_level,
                "track_indices": list(player.track_indices),
                "vehicle_count": int(player.vehicle_count),
                "mean_physical_score": float(player.physical_score),
                "behavior_order_one_value": value,
                "abs_behavior_order_one_value": abs(value),
                "behavior_order_one_per_vehicle": float(value / player.vehicle_count),
                "abs_behavior_order_one_per_vehicle": float(abs(value) / player.vehicle_count),
                "behavior_total_value": behavior_total,
                "behavior_abs_attribution_share": float(attribution_share),
            }
        )

    order_two_rows = []
    for left_id, right_id in sorted(
        behavior_order_two,
        key=lambda pair: (
            _player_sort_key(players_by_id[pair[0]]),
            _player_sort_key(players_by_id[pair[1]]),
        ),
    ):
        left = players_by_id[left_id]
        right = players_by_id[right_id]
        value = float(behavior_order_two[(left_id, right_id)])
        vehicle_pair_count = int(left.vehicle_count) * int(right.vehicle_count)
        behavior_pair = tuple(sorted((left.behavior_id, right.behavior_id)))
        pair_total = float(support_values.get(behavior_pair, 0.0))
        physical_pair_score = math.sqrt(
            max(0.0, float(left.physical_score))
            * max(0.0, float(right.physical_score))
        )
        order_two_rows.append(
            {
                "left_block_id": left.block_id,
                "right_block_id": right.block_id,
                "left_behavior_id": left.behavior_id,
                "right_behavior_id": right.behavior_id,
                "left_physical_tier": left.relevance_level,
                "right_physical_tier": right.relevance_level,
                "left_vehicle_count": int(left.vehicle_count),
                "right_vehicle_count": int(right.vehicle_count),
                "left_physical_score": float(left.physical_score),
                "right_physical_score": float(right.physical_score),
                "tier_pair_family": _tier_pair_family(
                    left.relevance_level,
                    right.relevance_level,
                ),
                "pair_physical_score": float(physical_pair_score),
                "behavior_order_two_value": value,
                "abs_behavior_order_two_value": abs(value),
                "behavior_order_two_per_vehicle_pair": float(value / vehicle_pair_count),
                "abs_behavior_order_two_per_vehicle_pair": float(
                    abs(value) / vehicle_pair_count
                ),
                "allocation_type": _allocation_type(value),
                "behavior_pair_total_value": pair_total,
            }
        )

    support_rows = [
        {
            "support_behaviors": list(support),
            "behavior_order": int(len(support)),
            "support_value": float(support_values[support]),
            "abs_support_value": abs(float(support_values[support])),
            "dividend_count": int(support_dividend_counts[support]),
        }
        for support in sorted(support_values, key=lambda item: (len(item), item))
    ]

    order_one_signed_sum = sum(
        float(row["behavior_order_one_value"])
        for row in order_one_rows
    )
    order_two_signed_sum = sum(
        float(row["behavior_order_two_value"])
        for row in order_two_rows
    )
    higher_order_rows = [
        row
        for row in support_rows
        if int(row["behavior_order"]) >= 3
    ]
    higher_order_signed_residual = sum(
        float(row["support_value"])
        for row in higher_order_rows
    )
    total_response = float(
        sum(float(dividends_by_mask[mask]) for mask in range(1, 1 << len(players)))
    )

    behavior_gaps = []
    for behavior in sorted({player.behavior_id for player in players}):
        allocated = sum(
            float(behavior_order_one[player.block_id])
            for player in players
            if player.behavior_id == behavior
        )
        behavior_gaps.append(abs(allocated - support_values.get((behavior,), 0.0)))

    behavior_pair_gaps = []
    behaviors = sorted({player.behavior_id for player in players})
    for left_index, left_behavior in enumerate(behaviors):
        for right_behavior in behaviors[left_index + 1:]:
            allocated = sum(
                float(row["behavior_order_two_value"])
                for row in order_two_rows
                if row["left_behavior_id"] == left_behavior
                and row["right_behavior_id"] == right_behavior
            )
            behavior_pair_gaps.append(
                abs(
                    allocated
                    - support_values.get((left_behavior, right_behavior), 0.0)
                )
            )

    return {
        "behavior_order_one_effects": order_one_rows,
        "behavior_order_two_pair_allocations": order_two_rows,
        "behavior_support_effects": support_rows,
        "scene_order_summary": {
            "behavior_order_one_signed_sum": float(order_one_signed_sum),
            "behavior_order_one_absolute_mass": float(
                sum(row["abs_behavior_order_one_value"] for row in order_one_rows)
            ),
            "behavior_order_two_signed_sum": float(order_two_signed_sum),
            "behavior_order_two_absolute_mass": float(
                sum(row["abs_behavior_order_two_value"] for row in order_two_rows)
            ),
            "higher_order_signed_residual": float(higher_order_signed_residual),
            "abs_higher_order_signed_residual": abs(float(higher_order_signed_residual)),
            "higher_order_absolute_support_mass": float(
                sum(row["abs_support_value"] for row in higher_order_rows)
            ),
            "max_behavior_order": int(
                max((row["behavior_order"] for row in support_rows), default=0)
            ),
            "total_response": total_response,
        },
        "checks": {
            "behavior_order_one_consistency_gap_max": float(
                max(behavior_gaps, default=0.0)
            ),
            "behavior_order_two_consistency_gap_max": float(
                max(behavior_pair_gaps, default=0.0)
            ),
            "joint_conservation_gap": float(
                order_one_signed_sum
                + order_two_signed_sum
                + higher_order_signed_residual
                - total_response
            ),
            "player_count": int(len(players)),
            "behavior_count": int(len(behaviors)),
            "behavior_order_one_count": int(len(order_one_rows)),
            "behavior_order_two_pair_count": int(len(order_two_rows)),
            "behavior_support_count": int(len(support_rows)),
            "higher_order_support_count": int(len(higher_order_rows)),
        },
    }


def compute_behavior_support_order(
    players: Sequence[BRPlayer],
    value_table: CoalitionValueTable,
) -> Dict:
    """
    功能：从共享联盟价值表计算冻结的 behavior-support-order 分解。
    输入：
      - players (Sequence[BRPlayer])：场景中的 active BRT players
      - value_table (CoalitionValueTable)：包含全部联盟值的共享表
    输出：
      - (Dict)：BO1、BO2、行为支持效应、场景汇总和数值检查
    """
    players_by_id = {
        player.block_id: player
        for player in players
    }
    ordered_players = [
        players_by_id[player_id]
        for player_id in value_table.player_ids
    ]
    dividends_by_mask = compute_mobius_dividends(value_table)
    result = aggregate_behavior_support_order(
        players=ordered_players,
        dividends_by_mask=dividends_by_mask,
    )
    empty_value = float(value_table.value_by_key[value_table.empty_key])
    full_value = float(value_table.value_by_key[value_table.full_key])
    result["formula_version"] = "behavior_support_order_v1"
    result["scene_order_summary"].update(
        {
            "empty_value": empty_value,
            "full_value": full_value,
            "total_response": float(full_value - empty_value),
        }
    )
    result["checks"]["joint_conservation_gap"] = float(
        result["scene_order_summary"]["behavior_order_one_signed_sum"]
        + result["scene_order_summary"]["behavior_order_two_signed_sum"]
        + result["scene_order_summary"]["higher_order_signed_residual"]
        - (full_value - empty_value)
    )
    result["checks"]["mobius_reconstruction_gap_max"] = float(
        _mobius_reconstruction_gap_max(value_table, dividends_by_mask)
    )
    return result
