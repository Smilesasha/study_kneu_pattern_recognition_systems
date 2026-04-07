import math

# -------------------------------------------------
# 1. Еталонні об'єкти
# -------------------------------------------------
etalons = {
    "Легковий автомобіль": [0, 1, 0, 0, 1, 1],
    "Мотоцикл":            [1, 0, 0, 0, 0, 1],
    "Автобус":             [0, 1, 1, 0, 1, 1],
    "Вантажівка":          [0, 1, 0, 1, 1, 0]
}

# -------------------------------------------------
# 2. Об'єкти для розпізнавання
# -------------------------------------------------
objects = {
    "Об'єкт A": [0, 1, 1, 0, 1, 0],   # схожий на автобус
    "Об'єкт B": [1, 0, 0, 0, 0, 1],   # повністю збігається з мотоциклом
    "Об'єкт C": [0, 1, 0, 1, 1, 1]    # схожий на вантажівку
}

# -------------------------------------------------
# 3. Обчислення a, b, g, h
# -------------------------------------------------
def calc_abgh(xi, xj):
    a = b = g = h = 0
    for i in range(len(xi)):
        if xi[i] == 1 and xj[i] == 1:
            a += 1
        elif xi[i] == 0 and xj[i] == 0:
            b += 1
        elif xi[i] == 1 and xj[i] == 0:
            g += 1
        elif xi[i] == 0 and xj[i] == 1:
            h += 1
    return a, b, g, h

# -------------------------------------------------
# 4. Функції подібності S1-S7
# -------------------------------------------------
def s1(a, b, g, h, n):
    return a / n

def s2(a, b, g, h, n):
    denom = n - b
    return a / denom if denom != 0 else 0

def s3(a, b, g, h, n):
    denom = 2 * a + g + h
    return a / denom if denom != 0 else 0

def s4(a, b, g, h, n):
    denom = a + 2 * (g + h)
    return a / denom if denom != 0 else 0

def s5(a, b, g, h, n):
    return (a + b) / n

def s6(a, b, g, h, n):
    denom = g + h
    return (a + b) / denom if denom != 0 else float("inf")

def s7(a, b, g, h, n):
    denom = a * b + g * h
    return (a * b - g * h) / denom if denom != 0 else 0

similarities = {
    "S1": s1,
    "S2": s2,
    "S3": s3,
    "S4": s4,
    "S5": s5,
    "S6": s6,
    "S7": s7
}

# -------------------------------------------------
# 5. Власна унікальна функція
# -------------------------------------------------
# Ідея: більш висока вага на спільні наявні ознаки, ніж на спільні відсутні
def s8_custom(a, b, g, h, n):
    denom = 2 * a + b + g + h
    return (2 * a + 0.5 * b) / denom if denom != 0 else 0

# -------------------------------------------------
# 6. Розпізнавання
# -------------------------------------------------
def classify_object(obj_name, obj_vector):
    print(f"\n{'='*60}")
    print(f"Розпізнавання: {obj_name} = {obj_vector}")
    print(f"{'='*60}")

    n = len(obj_vector)

    for sim_name, sim_func in similarities.items():
        best_class = None
        best_value = -10**9

        print(f"\n{sim_name}:")
        for etalon_name, etalon_vector in etalons.items():
            a, b, g, h = calc_abgh(obj_vector, etalon_vector)
            value = sim_func(a, b, g, h, n)

            print(
                f"{etalon_name:22s} -> a={a}, b={b}, g={g}, h={h}, "
                f"{sim_name}={value:.4f}"
            )

            if value > best_value:
                best_value = value
                best_class = etalon_name

        print(f"Найбільш схожий образ за {sim_name}: {best_class} ({best_value:.4f})")

    print("\nS8 (власна функція):")
    best_class = None
    best_value = -10**9
    for etalon_name, etalon_vector in etalons.items():
        a, b, g, h = calc_abgh(obj_vector, etalon_vector)
        value = s8_custom(a, b, g, h, n)

        print(
            f"{etalon_name:22s} -> a={a}, b={b}, g={g}, h={h}, S8={value:.4f}"
        )

        if value > best_value:
            best_value = value
            best_class = etalon_name

    print(f"Найбільш схожий образ за S8: {best_class} ({best_value:.4f})")

# -------------------------------------------------
# 7. Запуск
# -------------------------------------------------
for obj_name, obj_vector in objects.items():
    classify_object(obj_name, obj_vector)