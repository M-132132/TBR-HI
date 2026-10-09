"""Behavior labels and BRT construction from true historical trajectories."""

import numpy as np

from ._behavior_features import _compute_interactions, _compute_track_metrics, _safe_acceleration_from_speed
from ._behavior_rules import classify_vehicle
from .config import AnalyzerConfig, BehaviorConfig, InteractionConfig
from .interfaces import History
from .players import group_players
from .relevance import compute_target_interactions


def label_behaviors(history: History, config=AnalyzerConfig()) -> dict[int, dict]:
    """
    功能：使用模型输入的速度、朝向和真实历史位置识别车辆行为。
    输入：
      - history (History)：真实历史，包含模型输入速度和朝向
      - config (AnalyzerConfig)：正式行为阈值，至少八帧有效历史，不要求这些帧连续
    输出：
      - (dict[int, dict])：车辆槽位到主行为、辅助标签、运动学及历史连续性指标
    """
    xy = history.xy.detach().cpu().numpy()
    valid = history.valid.detach().cpu().numpy().astype(bool)
    velocity = history.velocity.detach().cpu().numpy()
    heading = history.heading.detach().cpu().numpy()
    dt = float((history.timestamps[1] - history.timestamps[0]).item())
    vehicles = []
    for track in range(len(xy)):
        if not bool(history.vehicle_mask[track]) or valid[track].sum() < config.min_valid_frames:
            continue
        speed = np.linalg.norm(velocity[track], axis=-1)
        acceleration = _safe_acceleration_from_speed(speed, valid[track], dt)
        metrics = _compute_track_metrics(
            xy[track], heading[track], speed, acceleration, valid[track], dt, config.thresholds,
        )
        vehicles.append({'track': track, 't_len': xy.shape[1], 'valid': valid[track],
                         'pos_xy': xy[track], 'heading': heading[track],
                         'speed': speed, 'metrics': metrics})
    interactions = _compute_interactions(vehicles, config)
    return {vehicle['track']: {
        **classify_vehicle(vehicle['metrics'], interactions[index], config),
        'kinematics': vehicle['metrics'],
    } for index, vehicle in enumerate(vehicles)}


def build_players(history: History, behavior_config=AnalyzerConfig(), relevance_config=InteractionConfig()):
    """
    功能：从真实历史构造六类行为与三个物理层级组成的 BRT 玩家。
    输入：
      - history (History)：固定目标坐标系中的真实历史轨迹
      - behavior_config (AnalyzerConfig)：行为识别配置
      - relevance_config (InteractionConfig)：物理相关性配置
    输出：
      - (list[BRTPlayer])：不包含目标车的 BRT 玩家
    """
    labels = label_behaviors(history, behavior_config)
    families = BehaviorConfig().families
    behaviors = {}
    for track, result in labels.items():
        if track == history.target_index:
            continue
        for behavior, primary_labels in families.items():
            if result['primary_label'] in primary_labels:
                behaviors[track] = behavior
                break
    dt = float((history.timestamps[1] - history.timestamps[0]).item())
    relevance = compute_target_interactions(
        history.xy[None], history.valid[None], history.target_index,
        behaviors, relevance_config, dt,
    )
    return group_players(behaviors, {track: row.interaction_score for track, row in relevance.items()})
