# Copyright 2020 - 2021 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable

from monai.handlers.ignite_metric import IgniteMetric
from monai.metrics import DiceMetric
from monai.utils import MetricReduction


class MeanDice(IgniteMetric):
    """
    Computes Dice score metric from full size Tensor and collects average over batch, class-channels, iterations.
    """

    def __init__(
        self, include_background: bool = True, output_transform: Callable = lambda x: x, save_details: bool = True
    ) -> None:
        """

        Args:
            include_background: whether to include dice computation on the first channel of the predicted output.
                Defaults to True.
            output_transform: callable to extract `y_pred` and `y` from `ignite.engine.state.output` then
                construct `(y_pred, y)` pair, where `y_pred` and `y` can be `batch-first` Tensors or
                lists of `channel-first` Tensors. the form of `(y_pred, y)` is required by the `update()`.
                for example: if `ignite.engine.state.output` is `{"pred": xxx, "label": xxx, "other": xxx}`,
                output_transform can be `lambda x: (x["pred"], x["label"])`.
            save_details: whether to save metric computation details per image, for example: mean dice of every image.
                default to True, will save to `engine.state.metric_details` dict with the metric name as key.

        See also:
            :py:meth:`monai.metrics.meandice.compute_meandice`
        """
        metric_fn = DiceMetric(include_background=include_background, reduction=MetricReduction.MEAN)
        super().__init__(metric_fn=metric_fn, output_transform=output_transform, save_details=save_details)
