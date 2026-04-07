import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

try:
    df = pd.read_csv('1.txt')
    print("Файл 1.txt успішно завантажено!")
except FileNotFoundError:
    print("Помилка: Файл 1.txt не знайдено.")
    exit()


df = df.dropna(subset=['price'])
df['train_class'] = df['train_class'].fillna(df['train_class'].mode()[0])
df['fare'] = df['fare'].fillna(df['fare'].mode()[0])


le_train_type = LabelEncoder()
le_train_class = LabelEncoder()
le_fare = LabelEncoder()

df['train_type_enc'] = le_train_type.fit_transform(df['train_type'])
df['train_class_enc'] = le_train_class.fit_transform(df['train_class'])
df['fare_enc'] = le_fare.fit_transform(df['fare'])


X = df[['price', 'train_type_enc', 'train_class_enc']]
y = df['fare_enc']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)

print("\n--- Результати Байєсівського аналізу ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nЗвіт по класах:")
print(classification_report(y_test, y_pred, target_names=le_fare.classes_, labels=np.unique(y_pred)))

# --- Крок 6: Візуалізація ---
# Розподіл цін (Gaussian distribution visualization)
plt.figure(figsize=(10, 5))
sns.kdeplot(data=df, x='price', hue='fare', fill=True, common_norm=False)
plt.title('Байєсівський розподіл ймовірностей цін для тарифів')
plt.grid(True, alpha=0.3)
plt.show()