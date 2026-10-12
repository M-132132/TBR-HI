"""Full-context first- and second-order surrogate safety responses."""

import itertools
import math

import torch

from ..baselines import replace_tracks
from ..players import covered_players


def response_from_replacements(players, values_by_baseline, weights=None):
    """
    功能：由完整上下文及单玩家、跨行为玩家对替换值计算有符号响应和绝对强度。
    输入：
      - players (Sequence[BRTPlayer])：共同有效玩家
      - values_by_baseline (Sequence[dict])：键为被替换玩家下标元组，空元组表示完整真实上下文
      - weights (Sequence[float] | None)：跨基线权重，缺省为均匀权重
    输出：
      - (dict)：single 和 pair 响应、逐成员差分、加权总体方差与标准差、成员数与权重；
        先加权平均有限差分，再取绝对值
    """
    count = len(values_by_baseline)
    raw = [1.0] * count if weights is None else list(weights)
    weights = [w / sum(raw) for w in raw]
    single, pair = [], []
    for i, player in enumerate(players):
        members = [float(values[(i,)] - values[()]) for values in values_by_baseline]
        signed = sum(w * value for w, value in zip(weights, members))
        variance = sum(w * (value - signed) ** 2 for w, value in zip(weights, members))
        single.append({'block_id': player.block_id, 'signed': signed, 'absolute': abs(signed),
                       'member_responses': members, 'variance': variance,
                       'std': math.sqrt(variance)})
    for i, j in itertools.combinations(range(len(players)), 2):
        if players[i].behavior_id == players[j].behavior_id:
            continue
        members = [float(values[(i, j)] - values[(i,)] - values[(j,)] + values[()])
                   for values in values_by_baseline]
        signed = sum(w * value for w, value in zip(weights, members))
        variance = sum(w * (value - signed) ** 2 for w, value in zip(weights, members))
        pair.append({'left_block_id': players[i].block_id, 'right_block_id': players[j].block_id,
                     'signed': signed, 'absolute': abs(signed), 'member_responses': members,
                     'variance': variance, 'std': math.sqrt(variance)})
    return {'single': single, 'pair': pair, 'baseline_member_count': count,
            'baseline_weights': weights}


def compute_safety_responses(history, players, family, predict_target, proxy):
    """
    功能：从完整真实上下文进行单玩家和跨行为玩家对替换，计算代理安全响应。
    输入：
      - history (History)：完整真实历史
      - players (Sequence[BRTPlayer])：BRT 玩家
      - family (BaselineFamily)：与模型依赖共享的条件轨迹基线族
      - predict_target (Callable)：目标车预测回调
      - proxy (Callable)：接收 Prediction 返回风险代理标量，闭包固定环境真实未来
    输出：
      - (dict)：共同有效玩家、基线摘要，以及一阶、二阶有符号响应、绝对强度和跨基线方差
    """
    retained, excluded = covered_players(players, family.available_tracks)
    keys = [(i,) for i in range(len(retained))]
    keys += [(i, j) for i, j in itertools.combinations(range(len(retained)), 2)
             if retained[i].behavior_id != retained[j].behavior_id]
    values_by_baseline = []
    with torch.inference_mode():
        full = float(proxy(predict_target(history)))
        for baseline in family.histories:
            values = {(): full}
            for key in keys:
                tracks = [track for i in key for track in retained[i].track_indices]
                prediction = predict_target(replace_tracks(history, baseline, tracks))
                values[key] = float(proxy(prediction))
            values_by_baseline.append(values)
    return {
        'players': retained, 'excluded_players': excluded,
        'baseline_summary': family.summary(),
        'replacement_values': values_by_baseline,
        **response_from_replacements(retained, values_by_baseline, family.weights),
    }
