import torch
from torch import nn
from torch.nn import functional as F


class MLP(torch.nn.Module):
    def __init__(self, obs_size, n_act):
        super().__init__()
        self.mlp = torch.nn.Sequential(
            torch.nn.Linear(obs_size, 50),
            torch.nn.ReLU(),
            torch.nn.Linear(50, 50),
            torch.nn.ReLU(),
            torch.nn.Linear(50, n_act)
        )

    def forward(self, X):
        return self.mlp(X)

