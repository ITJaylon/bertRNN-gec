import torch
from torch import nn
a = torch.tensor([[[1.0,2.0,3.0],[1.0,2.0,3.0]],[[2.0,2.0,3.0],[2.0,2.0,3.0]]])
b = torch.tensor([[0.5],[0.4]])
print(torch.sum(a, dim=1))