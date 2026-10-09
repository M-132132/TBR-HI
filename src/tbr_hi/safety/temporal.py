"""TTCE-DCE temporal proxy calculation."""

from typing import Dict
import torch
from ._schema import FutureSceneBatch


def temporal_ttce_dce_components(
    predicted_xy: torch.Tensor,
    future: FutureSceneBatch,
    time_step_s: float,
    sigma_t_s: float,
    sigma_d_m: float,
    denominator_epsilon: float = 1e-12,
) -> Dict[str, torch.Tensor]:
    """
    功能：计算逐模态、车辆和未来时刻的冻结 TTCE、DCE 与连续风险得分。
    输入：
      - predicted_xy (torch.Tensor)：目标预测位置[B,K,T,2]
      - future (FutureSceneBatch)：事实环境未来位置和有效掩码
      - time_step_s (float)：相邻未来帧间隔
      - sigma_t_s (float)：TTCE 指数衰减尺度
      - sigma_d_m (float)：DCE 指数衰减尺度
      - denominator_epsilon (float)：相对速度平方有效阈值
    输出：
      - (Dict[str, torch.Tensor])：relative_velocity、ttce、dce、score和valid
    """
    relative = future.environment_xy[:, None, :, :, :] - predicted_xy[
        :, :, None, :, :
    ]
    relative_velocity = torch.zeros_like(relative)
    relative_velocity[..., 1:, :] = (
        relative[..., 1:, :] - relative[..., :-1, :]
    ) / float(time_step_s)

    target_valid = future.target_mask[:, None, None, :]
    environment_valid = future.environment_mask[:, None, :, :]
    finite_position = torch.isfinite(relative).all(dim=-1)
    common = target_valid & environment_valid & finite_position
    consecutive = torch.zeros_like(common)
    consecutive[..., 1:] = common[..., 1:] & common[..., :-1]
    agent_indices = torch.arange(
        future.environment_mask.shape[1], device=predicted_xy.device
    )[None, :]
    non_target = agent_indices != future.target_track_index[:, None]
    consecutive = consecutive & non_target[:, None, :, None]

    speed_squared = relative_velocity.square().sum(dim=-1)
    radial_dot = (relative * relative_velocity).sum(dim=-1)
    denominator_valid = speed_squared > float(denominator_epsilon)
    safe_denominator = torch.where(
        denominator_valid, speed_squared, torch.ones_like(speed_squared)
    )
    ttce = -radial_dot / safe_denominator
    closest = relative + ttce[..., None] * relative_velocity
    dce = torch.linalg.vector_norm(closest, dim=-1)
    valid = (
        consecutive
        & denominator_valid
        & (radial_dot < 0.0)
        & (ttce > 0.0)
        & torch.isfinite(ttce)
        & torch.isfinite(dce)
    )
    score = torch.zeros_like(ttce)
    score[valid] = torch.exp(-ttce[valid] / float(sigma_t_s)) * torch.exp(
        -dce[valid] / float(sigma_d_m)
    )
    return {
        "relative_velocity": relative_velocity,
        "ttce": ttce,
        "dce": dce,
        "score": score,
        "valid": valid,
    }
