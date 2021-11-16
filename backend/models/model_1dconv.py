import torch.nn as nn
import torch.nn.functional as F
from .base_model import BaseModel
from .model_head import ArcMarginProduct


class Yoga1DCnnModel(BaseModel):
    def __init__(self, num_classes, input_dim=2, hidden_layers=[16, 16], kernel_size=10, s=30.0, m=0.5,
                 easy_margin=False, arc_margin=True, normal="batch", pool=False):
        super().__init__()
        if isinstance(kernel_size, int):
            kernel_size = [kernel_size,] * len(hidden_layers)
        in_dim = input_dim
        layers = []
        self.num_classes = num_classes

        for hidden, kernel in zip(hidden_layers, kernel_size):
            layers.append(nn.Conv1d(in_dim, hidden, kernel_size=kernel, padding="same"))
            if normal == "batch":
                layers.append(nn.BatchNorm1d(hidden))
            elif normal == "instance":
                layers.append(nn.InstanceNorm1d(hidden))

            layers.append(nn.ReLU(True))
            if pool:
                layers.append(nn.AvgPool1d(pool))
            in_dim = hidden

        layers.append(nn.AdaptiveAvgPool1d(1))
        layers.append(nn.Flatten(1))

        self.feature = nn.Sequential(*layers)
        self.arc_margin = arc_margin

        if arc_margin:
            self.output_layer = ArcMarginProduct(in_dim, self.num_classes, s, m, easy_margin)
        else:
            self.output_layer = nn.Linear(in_dim, self.num_classes, bias=False)

        self._initParam()

    def _initParam(self):
        for m in self.modules():
            if isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, (nn.BatchNorm1d, nn.GroupNorm)):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x, target=None):
        feature = self.feature(x)

        if self.arc_margin:
            output = self.output_layer(feature, target)
        else:
            output = self.output_layer(feature)

        return output

    def encode(self, x):
        feature = self.feature(x)
        return F.normalize(feature)

    def getWeightLoss(self):
        if self.arc_margin:
            return self.output_layer.getWeightLoss()
        else:
            return 0

    def wantedNamedParameters(self):
        named_parameter_pair = []
        for name, p in self.named_parameters():
            if "feature" in name or "output_layer" in name:
                named_parameter_pair.append([name, p])
        return named_parameter_pair
