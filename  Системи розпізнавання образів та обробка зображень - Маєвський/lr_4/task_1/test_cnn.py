import torch
from cnn_model import CNNModel

model = CNNModel(num_classes=10)

x = torch.randn(1, 3, 224, 224)
output = model(x)

print("Розмір виходу:", output.shape)