import torch
import torch.nn as nn
import torch.nn.functional as F
from .base_model import BaseModel
import math


class ArcMarginProduct(BaseModel):
    def __init__(self, in_features, out_features, s=30.0, m=0.5,
                 easy_margin=False):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.easy_margin = easy_margin
        self.s = s
        self.m = m
        self.cos_m = math.cos(m)
        self.sin_m = math.sin(m)
        self.th = math.cos(math.pi - m)
        self.mm = math.sin(math.pi - m) * m

        self.weight = torch.nn.Parameter(torch.FloatTensor(self.out_features, self.in_features))
        nn.init.xavier_uniform_(self.weight)

    def forward(self, feature, label):
        cosine = F.linear(F.normalize(feature), F.normalize(self.weight))
        if label is None:
            return cosine
        sine = torch.sqrt(1.0 - torch.pow(cosine, 2) + 1e-9)
        phi = cosine * self.cos_m - sine * self.sin_m
        if self.easy_margin:
            phi = torch.where(cosine > 0, phi, cosine)
        else:
            phi = torch.where(cosine > self.th, phi, cosine - self.mm)
        one_hot = torch.zeros(cosine.size(), device=feature.device)
        one_hot.scatter_(1, label.view(-1, 1).long(), 1)
        output = (one_hot * phi) + ((1.0 - one_hot) * cosine)
        output *= self.s
        return output

    def getWeightLoss(self):
        norm_weight = F.normalize(self.weight)
        pairwise_weight_cos = torch.mm(norm_weight, norm_weight.T)
        pairwise_weight_cos = torch.where(pairwise_weight_cos > 0, pairwise_weight_cos,
                                          torch.zeros_like(pairwise_weight_cos).to(pairwise_weight_cos.device))

        weight_cos_loss = (torch.sum(pairwise_weight_cos) - self.out_features) / \
                          (torch.count_nonzero(pairwise_weight_cos) - self.out_features)
        return weight_cos_loss
