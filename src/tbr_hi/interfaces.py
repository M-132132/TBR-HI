"""Dataset-independent, in-memory inputs for a single target scene."""

from dataclasses import dataclass
from typing import Callable

import torch


@dataclass(frozen=True)
class History:
    """Vehicle states in one fixed target coordinate frame; see docs/input_contract.md."""

    xy: torch.Tensor                 # [N, T, 2], metres
    valid: torch.Tensor              # [N, T], bool
    velocity: torch.Tensor           # [N, T, 2], metres / second
    heading: torch.Tensor            # [N, T], radians
    acceleration: torch.Tensor       # [N, T, 2], metres / second squared
    timestamps: torch.Tensor         # [T], seconds
    target_index: int
    vehicle_mask: torch.Tensor       # [N], bool
    object_ids: tuple[str, ...] | None = None


@dataclass(frozen=True)
class Prediction:
    """Target predictions [M, F, 2] and nonnegative mode probabilities [M]."""

    xy: torch.Tensor
    probability: torch.Tensor


@dataclass(frozen=True)
class EnvironmentForecast:
    """Per-vehicle forecasts [E, M, F, 2], probabilities [E, M], and true anchors [E, 2]."""

    xy: torch.Tensor
    probability: torch.Tensor
    anchors: torch.Tensor
    object_ids: tuple[str, ...] | None = None


@dataclass(frozen=True)
class BaselineFamily:
    """Matched, kinematically reconstructed histories and shared coverage."""

    histories: tuple[History, ...]
    weights: tuple[float, ...]
    names: tuple[str, ...]
    available_tracks: frozenset[int]
    requested_member_count: int | None = None

    @property
    def member_count(self) -> int:
        """
        功能：返回容器保存的基线成员数，包括空覆盖时的占位成员。
        输入：
          - 无
        输出：
          - (int)：histories 的长度
        """
        return len(self.histories)

    @property
    def actual_member_count(self) -> int:
        """
        功能：返回具有共同环境车辆覆盖的实际可用成员数。
        输入：
          - 无
        输出：
          - (int)：有覆盖时为成员数，无覆盖时为零
        """
        return self.member_count if self.available_tracks else 0

    def summary(self) -> dict:
        """
        功能：记录请求成员数、实际成员数及共有车辆覆盖。
        输入：
          - 无
        输出：
          - (dict)：数量、权重和是否满足请求数量；手工族未指定请求时状态为 None
        """
        complete = (None if self.requested_member_count is None
                    else self.actual_member_count == self.requested_member_count)
        return {
            'requested_member_count': self.requested_member_count,
            'actual_member_count': self.actual_member_count,
            'member_count': self.member_count,
            'available_track_count': len(self.available_tracks),
            'has_requested_member_count': complete,
            'weights': self.weights,
        }


PredictTarget = Callable[[History], Prediction]
PredictEnvironment = Callable[[History], EnvironmentForecast]
