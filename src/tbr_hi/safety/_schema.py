"""In-memory future trajectories and vehicle geometry."""

from dataclasses import dataclass
import torch


@dataclass(frozen=True)
class FutureSceneBatch:
    """目标车辆与环境车辆的未来轨迹和真实车辆几何。"""

    target_xy: torch.Tensor
    target_mask: torch.Tensor
    target_length: torch.Tensor
    target_width: torch.Tensor
    target_factual_heading: torch.Tensor
    target_geometry_mask: torch.Tensor
    environment_xy: torch.Tensor
    environment_mask: torch.Tensor
    environment_length: torch.Tensor
    environment_width: torch.Tensor
    environment_heading: torch.Tensor
    environment_geometry_mask: torch.Tensor
    target_track_index: torch.Tensor

def target_environment_valid_mask(
    future: FutureSceneBatch,
    mode_count: int,
) -> torch.Tensor:
    """
    功能：构造目标—环境车辆逐模态逐帧有效 mask，并排除目标自身。
    输入：
      - future (FutureSceneBatch)：未来轨迹和车辆几何
      - mode_count (int)：目标预测模态数量
    输出：
      - (torch.Tensor)：形状为[B,K,N,T]的有效车辆对 mask
    """
    batch_size, agent_count, time_count = future.environment_mask.shape
    target_mask = future.target_mask[:, None, None, :]
    environment_mask = future.environment_mask[:, None, :, :]
    target_geometry = future.target_geometry_mask[:, None, None, :]
    environment_geometry = future.environment_geometry_mask[:, None, :, :]
    valid = (
        target_mask
        & environment_mask
        & target_geometry
        & environment_geometry
    )

    agent_indices = torch.arange(
        agent_count,
        device=future.environment_mask.device,
    )[None, :]
    non_target = agent_indices != future.target_track_index[:, None]
    valid = valid & non_target[:, None, :, None]
    return valid.expand(batch_size, mode_count, agent_count, time_count)
