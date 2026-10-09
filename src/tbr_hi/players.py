"""Behavior × target-conditioned physical relevance players."""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class BRTPlayer:
    """One behavior-tier group containing one or more environment vehicles."""

    block_id: str
    behavior_id: str
    relevance_level: str
    track_indices: tuple[int, ...]
    physical_score: float = 0.0                 # Mean member score; retained API field.
    max_physical_score: float | None = None     # Maximum for physical-relevance ranking.

    @property
    def mean_physical_score(self) -> float:
        """
        功能：返回玩家成员车辆的平均物理相关性，保留 physical_score 的原有含义。
        输入：
          - 无
        输出：
          - (float)：成员平均分，不用于论文最大物理相关性对照排序
        """
        return self.physical_score

    @property
    def vehicle_count(self) -> int:
        """
        功能：返回该 BRT 玩家包含的环境车辆数。
        输入：
          - 无
        输出：
          - (int)：车辆数
        """
        return len(self.track_indices)


def player_track_map(players: Sequence[BRTPlayer]) -> dict[str, tuple[int, ...]]:
    """
    功能：生成 BRT 玩家到车辆槽位的映射。
    输入：
      - players (Sequence[BRTPlayer])：具有唯一 ID 的玩家序列
    输出：
      - (dict)：玩家 ID 对应的车辆槽位元组
    """
    return {player.block_id: player.track_indices for player in players}


def physical_tier_from_score(score: float, core_threshold=0.4, support_threshold=0.25) -> str:
    """
    功能：按论文阈值把目标条件物理相关性分数分为三个层级。
    输入：
      - score (float)：物理相关性分数
      - core_threshold (float)：核心层阈值
      - support_threshold (float)：支持层阈值
    输出：
      - (str)：core_relevant、candidate_context 或 background_weak
    """
    if score >= core_threshold:
        return 'core_relevant'
    if score >= support_threshold:
        return 'candidate_context'
    return 'background_weak'


def tier_family_from_tier(tier: str) -> str:
    """
    功能：将物理层级映射为前景或背景。
    输入：
      - tier (str)：物理相关性层级
    输出：
      - (str)：foreground、background 或 other
    """
    if tier in ('core_relevant', 'candidate_context'):
        return 'foreground'
    if tier == 'background_weak':
        return 'background'
    return 'other'


def group_players(behaviors: dict[int, str], physical_scores: dict[int, float]) -> list[BRTPlayer]:
    """
    功能：按行为类别和目标条件物理层级构造互不重叠的玩家。
    输入：
      - behaviors (dict[int, str])：环境车辆槽位到行为类别
      - physical_scores (dict[int, float])：相同槽位的物理相关性分数
    输出：
      - (list[BRTPlayer])：按行为和层级排序的玩家，分别保存成员平均分与最大分
    """
    buckets = {}
    for track, behavior in behaviors.items():
        tier = physical_tier_from_score(physical_scores[track])
        buckets.setdefault((behavior, tier), []).append(track)
    tier_order = {'core_relevant': 0, 'candidate_context': 1, 'background_weak': 2}
    players = []
    for behavior, tier in sorted(buckets, key=lambda key: (key[0], tier_order[key[1]])):
        tracks = tuple(sorted(buckets[(behavior, tier)]))
        players.append(BRTPlayer(
            f'{behavior}:{tier}', behavior, tier, tracks,
            sum(physical_scores[track] for track in tracks) / len(tracks),
            max(physical_scores[track] for track in tracks),
        ))
    return players


def covered_players(players: Sequence[BRTPlayer], available_tracks) -> tuple[list, list]:
    """
    功能：按完整玩家覆盖规则保留玩家，覆盖不足的玩家整体排除。
    输入：
      - players (Sequence[BRTPlayer])：BRT 玩家
      - available_tracks (Iterable[int])：所有基线成员共有的可替换车辆槽位
    输出：
      - (tuple[list, list])：保留玩家和排除玩家
    """
    available = set(available_tracks)
    retained = [p for p in players if set(p.track_indices) <= available]
    excluded = [p for p in players if not set(p.track_indices) <= available]
    return retained, excluded
