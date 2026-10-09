"""Run TBR-HI on artificial trajectories and a deterministic illustrative predictor."""

import torch

from tbr_hi.baselines import build_baseline_family
from tbr_hi.behavior import build_players
from tbr_hi.coalition import compute_model_dependence
from tbr_hi.interfaces import EnvironmentForecast, History, Prediction
from tbr_hi.safety import FutureContext, compute_safety_responses, spatial_proxy, temporal_proxy


def synthetic_history(times):
    """
    功能：构造包含目标车和四辆环境车的人工历史轨迹。
    输入：
      - times (torch.Tensor)：21 帧时间轴 [T]
    输出：
      - (History)：与任何研究数据集无关的合成场景
    """
    origin = torch.tensor([[0., 0.], [12., 0.], [22., 3.], [42., -3.], [-15., 6.]], dtype=times.dtype)
    velocity0 = torch.tensor([[8., 0.], [5., 0.], [6., 0.], [7., 0.], [0., 0.]], dtype=times.dtype)
    acceleration = torch.tensor([[0., 0.], [-1., 0.], [0.8, 0.], [0., 0.], [0., 0.]], dtype=times.dtype)
    xy = origin[:, None] + velocity0[:, None] * times[None, :, None]
    xy += 0.5 * acceleration[:, None] * times[None, :, None] ** 2
    velocity = velocity0[:, None] + acceleration[:, None] * times[None, :, None]
    return History(
        xy, torch.ones(xy.shape[:2], dtype=torch.bool), velocity,
        torch.zeros(xy.shape[:2], dtype=times.dtype), acceleration[:, None].expand_as(xy).clone(),
        times, 0, torch.ones(len(xy), dtype=torch.bool), tuple(f'synthetic_{i}' for i in range(len(xy))),
    )


class IllustrativePredictor:
    """One deterministic model provides both target and environment predictions."""

    def predict(self, history, track, steps):
        """
        功能：通过邻车历史构造可展示上下文依赖的六模态预测。
        输入：
          - history (History)：仅使用传入历史的场景
          - track (int)：预测车辆槽位
          - steps (int)：预测帧数
        输出：
          - (Prediction)：六模态合成预测及概率
        """
        time = torch.arange(1, steps + 1, dtype=history.xy.dtype) * 0.1
        displacement = history.xy[:, -1] - history.xy[track, -1]
        distance = torch.linalg.vector_norm(displacement, dim=-1)
        weights = torch.exp(-distance / 25.)
        weights[track] = 0
        speed = (history.velocity[:, :, 0] * history.valid).sum(dim=1) / history.valid.sum(dim=1)
        context = (weights * speed).sum() / (1 + weights.sum())
        curvature = 0.10 * context + 0.02 * context ** 2
        mode_offsets = torch.linspace(-0.25, 0.25, 6, dtype=time.dtype)
        xy = history.xy[track, -1][None, None] + history.velocity[track, -1][None, None] * time[None, :, None]
        xy = xy.repeat(6, 1, 1)
        xy[:, :, 0] += (curvature + mode_offsets[:, None]) * time[None] ** 2
        xy[:, :, 1] += (0.08 * context + 0.2 * mode_offsets[:, None]) * time[None] ** 2
        probability = torch.tensor([0.3, 0.23, 0.18, 0.13, 0.09, 0.07], dtype=time.dtype)
        return Prediction(xy, probability)

    def target(self, history):
        """
        功能：返回当前目标车的 40 帧合成预测。
        输入：
          - history (History)：目标车当前历史窗口
        输出：
          - (Prediction)：目标车预测
        """
        return self.predict(history, history.target_index, 40)

    def environment(self, earlier_history):
        """
        功能：用同一个模型从更早真实历史预测环境车的 20 帧轨迹。
        输入：
          - earlier_history (History)：截至替换窗口锚点的真实历史
        输出：
          - (EnvironmentForecast)：环境车六模态预测、概率和真实锚点
        """
        tracks = [i for i in range(len(earlier_history.xy)) if i != earlier_history.target_index]
        predictions = [self.predict(earlier_history, i, 20) for i in tracks]
        return EnvironmentForecast(
            torch.stack([p.xy for p in predictions]), torch.stack([p.probability for p in predictions]),
            earlier_history.xy[tracks, -1], tuple(earlier_history.object_ids[i] for i in tracks),
        )


def main():
    """
    功能：展示 BRT 构造、同模型基线、模型依赖以及空间和时间风险代理响应。
    输入：
      - 无
    输出：
      - (None)：在终端打印合成示例的逐玩家结果
    """
    torch.set_num_threads(1)
    history = synthetic_history(torch.linspace(-2., 0., 21, dtype=torch.float64))
    earlier = synthetic_history(torch.linspace(-4., -2., 21, dtype=torch.float64))
    future_history = synthetic_history(torch.arange(1, 41, dtype=torch.float64) * 0.1)
    model = IllustrativePredictor()
    players = build_players(history)
    family = build_baseline_family(history, earlier, model.environment)
    dependence = compute_model_dependence(
        history, players, family, model.target, future_history.xy[0], future_history.valid[0],
    )
    context = FutureContext(
        future_history.xy, future_history.valid, future_history.heading,
        torch.full((5,), 4.5, dtype=torch.float64), torch.full((5,), 1.8, dtype=torch.float64),
        torch.ones((5, 40), dtype=torch.bool), 0,
    )
    spatial = compute_safety_responses(history, players, family, model.target,
                                       lambda prediction: spatial_proxy(prediction, context))
    temporal = compute_safety_responses(history, players, family, model.target,
                                        lambda prediction: temporal_proxy(prediction, context))
    print('Synthetic illustration only; these values are not paper results.')
    print(f'Players: {len(dependence["players"])}; baseline family: {family.summary()}')
    print(f'{"BRT player":48} {"D":>12} {"Rs":>12} {"Rt":>12}')
    for spatial_row, temporal_row in zip(spatial['single'], temporal['single']):
        block = spatial_row['block_id']
        print(f'{block:48} {dependence["D"][block]:12.6f} '
              f'{spatial_row["absolute"]:12.6f} {temporal_row["absolute"]:12.6f}')
    print('Cross-behavior pairs:', len(spatial['pair']))
    print('Per-player spatial response variance:',
          {row['block_id']: row['variance'] for row in spatial['single']})
    print('BO1 + BO2 + higher-order + shrinkage remainder:',
          dependence['scene_order_summary']['mean_full_context_loss_improvement'])


if __name__ == '__main__':
    main()
