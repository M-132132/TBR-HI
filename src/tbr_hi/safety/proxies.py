"""Spatial and temporal proxy values against fixed true future trajectories."""

from dataclasses import dataclass

import torch

from ._schema import FutureSceneBatch
from .geometry import clearance_risk_cost, minimum_scene_clearance, trajectory_heading
from .temporal import temporal_ttce_dce_components


@dataclass(frozen=True)
class FutureContext:
    """True future states [N,F,...], fixed across every history replacement."""

    xy: torch.Tensor
    valid: torch.Tensor
    heading: torch.Tensor
    length: torch.Tensor
    width: torch.Tensor
    geometry_valid: torch.Tensor
    target_index: int


def as_future_batch(context: FutureContext, steps=40) -> FutureSceneBatch:
    """
    功能：把内存中的真实未来轨迹和车辆几何打包为安全计算张量。
    输入：
      - context (FutureContext)：固定的真实未来位置、朝向、长宽及掩码
      - steps (int)：评价未来帧数
    输出：
      - (FutureSceneBatch)：批大小为 1 的安全计算输入
    """
    i = context.target_index
    return FutureSceneBatch(
        target_xy=context.xy[i:i + 1, :steps], target_mask=context.valid[i:i + 1, :steps],
        target_length=context.length[i:i + 1], target_width=context.width[i:i + 1],
        target_factual_heading=context.heading[i:i + 1, :steps],
        target_geometry_mask=context.geometry_valid[i:i + 1, :steps],
        environment_xy=context.xy[None, :, :steps], environment_mask=context.valid[None, :, :steps],
        environment_length=context.length[None], environment_width=context.width[None],
        environment_heading=context.heading[None, :, :steps],
        environment_geometry_mask=context.geometry_valid[None, :, :steps],
        target_track_index=torch.tensor([i], device=context.xy.device),
    )


def spatial_proxy(prediction, context, steps=40, dt=0.1, safe_clearance=1.0, temperature=1.0):
    """
    功能：计算目标预测相对固定环境真实未来的模态概率期望空间风险代理。
    输入：
      - prediction (Prediction)：目标车多模态预测
      - context (FutureContext)：固定真实未来和车辆几何
      - steps (int)：评价未来帧数
      - dt (float)：帧间隔秒数
      - safe_clearance (float)：softplus 间隙阈值，单位米
      - temperature (float)：softplus 尺度，单位米
    输出：
      - (torch.Tensor)：标量空间风险代理
    """
    xy = prediction.xy[None, :, :steps]
    heading = trajectory_heading(xy, initial_heading=0.0, time_step_s=dt,
                                 stationary_speed_threshold_mps=0.0)
    clearance = minimum_scene_clearance(xy, as_future_batch(context, steps), heading)[0]
    probability = prediction.probability / prediction.probability.sum()
    return (probability * clearance_risk_cost(clearance, safe_clearance, temperature)).sum()


def temporal_proxy(prediction, context, steps=40, dt=0.1, sigma_t=4.0, sigma_d=4.0):
    """
    功能：计算目标预测相对固定环境真实未来的模态概率期望时间风险代理。
    输入：
      - prediction (Prediction)：目标车多模态预测
      - context (FutureContext)：固定真实未来轨迹
      - steps (int)：评价未来帧数
      - dt (float)：帧间隔秒数
      - sigma_t (float)：TTCE 指数衰减时间尺度，单位秒
      - sigma_d (float)：DCE 指数衰减距离尺度，单位米
    输出：
      - (torch.Tensor)：标量时间风险代理
    """
    components = temporal_ttce_dce_components(
        prediction.xy[None, :, :steps], as_future_batch(context, steps), dt, sigma_t, sigma_d,
    )
    mode_risk = components['score'][0].amax(dim=(-1, -2))
    probability = prediction.probability / prediction.probability.sum()
    return (probability * mode_risk).sum()
