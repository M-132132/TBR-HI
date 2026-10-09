"""基于真实车辆有向框计算目标条件安全间隙。"""

import torch
import torch.nn.functional as F

from ._schema import target_environment_valid_mask
from ._schema import FutureSceneBatch


def pairwise_center_distance(
    target_prediction_xy: torch.Tensor,
    environment_xy: torch.Tensor,
) -> torch.Tensor:
    """
    功能：计算目标预测模态与环境车辆未来轨迹的逐帧中心距离。
    输入：
      - target_prediction_xy (torch.Tensor)：形状为[B,K,T,2]的目标预测
      - environment_xy (torch.Tensor)：形状为[B,N,T,2]的环境真实未来
    输出：
      - (torch.Tensor)：形状为[B,K,N,T]的中心距离
    """
    displacement = (
        target_prediction_xy[:, :, None, :, :]
        - environment_xy[:, None, :, :, :]
    )
    return torch.linalg.vector_norm(displacement, dim=-1)


def trajectory_heading(
    trajectory_xy: torch.Tensor,
    initial_heading: float,
    time_step_s: float,
    stationary_speed_threshold_mps: float,
) -> torch.Tensor:
    """
    功能：使用轨迹切线估计预测车辆朝向，静止时延续上一朝向。
    输入：
      - trajectory_xy (torch.Tensor)：形状为[B,K,T,2]的目标轨迹
      - initial_heading (float)：目标局部坐标系中的初始朝向
    输出：
      - (torch.Tensor)：形状为[B,K,T]的预测朝向
    """
    batch_size, mode_count, time_count, _ = trajectory_xy.shape
    origin = torch.zeros(
        (batch_size, mode_count, 1, 2),
        device=trajectory_xy.device,
        dtype=trajectory_xy.dtype,
    )
    previous = torch.cat([origin, trajectory_xy[:, :, :-1, :]], dim=2)
    displacement = trajectory_xy - previous
    speed = torch.linalg.vector_norm(displacement, dim=-1) / float(
        time_step_s
    )
    raw_heading = torch.atan2(displacement[..., 1], displacement[..., 0])
    headings = []
    last_heading = torch.full(
        (batch_size, mode_count),
        float(initial_heading),
        device=trajectory_xy.device,
        dtype=trajectory_xy.dtype,
    )
    for time_index in range(time_count):
        current = torch.where(
            speed[:, :, time_index]
            > float(stationary_speed_threshold_mps),
            raw_heading[:, :, time_index],
            last_heading,
        )
        headings.append(current)
        last_heading = current
    return torch.stack(headings, dim=-1)


def oriented_box_corners(
    center_xy: torch.Tensor,
    heading: torch.Tensor,
    length: torch.Tensor,
    width: torch.Tensor,
) -> torch.Tensor:
    """
    功能：根据车辆中心、朝向和真实长宽构造四个有向框顶点。
    输入：
      - center_xy (torch.Tensor)：形状为[...,T,2]的车辆中心
      - heading (torch.Tensor)：形状为[...,T]的车辆朝向
      - length (torch.Tensor)：形状为[...]的车辆长度
      - width (torch.Tensor)：形状为[...]的车辆宽度
    输出：
      - (torch.Tensor)：形状为[...,T,4,2]的有向框顶点
    """
    half_length = length / 2.0
    half_width = width / 2.0
    while half_length.dim() < heading.dim():
        half_length = half_length.unsqueeze(-1)
        half_width = half_width.unsqueeze(-1)
    longitudinal = torch.stack(
        [torch.cos(heading), torch.sin(heading)],
        dim=-1,
    )
    lateral = torch.stack(
        [-torch.sin(heading), torch.cos(heading)],
        dim=-1,
    )
    signs = torch.tensor(
        [[1.0, 1.0], [1.0, -1.0], [-1.0, -1.0], [-1.0, 1.0]],
        device=center_xy.device,
        dtype=center_xy.dtype,
    )
    offsets = (
        half_length[..., None, None]
        * signs[:, 0, None]
        * longitudinal[..., None, :]
        + half_width[..., None, None]
        * signs[:, 1, None]
        * lateral[..., None, :]
    )
    return center_xy[..., None, :] + offsets


def point_to_polygon_edge_distance(
    points: torch.Tensor,
    polygon: torch.Tensor,
) -> torch.Tensor:
    """
    功能：计算一组点到另一矩形全部边的最小欧氏距离。
    输入：
      - points (torch.Tensor)：形状为[...,P,2]的点
      - polygon (torch.Tensor)：形状为[...,Q,2]的矩形顶点
    输出：
      - (torch.Tensor)：去除点和边维度后的最小距离
    """
    point = points[..., :, None, :]
    edge_start = polygon[..., None, :, :]
    edge_end = torch.roll(polygon, shifts=-1, dims=-2)[..., None, :, :]
    edge = edge_end - edge_start
    projection = (
        ((point - edge_start) * edge).sum(dim=-1)
        / (edge.square().sum(dim=-1) + 1e-12)
    ).clamp(0.0, 1.0)
    closest = edge_start + projection[..., None] * edge
    distance = torch.linalg.vector_norm(point - closest, dim=-1)
    return distance.amin(dim=(-2, -1))


def oriented_box_sat_margin(
    target_xy: torch.Tensor,
    target_heading: torch.Tensor,
    target_length: torch.Tensor,
    target_width: torch.Tensor,
    environment_xy: torch.Tensor,
    environment_heading: torch.Tensor,
    environment_length: torch.Tensor,
    environment_width: torch.Tensor,
) -> torch.Tensor:
    """
    功能：使用分离轴定理计算两组有向框的最大分离轴间隔。
    输入：
      - target_xy (torch.Tensor)：形状为[B,K,T,2]的目标中心
      - target_heading (torch.Tensor)：形状为[B,K,T]的目标朝向
      - target_length (torch.Tensor)：形状为[B]的目标长度
      - target_width (torch.Tensor)：形状为[B]的目标宽度
      - environment_xy (torch.Tensor)：形状为[B,N,T,2]的环境中心
      - environment_heading (torch.Tensor)：形状为[B,N,T]的环境朝向
      - environment_length (torch.Tensor)：形状为[B,N]的环境长度
      - environment_width (torch.Tensor)：形状为[B,N]的环境宽度
    输出：
      - (torch.Tensor)：形状为[B,K,N,T]的分离轴间隔
    """
    target_u = torch.stack(
        [torch.cos(target_heading), torch.sin(target_heading)],
        dim=-1,
    )
    target_v = torch.stack(
        [-torch.sin(target_heading), torch.cos(target_heading)],
        dim=-1,
    )
    environment_u = torch.stack(
        [torch.cos(environment_heading), torch.sin(environment_heading)],
        dim=-1,
    )
    environment_v = torch.stack(
        [-torch.sin(environment_heading), torch.cos(environment_heading)],
        dim=-1,
    )
    environment_count = int(environment_xy.shape[1])
    mode_count = int(target_xy.shape[1])
    axes = torch.stack(
        [
            target_u[:, :, None, :, :].expand(
                -1, -1, environment_count, -1, -1
            ),
            target_v[:, :, None, :, :].expand(
                -1, -1, environment_count, -1, -1
            ),
            environment_u[:, None, :, :, :].expand(
                -1, mode_count, -1, -1, -1
            ),
            environment_v[:, None, :, :, :].expand(
                -1, mode_count, -1, -1, -1
            ),
        ],
        dim=-2,
    )
    target_u_pair = target_u[:, :, None, :, None, :]
    target_v_pair = target_v[:, :, None, :, None, :]
    environment_u_pair = environment_u[:, None, :, :, None, :]
    environment_v_pair = environment_v[:, None, :, :, None, :]
    target_radius = (
        target_length[:, None, None, None, None]
        / 2.0
        * torch.abs((axes * target_u_pair).sum(dim=-1))
        + target_width[:, None, None, None, None]
        / 2.0
        * torch.abs((axes * target_v_pair).sum(dim=-1))
    )
    environment_radius = (
        environment_length[:, None, :, None, None]
        / 2.0
        * torch.abs((axes * environment_u_pair).sum(dim=-1))
        + environment_width[:, None, :, None, None]
        / 2.0
        * torch.abs((axes * environment_v_pair).sum(dim=-1))
    )
    displacement = (
        environment_xy[:, None, :, :, :]
        - target_xy[:, :, None, :, :]
    )
    projected_center_distance = torch.abs(
        (displacement[..., None, :] * axes).sum(dim=-1)
    )
    gaps = projected_center_distance - target_radius - environment_radius
    return gaps.amax(dim=-1)


def pairwise_oriented_box_clearance(
    target_prediction_xy: torch.Tensor,
    target_heading: torch.Tensor,
    future: FutureSceneBatch,
) -> torch.Tensor:
    """
    功能：计算目标预测有向框与环境真实有向框的逐帧有符号边界间隙。
    输入：
      - target_prediction_xy (torch.Tensor)：形状为[B,K,T,2]的目标预测
      - target_heading (torch.Tensor)：形状为[B,K,T]的目标预测朝向
      - future (FutureSceneBatch)：真实车辆尺寸、朝向和环境轨迹
    输出：
      - (torch.Tensor)：形状为[B,K,N,T]的有符号间隙
    """
    target_corners = oriented_box_corners(
        target_prediction_xy,
        target_heading,
        future.target_length,
        future.target_width,
    )
    environment_corners = oriented_box_corners(
        future.environment_xy,
        future.environment_heading,
        future.environment_length,
        future.environment_width,
    )
    target_pair = target_corners[:, :, None, :, :, :]
    environment_pair = environment_corners[:, None, :, :, :, :]
    target_to_environment = point_to_polygon_edge_distance(
        target_pair,
        environment_pair,
    )
    environment_to_target = point_to_polygon_edge_distance(
        environment_pair,
        target_pair,
    )
    boundary_distance = torch.minimum(
        target_to_environment,
        environment_to_target,
    )
    sat_margin = oriented_box_sat_margin(
        target_prediction_xy,
        target_heading,
        future.target_length,
        future.target_width,
        future.environment_xy,
        future.environment_heading,
        future.environment_length,
        future.environment_width,
    )
    return torch.where(sat_margin > 0.0, boundary_distance, sat_margin)


def minimum_clearance_by_agent(
    target_prediction_xy: torch.Tensor,
    future: FutureSceneBatch,
    target_heading: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    功能：计算每个预测模态相对每辆环境车的最小有向框间隙。
    输入：
      - target_prediction_xy (torch.Tensor)：形状为[B,K,T,2]的目标预测
      - future (FutureSceneBatch)：真实车辆几何和环境未来轨迹
      - target_heading (torch.Tensor)：形状为[B,K,T]的目标朝向
    输出：
      - (Tuple[torch.Tensor, torch.Tensor])：逐车间隙[B,K,N]和有效标记[B,N]
    """
    mode_count = int(target_prediction_xy.shape[1])
    clearance = pairwise_oriented_box_clearance(
        target_prediction_xy,
        target_heading,
        future,
    )
    valid = target_environment_valid_mask(future, mode_count)
    masked_clearance = clearance.masked_fill(~valid, torch.inf)
    per_agent = masked_clearance.amin(dim=-1)
    per_agent_valid = valid.any(dim=-1).any(dim=1)
    return per_agent, per_agent_valid


def minimum_clearance_by_agent_with_time(
    target_prediction_xy: torch.Tensor,
    future: FutureSceneBatch,
    target_heading: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    功能：计算逐环境车最小有向框间隙，并返回最小值对应的未来帧下标。
    输入：
      - target_prediction_xy (torch.Tensor)：形状为[B,K,T,2]的目标轨迹
      - future (FutureSceneBatch)：真实车辆几何和环境未来轨迹
      - target_heading (torch.Tensor)：形状为[B,K,T]的目标朝向
    输出：
      - (Tuple[torch.Tensor, torch.Tensor, torch.Tensor])：逐车间隙[B,K,N]、有效标记[B,N]和临界帧[B,K,N]
    """
    mode_count = int(target_prediction_xy.shape[1])
    clearance = pairwise_oriented_box_clearance(
        target_prediction_xy,
        target_heading,
        future,
    )
    valid = target_environment_valid_mask(future, mode_count)
    masked_clearance = clearance.masked_fill(~valid, torch.inf)
    per_agent = masked_clearance.amin(dim=-1)
    critical_time_index = masked_clearance.argmin(dim=-1)
    per_agent_valid = valid.any(dim=-1).any(dim=1)
    critical_time_index = critical_time_index.masked_fill(
        ~per_agent_valid[:, None, :],
        -1,
    )
    return per_agent, per_agent_valid, critical_time_index


def clearance_by_agent_over_time(
    target_prediction_xy: torch.Tensor,
    future: FutureSceneBatch,
    target_heading: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    功能：计算目标轨迹相对每辆环境车的逐帧有向框间距与有效掩码。
    输入：
      - target_prediction_xy (torch.Tensor)：形状为[B,1,T,2]的目标轨迹
      - future (FutureSceneBatch)：真实未来轨迹、车辆尺寸和朝向
      - target_heading (torch.Tensor)：形状为[B,1,T]的目标轨迹朝向
    输出：
      - (Tuple[torch.Tensor, torch.Tensor])：逐车逐帧间距[B,N,T]与有效掩码[B,N,T]
    """
    clearance = pairwise_oriented_box_clearance(
        target_prediction_xy,
        target_heading,
        future,
    )
    valid = target_environment_valid_mask(future, mode_count=1)
    return clearance[:, 0], valid[:, 0]


def minimum_scene_clearance(
    target_prediction_xy: torch.Tensor,
    future: FutureSceneBatch,
    target_heading: torch.Tensor,
) -> torch.Tensor:
    """
    功能：计算每个目标预测模态在全部环境车和未来帧上的最小有向框间隙。
    输入：
      - target_prediction_xy (torch.Tensor)：形状为[B,K,T,2]的目标预测
      - future (FutureSceneBatch)：真实车辆几何和环境未来轨迹
      - target_heading (torch.Tensor)：形状为[B,K,T]的目标朝向
    输出：
      - (torch.Tensor)：形状为[B,K]的场景最小间隙
    """
    per_agent, _ = minimum_clearance_by_agent(
        target_prediction_xy,
        future,
        target_heading=target_heading,
    )
    return per_agent.amin(dim=-1)


def clearance_risk_cost(
    minimum_clearance: torch.Tensor,
    safe_clearance: float,
    temperature: float,
) -> torch.Tensor:
    """
    功能：把有向框最小间隙转换为连续非负风险代价。
    输入：
      - minimum_clearance (torch.Tensor)：任意形状的最小间隙
      - safe_clearance (float)：安全间隙阈值
      - temperature (float)：风险响应平滑温度
    输出：
      - (torch.Tensor)：与输入同形状的连续风险代价
    """
    return F.softplus(
        (float(safe_clearance) - minimum_clearance) / float(temperature)
    )
