import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth

# 1. Завантаження даних
X = np.loadtxt('data_clustering.txt', delimiter=',')

# 2. Оцінка bandwidth
bandwidth = estimate_bandwidth(X, quantile=0.1)

# 3. Створення моделі
meanshift = MeanShift(bandwidth=bandwidth)

# 4. Навчання
meanshift.fit(X)

# 5. Мітки
labels = meanshift.labels_

# 6. Центри
centers = meanshift.cluster_centers_

# 7. Кількість кластерів
n_clusters = len(np.unique(labels))
print("Кількість кластерів:", n_clusters)

# 8. Візуалізація
plt.figure()
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50)

plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, marker='X')
plt.title("Mean Shift")
plt.show()