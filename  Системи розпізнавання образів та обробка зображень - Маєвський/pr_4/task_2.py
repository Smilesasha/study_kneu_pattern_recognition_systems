import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin

# Завантаження набору даних Iris
iris = load_iris()
X = iris['data']
y = iris['target']

# -------------------------------------------------
# 1. Кластеризація K-means для Iris
# -------------------------------------------------

# Створення моделі KMeans для 3 кластерів,
# оскільки в наборі Iris є 3 класи
kmeans = KMeans(n_clusters=3, random_state=0, n_init=10)

# Навчання моделі
kmeans.fit(X)

# Передбачення міток кластерів
y_kmeans = kmeans.predict(X)

# Візуалізація результату (по перших двох ознаках)
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

# Отримання центрів кластерів
centers = kmeans.cluster_centers_

# Відображення центрів кластерів
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.title('KMeans для набору Iris')
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.show()

# -------------------------------------------------
# 2. Власна реалізація пошуку кластерів
# -------------------------------------------------

def find_clusters(X, n_clusters, rseed=2):
    # Випадкове вибирання початкових центрів
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]

    while True:
        # Призначення міток за найближчим центром
        labels = pairwise_distances_argmin(X, centers)

        # Обчислення нових центрів
        new_centers = np.array([X[labels == i].mean(0) for i in range(n_clusters)])

        # Якщо центри не змінюються, зупиняємо цикл
        if np.all(centers == new_centers):
            break

        centers = new_centers

    return centers, labels

# Використання власної функції
centers, labels = find_clusters(X, 3)

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.title('Власна реалізація кластеризації Iris')
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.show()

# -------------------------------------------------
# 3. Та ж функція з іншим random seed
# -------------------------------------------------

centers, labels = find_clusters(X, 3, rseed=0)

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.title('Власна кластеризація Iris (rseed=0)')
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.show()

# -------------------------------------------------
# 4. Швидкий варіант через fit_predict
# -------------------------------------------------

labels = KMeans(n_clusters=3, random_state=0, n_init=10).fit_predict(X)

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
plt.title('KMeans fit_predict для Iris')
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.show()