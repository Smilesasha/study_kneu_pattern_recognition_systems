# Імпорт бібліотек
import json
import datetime
import warnings
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from sklearn import cluster, covariance
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# -------------------------------------------------
# 1. Вхідний файл із символами компаній
# -------------------------------------------------
input_file = 'company_symbol_mapping.json'

# -------------------------------------------------
# 2. Завантаження прив'язок символів компаній до назв
# -------------------------------------------------
with open(input_file, 'r', encoding='utf-8') as f:
    company_symbols_map = json.load(f)

symbols = np.array(list(company_symbols_map.keys()))
names = np.array(list(company_symbols_map.values()))

# -------------------------------------------------
# 3. Параметри періоду
# -------------------------------------------------
start_date = datetime.datetime(2003, 7, 3)
end_date = datetime.datetime(2007, 5, 4)

# -------------------------------------------------
# 4. Завантаження котирувань
# -------------------------------------------------
quotes_diff_list = []
valid_names = []
valid_symbols = []

warnings.filterwarnings("ignore")

for symbol, name in zip(symbols, names):
    try:
        data = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False
        )

        # Якщо даних немає — пропускаємо
        if data.empty:
            print(f'Немає даних для {symbol}, пропускаємо.')
            continue

        # Перевірка наявності колонок
        if 'Open' not in data.columns or 'Close' not in data.columns:
            print(f'Немає Open/Close для {symbol}, пропускаємо.')
            continue

        # Перетворюємо в 1D масиви
        open_prices = np.asarray(data['Open']).astype(float).reshape(-1)
        close_prices = np.asarray(data['Close']).astype(float).reshape(-1)

        # Видаляємо NaN
        valid_mask = ~np.isnan(open_prices) & ~np.isnan(close_prices)
        open_prices = open_prices[valid_mask]
        close_prices = close_prices[valid_mask]

        # Якщо після очищення даних не залишилось — пропускаємо
        if len(open_prices) == 0 or len(close_prices) == 0:
            print(f'Порожні ряди для {symbol}, пропускаємо.')
            continue

        # Вирівнюємо довжини
        min_len = min(len(open_prices), len(close_prices))
        open_prices = open_prices[:min_len]
        close_prices = close_prices[:min_len]

        # Різниця між закриттям і відкриттям
        diff = close_prices - open_prices

        # Додаємо до списку
        quotes_diff_list.append(diff)
        valid_symbols.append(symbol)
        valid_names.append(name)

    except Exception as e:
        print(f'Помилка для {symbol}: {e}')

# -------------------------------------------------
# 5. Перевірка кількості валідних компаній
# -------------------------------------------------
if len(quotes_diff_list) < 2:
    raise ValueError("Недостатньо компаній із валідними даними для кластеризації.")

# -------------------------------------------------
# 6. Обрізаємо всі ряди до однакової довжини
# -------------------------------------------------
global_min_len = min(len(arr) for arr in quotes_diff_list)
quotes_diff_list = [arr[:global_min_len] for arr in quotes_diff_list]

# -------------------------------------------------
# 7. Формування матриці ознак
#    Рядки = дні, стовпці = компанії
# -------------------------------------------------
X = np.array(quotes_diff_list, dtype=float).T

print("Форма X до нормалізації:", X.shape)

# Якщо X не 2D — аварійно завершуємо
if X.ndim != 2:
    raise ValueError(f"Очікувався 2D масив, але отримано X.ndim = {X.ndim}")

# -------------------------------------------------
# 8. Нормалізація даних
# -------------------------------------------------
X = StandardScaler().fit_transform(X)

# -------------------------------------------------
# 9. Побудова графової моделі
# -------------------------------------------------
edge_model = covariance.GraphicalLassoCV()

with np.errstate(all='ignore'):
    edge_model.fit(X)

# -------------------------------------------------
# 10. Кластеризація методом поширення подібності
# -------------------------------------------------
_, labels = cluster.affinity_propagation(edge_model.covariance_)

n_labels = labels.max() + 1

# -------------------------------------------------
# 11. Виведення результатів
# -------------------------------------------------
print("\nЗнайдено кластерів:", n_labels)
print()

valid_names = np.array(valid_names)
valid_symbols = np.array(valid_symbols)

for i in range(n_labels):
    cluster_companies = valid_names[labels == i]
    print(f"Кластер {i + 1} => {', '.join(cluster_companies)}")

# -------------------------------------------------
# 12. Візуалізація компаній у 2D через PCA
# -------------------------------------------------
# labels належать компаніям, тому беремо X.T:
# рядки = компанії, стовпці = ознаки по днях
X_companies = X.T

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_companies)

plt.figure(figsize=(10, 6))

for i in range(n_labels):
    plt.scatter(
        X_2d[labels == i, 0],
        X_2d[labels == i, 1],
        s=100,
        label=f'Кластер {i + 1}'
    )

# Підписи компаній
for i, name in enumerate(valid_names):
    plt.text(X_2d[i, 0], X_2d[i, 1], name, fontsize=9)

plt.title('Кластеризація компаній фондового ринку')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.legend()
plt.grid(True)
plt.show()