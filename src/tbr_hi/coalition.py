"""Loss-game evaluation through a caller-supplied prediction function."""

import torch

from .baselines import replace_tracks
from .decomposition import decompose_loss_tables
from .players import covered_players


def min_ade(prediction, target_future, target_valid, future_eval_steps=40):
    """
    功能：在有效真实未来帧上计算各模态 ADE，并为该联盟重新选择最小模态。
    输入：
      - prediction (Prediction)：目标车预测
      - target_future (torch.Tensor)：有限数值的真实未来位置 [F,2]，无效帧也使用有限填充值
      - target_valid (torch.Tensor)：真实未来有效掩码 [F]，评价窗口内至少一帧有效
      - future_eval_steps (int)：评价时域，正式设置为 40 帧
    输出：
      - (torch.Tensor)：标量 minADE
    """
    mask = target_valid[:future_eval_steps]
    distances = torch.linalg.vector_norm(
        prediction.xy[:, :future_eval_steps] - target_future[None, :future_eval_steps], dim=-1,
    )
    return ((distances * mask).sum(dim=-1) / mask.sum()).min()


def compute_model_dependence(
    history, players, family, predict_target, target_future, target_valid,
    robust_lambda=0.25, future_eval_steps=40, predict_many=None, batch_size=8,
):
    """
    功能：在共同有效玩家上精确计算条件基线恢复博弈及模型上下文依赖。
    输入：
      - history (History)：完整真实历史
      - players (Sequence[BRTPlayer])：由真实历史定义的玩家
      - family (BaselineFamily)：同模型条件轨迹基线族
      - predict_target (Callable)：接收 History 返回 Prediction 的目标车预测回调
      - target_future (torch.Tensor)：目标车真实未来 [F,2]
      - target_valid (torch.Tensor)：真实未来掩码 [F]
      - robust_lambda (float)：股利收缩强度
      - future_eval_steps (int)：评价未来帧数
      - predict_many (Callable | None)：可选的批量预测回调，接收 list[History]
      - batch_size (int)：联盟前向批大小
    输出：
      - (dict)：保留与排除玩家、基线数量与覆盖摘要、有效目标未来帧数、损失表和行为支持分解
    """
    retained, excluded = covered_players(players, family.available_tracks)
    count = 1 << len(retained)
    losses = []
    with torch.inference_mode():
        for baseline in family.histories:
            row = []
            for start in range(0, count, batch_size):
                inputs = []
                for mask in range(start, min(start + batch_size, count)):
                    replaced = [track for i, p in enumerate(retained) if not mask & (1 << i)
                                for track in p.track_indices]
                    inputs.append(replace_tracks(history, baseline, replaced))
                predictions = ([predict_target(item) for item in inputs] if predict_many is None
                               else predict_many(inputs))
                row.extend(float(min_ade(p, target_future, target_valid, future_eval_steps))
                           for p in predictions)
            losses.append(row)
    return {
        'players': retained, 'excluded_players': excluded, 'losses_by_baseline': losses,
        'baseline_summary': family.summary(),
        'target_valid_frame_count': int(target_valid[:future_eval_steps].sum()),
        **decompose_loss_tables(retained, losses, family.weights, robust_lambda),
    }
