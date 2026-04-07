# -------------------------------------------------
# Реалізація логічних функцій OR, AND, XOR
# через двохшаровий персептрон
# -------------------------------------------------

def activation(v):
    """Порогова функція активації"""
    return 1 if v > 0 else 0


def neuron(x1, x2, w1, w2, w0):
    """Модель одного нейрона"""
    v = w1 * x1 + w2 * x2 + w0
    return activation(v)


def logical_or(x1, x2):
    """
    OR:
    g(x) = x1 + x2 - 0.5
    """
    return neuron(x1, x2, 1, 1, -0.5)


def logical_and(x1, x2):
    """
    AND:
    g(x) = x1 + x2 - 1.5
    """
    return neuron(x1, x2, 1, 1, -1.5)


def logical_xor(x1, x2):
    """
    XOR через OR і AND
    y1 = OR(x1, x2)
    y2 = AND(x1, x2)

    На другому шарі:
    g(y1, y2) = y1 - y2 - 0.5
    """
    y1 = logical_or(x1, x2)
    y2 = logical_and(x1, x2)
    xor_result = neuron(y1, y2, 1, -1, -0.5)
    return y1, y2, xor_result


# -------------------------------------------------
# Перевірка для всіх вхідних комбінацій
# -------------------------------------------------
inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

print(" x1  x2 | OR AND XOR ")
print("----------------------")

for x1, x2 in inputs:
    y1, y2, y = logical_xor(x1, x2)
    print(f"  {x1}   {x2} |  {y1}   {y2}   {y}")