import numpy as np

# Вхідні дані
lambda12 = 0.68
lambda21 = 0.5
P_w1 = 1/4
P_w2 = 3/4
sigma2 = 0.28

# Обчислення порога
x = 0.5 - sigma2 * np.log((lambda21 / lambda12) * (P_w2 / P_w1))

print(f"Поріг x = {x:.6f}")