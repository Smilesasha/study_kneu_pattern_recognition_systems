import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1. Завантаження даних
X = np.loadtxt('data_clustering.txt', delimiter=',')

# 2. Візуалізація початкових даних
plt.figure()
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.title("Вхідні дані")
plt.show()

# 3. Кількість кластерів (згідно методички = 5)
k = 5

# 4. Створення моделі
kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10)

# 5. Навчання
kmeans.fit(X)

# 6. Отримання міток
labels = kmeans.predict(X)

# 7. Центри кластерів
centers = kmeans.cluster_centers_

# 8. Візуалізація результату
plt.figure()
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50)
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, marker='X')
plt.title("K-means кластеризація")
plt.show()