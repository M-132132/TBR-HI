"""Rule-based behavior labels computed from in-memory kinematic evidence."""

from typing import Dict, List
from ..config import AnalyzerConfig


def _dedup(labels: List[str]) -> List[str]:
    """
    功能：按原顺序去除重复标签。
    输入：
      - labels (List[str])：原始标签列表
    输出：
      - (List[str])：去重后的标签列表
    """
    seen = set()
    out = []
    for label in labels:
        if label not in seen:
            seen.add(label)
            out.append(label)
    return out


def _choose_primary_label(category_labels: Dict[str, List[str]]) -> str:
    """
    功能：从规则产生的标签中按固定优先级选择唯一主行为标签。
    输入：
      - category_labels (Dict[str, List[str]])：按类别组织的主标签候选和辅助标签
    输出：
      - (str)：用于分组的主标签；强制动、启停、受阻和让行不单独参与优先级
    """
    priority = [
        "parked",
        "lane_change_left",
        "lane_change_right",
        "overtake",
        "u_turn",
        "left_turn",
        "right_turn",
        "accelerate",
        "decelerate",
        "cruise_high",
        "cruise_low",
        "straight",
        "lane_keep",
    ]
    all_labels = []
    for labels in category_labels.values():
        all_labels.extend(labels)
    for name in priority:
        if name in all_labels:
            return name
    return "unknown"


def _is_stopped(metrics: Dict, th) -> bool:
    """
    功能：按全窗静止或末端停止两种规则确定静止主行为。
    输入：
      - metrics (Dict)：有效历史帧指标，end_speed_mps 对应最后有效帧
      - th (BehaviorThresholds)：行为判定阈值
    输出：
      - (bool)：True 表示静止优先，包括满足末端停止条件的减速后停止
    """
    mean_speed = metrics["mean_speed_mps"]
    max_speed = metrics["max_speed_mps"]
    displacement = metrics["displacement_m"]
    low_speed_ratio = metrics["low_speed_ratio"]
    moving_ratio = metrics["moving_ratio"]
    end_speed = metrics.get("end_speed_mps", mean_speed)
    parked_all_window = (
        mean_speed <= th.parked_mean_speed_max
        and max_speed <= th.parked_max_speed_max
        and displacement <= th.parked_displacement_max
    )
    stopped_now = (
        end_speed <= th.stop_speed_threshold
        and low_speed_ratio >= th.stopped_low_speed_ratio_min
        and moving_ratio <= th.stopped_moving_ratio_max
    )
    return bool(parked_all_window or stopped_now)


def _is_moving_enough(metrics: Dict, th) -> bool:
    """
    功能：判断车辆是否有足够运动量来判定转向、横向机动或纵向动作。
    输入：
      - metrics (Dict)：车辆运动学指标
      - th (BehaviorThresholds)：行为判定阈值
    输出：
      - (bool)：True 表示车辆运动量足够
    """
    return bool(
        metrics["displacement_m"] >= th.moving_displacement_min
        and metrics["moving_ratio"] >= th.moving_ratio_min
    )


def classify_vehicle(metrics: Dict, interaction: Dict, cfg: AnalyzerConfig) -> Dict:
    """
    功能：根据车辆运动学和交互特征生成主行为标签和辅助标签。
    输入：
      - metrics (Dict)：车辆运动学指标
      - interaction (Dict)：车辆与周围车辆的交互特征
      - cfg (AnalyzerConfig)：行为分析配置
    输出：
      - (Dict)：包含 categories、all_labels 和 primary_label 的标签结果
    """
    th = cfg.thresholds
    longitudinal: List[str] = []
    lateral: List[str] = []
    turn: List[str] = []
    interaction_labels: List[str] = []
    risk: List[str] = []

    mean_speed = metrics["mean_speed_mps"]
    max_speed = metrics["max_speed_mps"]
    displacement = metrics["displacement_m"]
    start_speed = metrics.get("start_speed_mps", mean_speed)
    end_speed = metrics.get("end_speed_mps", mean_speed)
    speed_delta = metrics["speed_delta_mps"]
    speed_std = metrics["speed_std_mps"]
    acc_p10 = metrics["acc_p10_mps2"]
    acc_p90 = metrics["acc_p90_mps2"]
    heading_delta_deg = metrics["heading_delta_deg"]
    lateral_shift = metrics["lateral_shift_m"]
    stop_go_transitions = metrics["stop_go_transitions"]
    low_speed_ratio = metrics["low_speed_ratio"]
    moving_ratio = metrics["moving_ratio"]

    stopped = _is_stopped(metrics, th)
    moving_enough = _is_moving_enough(metrics, th)

    if stopped:
        longitudinal.append("parked")
        if (
            start_speed >= th.moving_speed_threshold
            and end_speed <= th.stop_speed_threshold
            and speed_delta <= th.decel_speed_delta_max
        ):
            longitudinal.append("stopped_after_deceleration")
    else:
        stop_go = (
            stop_go_transitions >= th.stop_go_min_transitions
            and low_speed_ratio >= 0.2
            and moving_ratio >= 0.2
        )
        if stop_go:
            longitudinal.append("stop_go")

        decelerating = (
            moving_enough
            and speed_delta <= th.decel_speed_delta_max
            and acc_p10 <= th.decel_p10_max
        )
        accelerating = (
            moving_enough
            and speed_delta >= th.accel_speed_delta_min
            and acc_p90 >= th.accel_p90_min
        )

        if moving_enough and acc_p10 <= th.hard_brake_acc_min:
            longitudinal.append("hard_brake")

        if accelerating:
            longitudinal.append("accelerate")
        if decelerating:
            longitudinal.append("decelerate")

        if speed_std <= th.cruise_speed_std_max and "stop_go" not in longitudinal:
            if mean_speed >= th.cruise_high_speed_min:
                longitudinal.append("cruise_high")
            elif mean_speed >= th.cruise_low_speed_min:
                longitudinal.append("cruise_low")

    turn_allowed = (
        moving_enough
        and mean_speed >= th.turn_mean_speed_min
    )
    if (
        turn_allowed
        and abs(heading_delta_deg) >= th.u_turn_delta_deg_min
        and displacement >= th.u_turn_displacement_min
    ):
        turn.append("u_turn")
    elif turn_allowed and heading_delta_deg >= th.left_turn_delta_deg_min:
        turn.append("left_turn")
    elif turn_allowed and heading_delta_deg <= th.right_turn_delta_deg_max:
        turn.append("right_turn")
    else:
        turn.append("straight")

    lane_change = (
        moving_enough
        and
        abs(lateral_shift) >= th.lane_change_lateral_shift_min
        and abs(heading_delta_deg) <= th.lane_change_heading_delta_deg_max
        and displacement >= th.lane_change_displacement_min
    )
    if lane_change:
        if lateral_shift > 0:
            lateral.append("lane_change_left")
        else:
            lateral.append("lane_change_right")
    else:
        lateral.append("lane_keep")

    if interaction["following_ratio"] >= th.following_ratio_min:
        interaction_labels.append("following")
    if interaction["blocked_ratio"] >= th.blocked_ratio_min:
        interaction_labels.append("blocked")
    if (
        interaction["side_conflict_ratio"] >= th.yielding_side_ratio_min
        and ("decelerate" in longitudinal or "hard_brake" in longitudinal)
    ):
        interaction_labels.append("yielding")
    if interaction["overtake_events"] >= 1:
        interaction_labels.append("overtake")
        if moving_enough and not lane_change:
            lateral.append("overtake")
    if lane_change and interaction["min_distance_m"] <= th.cut_in_distance_max and interaction["side_conflict_ratio"] >= th.cut_in_side_ratio_min:
        interaction_labels.append("cut_in")

    if interaction["min_ttc_s"] <= th.ttc_low_threshold_s:
        risk.append("ttc_low")
    if interaction["near_conflict_frames"] >= th.near_conflict_min_frames:
        risk.append("near_conflict")

    category_labels = {
        "longitudinal": _dedup(longitudinal),
        "lateral": _dedup(lateral),
        "turn": _dedup(turn),
        "interaction": _dedup(interaction_labels),
        "risk": _dedup(risk),
    }

    all_labels = _dedup(
        category_labels["longitudinal"]
        + category_labels["lateral"]
        + category_labels["turn"]
        + category_labels["interaction"]
        + category_labels["risk"]
    )
    primary_label = _choose_primary_label(category_labels)
    return {
        "categories": category_labels,
        "all_labels": all_labels,
        "primary_label": primary_label,
    }
