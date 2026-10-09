"""Exact coalition value tables."""

import itertools
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple
from .players import BRTPlayer as BRPlayer, player_track_map

CoalitionKey = Tuple[str, ...]


@dataclass(frozen=True)
class CoalitionValueTable:
    """BR player coalition 到模型 value 的共享缓存表。"""

    player_ids: List[str]
    value_by_key: Dict[CoalitionKey, float]
    track_sets_by_key: Dict[CoalitionKey, List[int]]

    @property
    def coalition_count(self) -> int:
        """
        功能：返回 coalition 数量。
        输入：
          - 无
        输出：
          - (int)：value table 中的 coalition 数量
        """
        return len(self.value_by_key)

    @property
    def empty_key(self) -> CoalitionKey:
        """
        功能：返回空 coalition key。
        输入：
          - 无
        输出：
          - (CoalitionKey)：空元组 key
        """
        return ()

    @property
    def full_key(self) -> CoalitionKey:
        """
        功能：返回包含所有 player 的 coalition key。
        输入：
          - 无
        输出：
          - (CoalitionKey)：全 player coalition key
        """
        return coalition_key(self.player_ids)

    def value(self, players: Iterable[str]) -> float:
        """
        功能：读取一个 player coalition 的 value。
        输入：
          - players (Iterable[str])：player ID 集合
        输出：
          - (float)：该 coalition 的 value
        """
        return float(self.value_by_key[coalition_key(players)])

    def to_dict(self) -> Dict:
        """
        功能：把 value table 元信息转换成字典。
        输入：
          - 无
        输出：
          - (Dict)：包含 player、coalition 和 value 的字典
        """
        return {
            "player_ids": list(self.player_ids),
            "coalition_count": int(self.coalition_count),
            "empty_value": float(self.value_by_key[self.empty_key]),
            "full_value": float(self.value_by_key[self.full_key]),
        }


def coalition_key(values: Iterable[str]) -> CoalitionKey:
    """
    功能：把 player ID 集合转换为稳定 coalition key。
    输入：
      - values (Iterable[str])：player ID 集合
    输出：
      - (CoalitionKey)：排序去重后的 key
    """
    return tuple(sorted({str(value) for value in values}))


def enumerate_coalitions(player_ids: Sequence[str]) -> List[CoalitionKey]:
    """
    功能：枚举全部 player coalition。
    输入：
      - player_ids (Sequence[str])：player ID 列表
    输出：
      - (List[CoalitionKey])：所有 coalition key
    """
    ids = [str(player_id) for player_id in player_ids]
    return [
        coalition_key(items)
        for size in range(len(ids) + 1)
        for items in itertools.combinations(ids, size)
    ]


def tracks_for_coalition(
    key: Iterable[str],
    block_to_tracks: Mapping[str, Sequence[int]],
    fixed_context_tracks: Iterable[int] = (),
) -> List[int]:
    """
    功能：把 BR player coalition 展开为车辆 track coalition。
    输入：
      - key (Iterable[str])：player ID coalition
      - block_to_tracks (Mapping[str, Sequence[int]])：block_id 到 track_indices 的映射
    输出：
      - (List[int])：排序去重后的车辆 track 下标
    """
    tracks = {int(track) for track in fixed_context_tracks}
    tracks.update(
        int(track)
        for block_id in key
        for track in block_to_tracks[str(block_id)]
    )
    return sorted(tracks)


def table_from_value_function(
    players: Sequence[BRPlayer],
    value_fn: Callable[[CoalitionKey], float],
) -> CoalitionValueTable:
    """
    功能：用纯 Python value 函数构造测试用 coalition value table。
    输入：
      - players (Sequence[BRPlayer])：BR player 列表
      - value_fn (Callable[[CoalitionKey], float])：输入 coalition key 输出 value 的函数
    输出：
      - (CoalitionValueTable)：测试用 value table
    """
    player_ids = [player.block_id for player in players]
    block_to_tracks = player_track_map(players)
    keys = enumerate_coalitions(player_ids)
    return CoalitionValueTable(
        player_ids=list(player_ids),
        value_by_key={
            key: float(value_fn(key))
            for key in keys
        },
        track_sets_by_key={
            key: tracks_for_coalition(key, block_to_tracks)
            for key in keys
        },
    )

def coalition_key_text(key: Iterable[str]) -> str:
    """
    功能：把 coalition key 转换成可读字符串。
    输入：
      - key (Iterable[str])：player ID coalition
    输出：
      - (str)：分号连接的 coalition ID 字符串
    """
    return ";".join(str(item) for item in key)
