import random
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------
# 1. Параметр задачі
# -------------------------------------------------
# Заміни на свій номер у списку
N = 2

# -------------------------------------------------
# 2. Вирішальні функції
# -------------------------------------------------
def g1(x1, x2):
    return x2 - x1

def g2(x1, x2, N):
    return x1 + x2 - N

# -------------------------------------------------
# 3. Визначення класу
# -------------------------------------------------
def classify(x1, x2, N):
    val1 = g1(x1, x2)
    val2 = g2(x1, x2, N)

    if val1 >= 0 and val2 < 0:
        return "Omega1"
    elif val1 < 0 and val2 < 0:
        return "Omega2"
    elif val1 >= 0 and val2 >= 0:
        return "Omega3"
    else:
        return "Unknown"

# -------------------------------------------------
# 4. Генерація випадкових об'єктів
# -------------------------------------------------
num_points = 200
points = []

for _ in range(num_points):
    x1 = random.uniform(0, N)
    x2 = random.uniform(0, N)
    cls = classify(x1, x2, N)
    points.append((x1, x2, cls))

# -------------------------------------------------
# 5. Виведення кількох прикладів
# -------------------------------------------------
print("Приклади класифікації:")
for i in range(10):
    x1, x2, cls = points[i]
    print(f"x1={x1:.2f}, x2={x2:.2f} -> {cls}")

# -------------------------------------------------
# 6. Побудова графіка
# -------------------------------------------------
x = np.linspace(0, N, 300)

# Прямі
y_line1 = x              # x2 = x1
y_line2 = N - x          # x2 = N - x1

# Розділяємо точки за класами
omega1_x = [p[0] for p in points if p[2] == "Omega1"]
omega1_y = [p[1] for p in points if p[2] == "Omega1"]

omega2_x = [p[0] for p in points if p[2] == "Omega2"]
omega2_y = [p[1] for p in points if p[2] == "Omega2"]

omega3_x = [p[0] for p in points if p[2] == "Omega3"]
omega3_y = [p[1] for p in points if p[2] == "Omega3"]

unknown_x = [p[0] for p in points if p[2] == "Unknown"]
unknown_y = [p[1] for p in points if p[2] == "Unknown"]

plt.figure(figsize=(9, 7))

# Прямі
plt.plot(x, y_line1, label='g1(x1,x2)=x2-x1=0')
plt.plot(x, y_line2, label='g2(x1,x2)=x1+x2-N=0')

# Точки
plt.scatter(omega1_x, omega1_y, label='Ω1')
plt.scatter(omega2_x, omega2_y, label='Ω2')
plt.scatter(omega3_x, omega3_y, label='Ω3')
plt.scatter(unknown_x, unknown_y, label='Невідомий клас')

plt.xlim(0, N)
plt.ylim(0, N)
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Класифікація об’єктів за вирішальними функціями')
plt.grid(True)
plt.legend()
plt.show()