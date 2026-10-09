"""Method parameters, independent of dataset and experiment configuration."""

from dataclasses import dataclass, field
from typing import Dict, Set, Tuple


@dataclass(frozen=True)
class BehaviorThresholds:
    # Kinematic thresholds
    parked_mean_speed_max: float = 0.30
    parked_max_speed_max: float = 0.80
    parked_displacement_max: float = 2.00
    stop_speed_threshold: float = 0.70
    moving_speed_threshold: float = 2.00
    stop_go_min_transitions: int = 2
    hard_brake_acc_min: float = -3.50
    accel_speed_delta_min: float = 1.20
    accel_p90_min: float = 1.00
    decel_speed_delta_max: float = -1.20
    decel_p10_max: float = -1.00
    cruise_speed_std_max: float = 1.00
    cruise_low_speed_min: float = 1.00
    cruise_high_speed_min: float = 8.00
    stopped_low_speed_ratio_min: float = 0.50
    stopped_moving_ratio_max: float = 0.50
    moving_displacement_min: float = 3.00
    moving_ratio_min: float = 0.30
    turn_mean_speed_min: float = 1.00

    # Turning / lane-change thresholds
    left_turn_delta_deg_min: float = 35.0
    right_turn_delta_deg_max: float = -35.0
    u_turn_delta_deg_min: float = 150.0
    u_turn_displacement_min: float = 8.0
    lane_change_lateral_shift_min: float = 2.8
    lane_change_heading_delta_deg_max: float = 20.0
    lane_change_displacement_min: float = 8.0

    # Interaction thresholds
    front_distance_window: float = 25.0
    front_lateral_window: float = 3.5
    following_ratio_min: float = 0.40
    following_speed_gap_max: float = 3.0
    blocked_front_distance_max: float = 12.0
    blocked_ego_speed_max: float = 2.0
    blocked_ratio_min: float = 0.30
    side_distance_window: float = 8.0
    side_lateral_window: float = 4.0
    side_longitudinal_window: float = 8.0
    yielding_side_ratio_min: float = 0.20
    cut_in_side_ratio_min: float = 0.20
    cut_in_distance_max: float = 5.0
    overtake_longitudinal_near_max: float = 30.0
    overtake_lateral_near_max: float = 4.0

    # Risk thresholds
    ttc_low_threshold_s: float = 3.0
    near_conflict_distance_max: float = 2.5
    near_conflict_min_frames: int = 1

    # Scene-level tags
    congested_ratio_min: float = 0.35
    congested_mean_speed_max: float = 3.0
    lanechange_ratio_min: float = 0.12
    turning_ratio_min: float = 0.25
    interaction_ratio_min: float = 0.35
    risk_ratio_min: float = 0.10


@dataclass(frozen=True)
class AnalyzerConfig:
    dt_default: float = 0.10
    min_valid_frames: int = 8
    allowed_object_types: Tuple[str, ...] = field(default_factory=lambda: ("VEHICLE",))
    thresholds: BehaviorThresholds = field(default_factory=BehaviorThresholds)
    processed_kinematic_source: str = "model_input_features"

def _default_behavior_families() -> Dict[str, Set[str]]:
    """
    功能：定义主行为标签到论文六类行为的映射。
    输入：
      - 无
    输出：
      - (Dict[str, Set[str]])：行为类别及其主标签集合
    """
    return {
        "acceleration": {"accelerate"},
        "deceleration": {"decelerate"},
        "lateral_maneuver": {"lane_change_left", "lane_change_right", "overtake"},
        "turning": {"left_turn", "right_turn", "u_turn"},
        "steady_motion": {"straight", "cruise_low", "cruise_high"},
        "stationary": {"parked"},
    }


@dataclass(frozen=True)
class BehaviorConfig:
    families: Dict[str, Set[str]] = field(default_factory=_default_behavior_families)
    unknown_family: str = "other"


@dataclass(frozen=True)
class InteractionConfig:
    threshold: float = 0.4
    sigma_distance: float = 20.0
    sigma_ttc: float = 4.0
    sigma_dca: float = 4.0
    sigma_lateral: float = 3.5
    sigma_closing_speed: float = 3.0
    distance_weight: float = 0.30
    ttc_weight: float = 0.25
    corridor_weight: float = 0.20
    approach_weight: float = 0.25
    min_closing_speed: float = 0.2
    min_relative_speed: float = 0.2
    velocity_fit_steps: int = 8
    default_dt: float = 0.1

    def normalized_weights(self) -> Dict[str, float]:
        """
        功能：计算四项物理相关性证据的归一化权重。
        输入：
          - 无
        输出：
          - (Dict[str, float])：距离、TTCE/DCA、横向走廊和接近速度的权重
        """
        raw = {
            "distance": max(0.0, float(self.distance_weight)),
            "ttc": max(0.0, float(self.ttc_weight)),
            "corridor": max(0.0, float(self.corridor_weight)),
            "approach": max(0.0, float(self.approach_weight)),
        }
        total = sum(raw.values())
        if total <= 0.0:
            return {key: 0.25 for key in raw}
        return {key: value / total for key, value in raw.items()}
