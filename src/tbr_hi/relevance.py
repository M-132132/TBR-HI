"""Target-conditioned interaction features computed from model input trajectories."""

import math
from dataclasses import asdict, dataclass
from typing import Dict, Iterable, Optional

import torch

from .config import InteractionConfig


@dataclass(frozen=True)
class TargetInteraction:
    track_index: int
    valid_overlap_steps: int
    velocity_fit_steps: int
    current_distance: float
    min_history_distance: float
    longitudinal_offset: float
    lateral_offset: float
    relative_velocity_x: float
    relative_velocity_y: float
    relative_speed: float
    closing_speed: float
    ttc: float
    distance_at_closest_approach: float
    distance_score: float
    ttc_score: float
    corridor_score: float
    approach_score: float
    interaction_score: float
    interaction_level: str

    def to_dict(self) -> Dict:
        """
        功能：将单车目标条件物理相关性结果转换为字典。
        输入：
          - 无
        输出：
          - (Dict)：物理特征和相关性评分
        """
        return asdict(self)


def _finite(value: float, default: float = 0.0) -> float:
    """
    功能：按来源实现把非有限的派生物理特征转换为约定值。
    输入：
      - value (float)：物理特征值
      - default (float)：非有限值的表示
    输出：
      - (float)：有限特征值
    """
    return float(value) if math.isfinite(float(value)) else float(default)


def _exp_decay(value: float, sigma: float) -> float:
    """
    功能：计算非负物理量的指数衰减分数。
    输入：
      - value (float)：物理量
      - sigma (float)：衰减尺度
    输出：
      - (float)：衰减分数
    """
    return float(math.exp(-max(0.0, float(value)) / max(float(sigma), 1e-6)))


def _valid_mask(
    obj_trajs: torch.Tensor,
    obj_trajs_mask: Optional[torch.Tensor],
    target_track_index: int,
    track_index: int,
) -> torch.Tensor:
    """
    功能：生成目标车与指定环境车的共同有效历史掩码。
    输入：
      - obj_trajs (torch.Tensor)：历史状态 [1,N,T,F]
      - obj_trajs_mask (torch.Tensor | None)：历史有效掩码 [1,N,T]
      - target_track_index (int)：目标车槽位
      - track_index (int)：环境车槽位
    输出：
      - (torch.Tensor)：共同有效掩码 [T]
    """
    num_steps = int(obj_trajs.shape[2])
    if obj_trajs_mask is None:
        return torch.ones((num_steps,), dtype=torch.bool, device=obj_trajs.device)
    return obj_trajs_mask[0, target_track_index].bool() & obj_trajs_mask[0, track_index].bool()


def _fit_relative_velocity(
    relative_xy: torch.Tensor,
    valid_indices: torch.Tensor,
    dt: float,
    max_steps: int,
) -> torch.Tensor:
    """
    功能：在最近共同有效历史位置上拟合恒定二维相对速度。
    输入：
      - relative_xy (torch.Tensor)：有效相对位置 [V,2]
      - valid_indices (torch.Tensor)：原时间轴有效帧索引 [V]
      - dt (float)：帧间隔秒数
      - max_steps (int)：最多使用的有效帧数
    输出：
      - (torch.Tensor)：拟合相对速度 [2]
    """
    count = min(int(relative_xy.shape[0]), max(2, int(max_steps)))
    if count < 2:
        return torch.zeros((2,), dtype=relative_xy.dtype, device=relative_xy.device)

    positions = relative_xy[-count:]
    times = valid_indices[-count:].to(dtype=relative_xy.dtype) * float(dt)
    centered_time = times - times.mean()
    denominator = torch.sum(centered_time * centered_time)
    if float(denominator.item()) <= 1e-12:
        return torch.zeros((2,), dtype=relative_xy.dtype, device=relative_xy.device)
    centered_positions = positions - positions.mean(dim=0, keepdim=True)
    return torch.sum(centered_time[:, None] * centered_positions, dim=0) / denominator


def _collision_geometry(
    current_relative_xy: torch.Tensor,
    relative_velocity: torch.Tensor,
    min_relative_speed: float,
    min_closing_speed: float,
) -> tuple:
    """
    功能：计算径向接近速度、最近接近时间和对应距离。
    输入：
      - current_relative_xy (torch.Tensor)：当前相对位置 [2]
      - relative_velocity (torch.Tensor)：拟合相对速度 [2]
      - min_relative_speed (float)：相对运动阈值
      - min_closing_speed (float)：径向接近速度阈值
    输出：
      - (tuple)：接近速度、TTCE、DCA 和相对速度大小
    """
    distance = float(torch.linalg.vector_norm(current_relative_xy).item())
    relative_speed_sq = float(torch.dot(relative_velocity, relative_velocity).item())
    relative_speed = math.sqrt(max(0.0, relative_speed_sq))
    if distance <= 1e-6 or relative_speed < float(min_relative_speed):
        return 0.0, 1e9, distance, relative_speed

    radial_dot = float(torch.dot(current_relative_xy, relative_velocity).item())
    closing_speed = max(0.0, -radial_dot / distance)
    if closing_speed < float(min_closing_speed) or radial_dot >= 0.0:
        return closing_speed, 1e9, distance, relative_speed

    ttc = max(0.0, -radial_dot / max(relative_speed_sq, 1e-12))
    closest_relative = current_relative_xy + float(ttc) * relative_velocity
    dca = float(torch.linalg.vector_norm(closest_relative).item())
    return closing_speed, ttc, dca, relative_speed


def compute_target_interactions(
    obj_trajs: torch.Tensor,
    obj_trajs_mask: Optional[torch.Tensor],
    target_track_index: int,
    candidate_tracks: Iterable[int],
    config: InteractionConfig,
    dt: Optional[float] = None,
) -> Dict[int, TargetInteraction]:
    """
    功能：计算环境车辆对目标车的历史物理相关性特征和加权分数。
    输入：
      - obj_trajs (torch.Tensor)：固定目标坐标系中的历史状态 [1,N,T,F]
      - obj_trajs_mask (torch.Tensor | None)：有效掩码 [1,N,T]
      - target_track_index (int)：目标車槽位
      - candidate_tracks (Iterable[int])：候选环境车辆槽位
      - config (InteractionConfig)：物理相关性参数
      - dt (float | None)：帧间隔，缺省使用配置
    输出：
      - (Dict[int, TargetInteraction])：逐车物理相关性
    """
    if obj_trajs.dim() != 4 or int(obj_trajs.shape[0]) != 1:
        raise ValueError(f"expected obj_trajs [1,N,T,F], got {tuple(obj_trajs.shape)}")
    if int(obj_trajs.shape[-1]) < 2:
        raise ValueError("obj_trajs must contain x/y positions in features 0:2")

    num_agents = int(obj_trajs.shape[1])
    target = int(target_track_index)
    if target < 0 or target >= num_agents:
        raise ValueError(f"target track index out of range: {target}")

    step_dt = max(float(config.default_dt if dt is None else dt), 1e-6)
    weights = config.normalized_weights()
    output: Dict[int, TargetInteraction] = {}

    for raw_index in candidate_tracks:
        track_index = int(raw_index)
        if track_index == target or track_index < 0 or track_index >= num_agents:
            continue

        overlap = _valid_mask(obj_trajs, obj_trajs_mask, target, track_index)
        valid_indices = torch.where(overlap)[0]
        if int(valid_indices.numel()) == 0:
            interaction = TargetInteraction(
                track_index=track_index,
                valid_overlap_steps=0,
                velocity_fit_steps=0,
                current_distance=1e9,
                min_history_distance=1e9,
                longitudinal_offset=0.0,
                lateral_offset=0.0,
                relative_velocity_x=0.0,
                relative_velocity_y=0.0,
                relative_speed=0.0,
                closing_speed=0.0,
                ttc=1e9,
                distance_at_closest_approach=1e9,
                distance_score=0.0,
                ttc_score=0.0,
                corridor_score=0.0,
                approach_score=0.0,
                interaction_score=0.0,
                interaction_level="weak",
            )
            output[track_index] = interaction
            continue

        target_xy = obj_trajs[0, target, valid_indices, 0:2]
        other_xy = obj_trajs[0, track_index, valid_indices, 0:2]
        relative_xy = other_xy - target_xy
        distances = torch.linalg.vector_norm(relative_xy, dim=-1)
        current_rel = relative_xy[-1]
        current_distance = float(distances[-1].item())
        min_distance = float(distances.min().item())

        relative_velocity = _fit_relative_velocity(
            relative_xy=relative_xy,
            valid_indices=valid_indices,
            dt=step_dt,
            max_steps=config.velocity_fit_steps,
        )
        closing_speed, ttc, dca, relative_speed = _collision_geometry(
            current_relative_xy=current_rel,
            relative_velocity=relative_velocity,
            min_relative_speed=config.min_relative_speed,
            min_closing_speed=config.min_closing_speed,
        )

        longitudinal = float(current_rel[0].item())
        lateral = float(current_rel[1].item())
        distance_score = _exp_decay(min_distance, config.sigma_distance)
        ttc_score = (
            _exp_decay(ttc, config.sigma_ttc) * _exp_decay(dca, config.sigma_dca)
            if ttc < 1e8
            else 0.0
        )
        corridor_score = _exp_decay(abs(lateral), config.sigma_lateral)
        approach_score = 1.0 - math.exp(
            -closing_speed / max(float(config.sigma_closing_speed), 1e-6)
        )
        score = (
            weights["distance"] * distance_score
            + weights["ttc"] * ttc_score
            + weights["corridor"] * corridor_score
            + weights["approach"] * approach_score
        )
        score = min(1.0, max(0.0, float(score)))

        output[track_index] = TargetInteraction(
            track_index=track_index,
            valid_overlap_steps=int(valid_indices.numel()),
            velocity_fit_steps=min(
                int(valid_indices.numel()),
                max(2, int(config.velocity_fit_steps)),
            ),
            current_distance=current_distance,
            min_history_distance=min_distance,
            longitudinal_offset=longitudinal,
            lateral_offset=lateral,
            relative_velocity_x=_finite(float(relative_velocity[0].item())),
            relative_velocity_y=_finite(float(relative_velocity[1].item())),
            relative_speed=_finite(relative_speed),
            closing_speed=closing_speed,
            ttc=float(ttc),
            distance_at_closest_approach=float(dca),
            distance_score=distance_score,
            ttc_score=ttc_score,
            corridor_score=corridor_score,
            approach_score=approach_score,
            interaction_score=score,
            interaction_level="relevant" if score >= float(config.threshold) else "weak",
        )

    return output
