"""Conditional-trajectory baseline families without dataset or checkpoint I/O."""

from dataclasses import replace

import torch

from .interfaces import BaselineFamily, EnvironmentForecast, History, PredictEnvironment


def replace_tracks(history: History, baseline: History, tracks) -> History:
    """
    功能：把指定环境车辆的历史状态替换为基线，保留其他车辆和静态上下文。
    输入：
      - history (History)：真实历史
      - baseline (History)：对应基线成员
      - tracks (Iterable[int])：需要替换的环境车辆槽位
    输出：
      - (History)：替换后的独立张量副本
    """
    indices = list(tracks)
    fields = {}
    for name in ('xy', 'valid', 'velocity', 'heading', 'acceleration'):
        value = getattr(history, name).clone()
        value[indices] = getattr(baseline, name)[indices]
        fields[name] = value
    return replace(history, **fields)


def reconstruct_kinematics(xy: torch.Tensor, timestamps: torch.Tensor, initial_heading: torch.Tensor):
    """
    功能：按正式基线实现由锚点和预测位置重建速度、朝向及加速度。
    输入：
      - xy (torch.Tensor)：包含真实初始锚点的位置 [T,2]
      - timestamps (torch.Tensor)：完整时间轴 [T]
      - initial_heading (torch.Tensor)：真实锚点朝向标量
    输出：
      - (tuple)：速度 [T,2]、朝向 [T] 和加速度 [T,2]
    """
    dt = timestamps[1:] - timestamps[:-1]
    velocity = torch.zeros_like(xy)
    velocity[1:] = (xy[1:] - xy[:-1]) / dt[:, None]
    velocity[0] = velocity[1]
    speed = torch.linalg.vector_norm(velocity, dim=-1)
    raw_heading = torch.atan2(velocity[:, 1], velocity[:, 0])
    last_heading = initial_heading
    headings = []
    for index in range(len(xy)):
        last_heading = torch.where(speed[index] > 0, raw_heading[index], last_heading)
        headings.append(last_heading)
    acceleration = torch.zeros_like(velocity)
    acceleration[1:] = (velocity[1:] - velocity[:-1]) / dt[:, None]
    acceleration[0] = acceleration[1]
    return velocity, torch.stack(headings), acceleration


def match_forecasts(history: History, forecast: EnvironmentForecast, tolerance=0.25, min_valid_steps=19):
    """
    功能：用真实实体 ID 和锚点距离匹配预测车辆；无 ID 时使用距离贪心匹配。
    输入：
      - history (History)：待替换窗口，第一帧为锚点
      - forecast (EnvironmentForecast)：按车辆组织的模型预测和真实锚点
      - tolerance (float)：允许的锚点匹配距离，单位米
      - min_valid_steps (int)：锚点后真实历史的最少有效帧数
    输出：
      - (list[tuple[int,int]])：预测车辆序号和模型槽位的对应关系
    """
    candidates = [i for i in range(len(history.xy))
                  if i != history.target_index and bool(history.vehicle_mask[i])
                  and bool(history.valid[i, 0])
                  and int(history.valid[i, 1:].sum()) >= min_valid_steps]
    if history.object_ids is not None and forecast.object_ids is not None:
        slots = {history.object_ids[i]: i for i in candidates}
        matched = []
        used = set()
        for index, object_id in enumerate(forecast.object_ids):
            if object_id not in slots or slots[object_id] in used:
                continue
            slot = slots[object_id]
            if float(torch.linalg.vector_norm(forecast.anchors[index] - history.xy[slot, 0])) <= tolerance:
                matched.append((index, slot))
                used.add(slot)
        return sorted(matched, key=lambda item: item[1])
    pairs = [(float(torch.linalg.vector_norm(anchor - history.xy[slot, 0])), index, slot)
             for index, anchor in enumerate(forecast.anchors) for slot in candidates]
    pairs.sort(key=lambda item: item[0])
    matched, used_forecasts, used_slots = [], set(), set()
    for distance, index, slot in pairs:
        if distance > tolerance:
            break
        if index not in used_forecasts and slot not in used_slots:
            matched.append((index, slot))
            used_forecasts.add(index)
            used_slots.add(slot)
    return sorted(matched, key=lambda item: item[1])


def build_baseline_family(
    history: History, earlier_history: History, predict_environment: PredictEnvironment,
    member_count=6, match_tolerance=0.25, min_valid_steps=19,
) -> BaselineFamily:
    """
    功能：调用被审计模型的前窗预测接口，构造按车内概率排序组合的条件轨迹基线族。
    输入：
      - history (History)：真实替换窗口，正式设置为 21 帧
      - earlier_history (History)：截至替换窗口首帧的更早真实历史，正式设置为 21 帧
      - predict_environment (Callable)：只接收 earlier_history 的同模型环境车预测回调
      - member_count (int)：请求的基线成员数，默认 6；可用共有模态不足时按来源规则减少
      - match_tolerance (float)：锚点匹配距离，默认 0.25 米
      - min_valid_steps (int)：锚点后真实历史的有效帧阈值，默认 19
    输出：
      - (BaselineFamily)：统一权重、共享实体映射和共有覆盖的基线族；无匹配时返回
        一个未替换成员且 available_tracks 为空，表示没有可审计玩家；summary() 记录
        请求数、实际可用数与容器成员数，论文主分析要求实际可用数为 6
    """
    with torch.inference_mode():
        forecast = predict_environment(earlier_history)
    order = forecast.probability.argsort(dim=1, descending=True, stable=True)
    ranked = forecast.xy.gather(1, order[:, :, None, None].expand_as(forecast.xy))
    finite_top = torch.isfinite(ranked[:, 0]).all(dim=(-1, -2))
    valid_indices = torch.where(finite_top)[0]
    forecast = EnvironmentForecast(
        ranked[valid_indices], forecast.probability.gather(1, order)[valid_indices],
        forecast.anchors[valid_indices],
        None if forecast.object_ids is None else tuple(forecast.object_ids[int(i)] for i in valid_indices),
    )
    ranked = forecast.xy
    matches = match_forecasts(history, forecast, match_tolerance, min_valid_steps)
    usable = []
    counts = []
    for index, slot in matches:
        count = 0
        for trajectory in ranked[index]:
            if not bool(torch.isfinite(trajectory).all()):
                break
            count += 1
        if count:
            usable.append((index, slot))
            counts.append(count)
    count = min([member_count] + counts) if counts else 1
    histories = []
    steps = history.xy.shape[1] - 1
    for rank in range(count):
        fields = {name: getattr(history, name).clone()
                  for name in ('xy', 'valid', 'velocity', 'heading', 'acceleration')}
        for index, slot in usable:
            trajectory = torch.cat([history.xy[slot, :1], ranked[index, rank, :steps]], dim=0)
            velocity, heading, acceleration = reconstruct_kinematics(
                trajectory, history.timestamps, history.heading[slot, 0],
            )
            fields['xy'][slot] = trajectory
            fields['valid'][slot] = True
            fields['velocity'][slot] = velocity
            fields['heading'][slot] = heading
            fields['acceleration'][slot] = acceleration
        histories.append(replace(history, **fields))
    return BaselineFamily(tuple(histories), tuple([1.0 / count] * count),
                          tuple(f'rank_{i + 1}' for i in range(count)),
                          frozenset(slot for _, slot in usable), member_count)
