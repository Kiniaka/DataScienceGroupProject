import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Generowanie przykładowych danych (możesz zamienić na swoje rzeczywiste dane, jeśli są dostępne)
np.random.seed(42)
X = np.random.rand(100, 9)  # 100 próbek, 9 cech
y = np.random.randint(2, size=100)  # Binarny cel (0 lub 1)

# Podział danych na zestawy treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Skalowanie cech
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Trenowanie modelu RandomForest
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Zapis modelu i skalera w jednym pliku
joblib.dump({'model': model, 'scaler': scaler}, 'model_random_forest.pkl')
print("Model i skaler zapisane pomyślnie jako model_random_forest.pkl")
