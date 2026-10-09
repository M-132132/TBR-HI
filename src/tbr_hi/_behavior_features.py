"""Trajectory-only features required by the behavior labeling rules."""

import math
from typing import Dict, List, Tuple
import numpy as np
from .config import AnalyzerConfig, BehaviorThresholds


def heading_unit(theta: float) -> Tuple[float, float]:
    """
    功能：计算朝向对应的纵向单位向量。
    输入：
      - theta (float)：朝向弧度
    输出：
      - (Tuple[float, float])：二维纵向单位向量
    """
    return math.cos(theta), math.sin(theta)


def lateral_unit(theta: float) -> Tuple[float, float]:
    """
    功能：计算朝向对应的左侧横向单位向量。
    输入：
      - theta (float)：朝向弧度
    输出：
      - (Tuple[float, float])：二维横向单位向量
    """
    return -math.sin(theta), math.cos(theta)

def _contiguous_segments(indices: np.ndarray) -> List[List[int]]:
    """
    功能：把有效帧下标切分为连续时间段。
    输入：
      - indices (np.ndarray)：升序帧下标
    输出：
      - (List[List[int]])：连续帧段列表
    """
    if indices.size == 0:
        return []
    segments: List[List[int]] = []
    start = int(indices[0])
    prev = int(indices[0])
    for idx in indices[1:]:
        idx = int(idx)
        if idx == prev + 1:
            prev = idx
            continue
        segments.append(list(range(start, prev + 1)))
        start = idx
        prev = idx
    segments.append(list(range(start, prev + 1)))
    return segments


def _safe_acceleration_from_speed(
    speed: np.ndarray,
    valid: np.ndarray,
    dt: float,
) -> np.ndarray:
    """
    功能：在连续有效历史段内由速度标量计算加速度证据。
    输入：
      - speed (np.ndarray)：速度标量序列，形状为 [T]
      - valid (np.ndarray)：有效帧掩码，形状为 [T]
      - dt (float)：帧间隔秒数
    输出：
      - (np.ndarray)：标量加速度序列，形状为 [T]
    """
    valid = np.asarray(valid, dtype=bool).reshape(speed.shape[0])
    acc = np.zeros(speed.shape[0], dtype=np.float64)
    for segment in _contiguous_segments(np.where(valid)[0]):
        if len(segment) <= 1:
            continue
        idx = np.asarray(segment, dtype=np.int64)
        acc[idx[1:]] = (speed[idx[1:]] - speed[idx[:-1]]) / max(dt, 1e-6)
        acc[idx[0]] = acc[idx[1]]
    return acc


def _compute_track_metrics(
    pos_xy: np.ndarray,
    heading: np.ndarray,
    speed: np.ndarray,
    acc: np.ndarray,
    valid: np.ndarray,
    dt: float,
    thresholds: BehaviorThresholds,
) -> Dict:
    """
    功能：计算正式行为指标，并报告有效历史段和内部缺口的描述性信息。
    输入：
      - pos_xy (np.ndarray)：位置 [T,2]
      - heading (np.ndarray)：模型输入朝向 [T]
      - speed (np.ndarray)：模型输入速度大小 [T]
      - acc (np.ndarray)：连续有效段内速度大小的差分 [T]
      - valid (np.ndarray)：有效历史掩码 [T]
      - dt (float)：帧间隔秒数
      - thresholds (BehaviorThresholds)：行为阈值
    输出：
      - (Dict)：运动学与历史覆盖指标；加速度分段差分，朝向及启停按有效帧序列计算
    """
    valid_idx = np.where(valid)[0]
    first = int(valid_idx[0])
    last = int(valid_idx[-1])
    valid_count = int(valid_idx.size)
    duration_s = float(max(0, valid_count - 1) * dt)
    segments = _contiguous_segments(valid_idx)

    pos_valid = pos_xy[valid_idx]
    speed_valid = speed[valid_idx]
    acc_valid = acc[valid_idx]
    heading_valid = np.unwrap(heading[valid_idx])

    step = pos_valid[1:] - pos_valid[:-1]
    path_length = float(np.linalg.norm(step, axis=1).sum()) if step.size else 0.0
    displacement_vec = pos_valid[-1] - pos_valid[0]
    displacement = float(np.linalg.norm(displacement_vec))
    straightness = float(displacement / max(path_length, 1e-6))
    heading_delta_rad = float(heading_valid[-1] - heading_valid[0]) if heading_valid.size >= 2 else 0.0
    heading_delta_deg = float(np.degrees(heading_delta_rad))

    heading0 = float(heading_valid[0]) if heading_valid.size > 0 else 0.0
    nx, ny = lateral_unit(heading0)
    lateral_shift = float(displacement_vec[0] * nx + displacement_vec[1] * ny)

    low_speed = speed_valid < thresholds.stop_speed_threshold
    stop_go_transitions = int(np.count_nonzero(low_speed[1:] != low_speed[:-1])) if low_speed.size >= 2 else 0

    return {
        "valid_frame_count": valid_count,
        "first_valid_frame": first,
        "last_valid_frame": last,
        "duration_s": duration_s,
        "valid_time_span_s": float((last - first) * dt),
        "valid_segment_count": len(segments),
        "longest_valid_segment_frames": max(len(segment) for segment in segments),
        "internal_missing_frame_count": last - first + 1 - valid_count,
        "missing_history_frame_count": int(valid.shape[0]) - valid_count,
        "last_history_frame_valid": bool(valid[-1]),
        "start_speed_mps": float(speed_valid[0]) if speed_valid.size else 0.0,
        "end_speed_mps": float(speed_valid[-1]) if speed_valid.size else 0.0,
        "mean_speed_mps": float(np.mean(speed_valid)),
        "max_speed_mps": float(np.max(speed_valid)),
        "p95_speed_mps": float(np.percentile(speed_valid, 95)),
        "speed_std_mps": float(np.std(speed_valid)),
        "speed_delta_mps": float(speed_valid[-1] - speed_valid[0]) if speed_valid.size >= 2 else 0.0,
        "acc_mean_mps2": float(np.mean(acc_valid)),
        "acc_min_mps2": float(np.min(acc_valid)),
        "acc_max_mps2": float(np.max(acc_valid)),
        "acc_p10_mps2": float(np.percentile(acc_valid, 10)),
        "acc_p90_mps2": float(np.percentile(acc_valid, 90)),
        "path_length_m": path_length,
        "displacement_m": displacement,
        "straightness": straightness,
        "heading_delta_deg": heading_delta_deg,
        "lateral_shift_m": lateral_shift,
        "stop_go_transitions": stop_go_transitions,
        "low_speed_ratio": float(
            np.mean(speed_valid < thresholds.stop_speed_threshold)
        ),
        "moving_ratio": float(
            np.mean(speed_valid > thresholds.moving_speed_threshold)
        ),
    }

def _compute_interactions(vehicles: List[Dict], cfg: AnalyzerConfig) -> Dict[int, Dict]:
    """
    功能：计算行为识别所需车辆间关系，供跟随、受阻和超车标签判定。
    输入：
      - vehicles (List[Dict])：有效车辆的历史数组和运动学指标
      - cfg (AnalyzerConfig)：行为阈值配置
    输出：
      - (Dict[int, Dict])：行为关系证据；目标车条件物理相关性由 relevance 模块分别计算
    """
    th = cfg.thresholds
    n = len(vehicles)
    outputs: Dict[int, Dict] = {}
    if n == 0:
        return outputs

    for i, ego in enumerate(vehicles):
        t_len = ego["t_len"]
        valid_i = ego["valid"]
        pos_i = ego["pos_xy"]
        heading_i = ego["heading"]
        speed_i = ego["speed"]
        valid_indices = np.where(valid_i)[0]

        min_distance = float("inf")
        min_ttc = float("inf")
        near_conflict_frames = 0
        low_ttc_frames = 0
        following_frames = 0
        blocked_frames = 0
        side_conflict_frames = 0

        # Pairwise relation logs for crude overtake detection.
        pair_sign_logs: Dict[int, List[float]] = {j: [] for j in range(n) if j != i}

        for t in valid_indices:
            ego_xy = pos_i[t]
            theta = float(heading_i[t])
            hx, hy = heading_unit(theta)
            nx, ny = lateral_unit(theta)

            frame_min_dist = float("inf")
            frame_front_found = False
            frame_front_close = False
            frame_following = False
            frame_side_conflict = False
            front_best_ttc = float("inf")

            for j, other in enumerate(vehicles):
                if j == i or t >= other["t_len"] or not other["valid"][t]:
                    continue

                other_xy = other["pos_xy"][t]
                rel_x = float(other_xy[0] - ego_xy[0])
                rel_y = float(other_xy[1] - ego_xy[1])
                dist = math.hypot(rel_x, rel_y)
                if dist < frame_min_dist:
                    frame_min_dist = dist
                if dist < min_distance:
                    min_distance = dist

                longi = rel_x * hx + rel_y * hy
                lati = abs(rel_x * nx + rel_y * ny)

                if abs(longi) <= th.overtake_longitudinal_near_max and lati <= th.overtake_lateral_near_max:
                    pair_sign_logs[j].append(longi)

                is_front = (
                    longi > 0.0
                    and lati <= th.front_lateral_window
                    and dist <= th.front_distance_window
                )
                if is_front:
                    frame_front_found = True
                    rel_speed = float(speed_i[t] - other["speed"][t])
                    if dist <= th.blocked_front_distance_max and speed_i[t] <= th.blocked_ego_speed_max:
                        frame_front_close = True
                    if abs(rel_speed) <= th.following_speed_gap_max:
                        frame_following = True
                    if rel_speed > 1e-3:
                        ttc = dist / rel_speed
                        if ttc < front_best_ttc:
                            front_best_ttc = ttc

                is_side = (
                    abs(longi) <= th.side_longitudinal_window
                    and lati <= th.side_lateral_window
                    and dist <= th.side_distance_window
                )
                if is_side:
                    frame_side_conflict = True

            if frame_min_dist <= th.near_conflict_distance_max:
                near_conflict_frames += 1
            if frame_front_found and frame_following:
                following_frames += 1
            if frame_front_found and frame_front_close:
                blocked_frames += 1
            if frame_side_conflict:
                side_conflict_frames += 1

            if front_best_ttc < min_ttc:
                min_ttc = front_best_ttc
            if front_best_ttc <= th.ttc_low_threshold_s:
                low_ttc_frames += 1

        overtake_events = 0
        for j, longs in pair_sign_logs.items():
            if not longs:
                continue
            arr = np.asarray(longs, dtype=np.float64)
            has_front = np.any(arr > 2.0)
            has_back = np.any(arr < -2.0)
            if not (has_front and has_back):
                continue
            if ego["metrics"]["mean_speed_mps"] > vehicles[j]["metrics"]["mean_speed_mps"] + 0.5:
                overtake_events += 1

        valid_count = max(int(valid_indices.size), 1)
        outputs[i] = {
            "min_distance_m": float(min_distance if np.isfinite(min_distance) else 1e9),
            "min_ttc_s": float(min_ttc if np.isfinite(min_ttc) else 1e9),
            "near_conflict_frames": int(near_conflict_frames),
            "low_ttc_frames": int(low_ttc_frames),
            "following_ratio": float(following_frames / valid_count),
            "blocked_ratio": float(blocked_frames / valid_count),
            "side_conflict_ratio": float(side_conflict_frames / valid_count),
            "overtake_events": int(overtake_events),
        }
    return outputs
