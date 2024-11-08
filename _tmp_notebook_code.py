#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import shapiro
import seaborn as sns
from sklearn.preprocessing import LabelEncoder,StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


# Zaciągamy dane do analizy
# df = pd.read_csv('/content/drive/MyDrive/internet_service_churn.csv')
df = pd.read_csv('internet_service_churn.csv')

# Sprawdzamy informacje o danych
print(f'Zaciągnięte dane:')
print(df.head())
print(f'Ogólne informacje o danych:')
print(df.info())
print(df.describe())
print(f'Sprawdzamy czy kolumny mają jakieś puste dane:')
print(df.isnull().sum())


# In[5]:


# HISTOGRAM
df.hist(bins=50, figsize=(20,15))
plt.show()
#


# In[6]:


# Standaryzacja danych i zastąpienie NAN wartosciami obliczonymi wartość x -  srednia z x /odchylenie stadardowe z x gdzie x - to wartość wiersza z wybranej kolumny

# Normalizacja kolumn tylko w przypadku kolumn zawierających NaN
for column in df.columns:
    if df[column].isnull().any():
        df[column] = (df[column] - df[column].mean()) / df[column].std()

# Zastępowanie NaN obliczonymi wartościami dla każdej kolumny
for column in df.columns:
    if df[column].isnull().any():
        mean_value = df[column].mean()
        df[column].fillna(mean_value, inplace=True)

# Sprawdzenie likwidacji wierszy z wartościami NaN poprzez drukowanie kolumn, które nadal mają wartości NaN
columns_with_nan = df.columns[df.isnull().any()].tolist()
if columns_with_nan == []:
    print("Brak kolumn z wartościami NaN ! ")
else:
    print(columns_with_nan)


# Test Shapiro-Wilka
# 
# 1. Iteruje przez każdą kolumnę w DataFrame df.
# 2. Oblicza statystykę testu Shapiro-Wilka oraz wartość p (p_value) dla kolumny, pomijając brakujące wartości (NaN).
# 3. Wyświetlam nazwę kolumny, statystykę testu oraz wartość p.
# 4. Sprawdzam, czy wartość p jest większa niż 0.05. Jeśli tak, przyjmuje, że kolumna ma rozkład normalny. W przeciwnym razie, przyjmuje, że kolumna nie ma rozkładu normalnego.

# In[7]:


# Test Shapiro-Wilka dla każdej kolumny
for column in df.columns:
    stat, p_value = shapiro(df[column].dropna())
    print(f"Kolumna: {column}, Statystyka: {stat}, P-wartość: {p_value}")
    if p_value > 0.05:
        print(f"Kolumna '{column}' ma rozkład normalny (p > 0.05)")
    else:
        print(f"Kolumna '{column}' nie ma rozkładu normalnego (p <= 0.05)")


# 1. Iteruję przez każdą kolumnę w DataFrame df.
# 2. Tworzę wykres Q-Q, używając stats.probplot, pomijając brakujące wartości(NaN) i porównując je z rozkładem normalnym.
# 3. Ustawiam tytuł wykresu na "Q-Q Plot for {column}" i wyświetla wykres.
# 
# PODSUMOWANIE TESTU: Kod ten pomaga zarówno statystycznie, jak i wizualnie ocenić, czy dane w każdej kolumnie mają rozkład normalny.

# In[8]:


# Wykres Q-Q dla każdej kolumny
for column in df.columns:
    stats.probplot(df[column].dropna(), dist="norm", plot=plt)
    plt.title(f"Q-Q Plot for {column}")
    plt.show()


# In[9]:


percentiles = [25, 50, 75]  # Możena podać dowolne percentyle (np. 25%, 50%, 75%)

# Obliczenie percentyli
subscription_age_percentiles = df['subscription_age'].quantile([p / 100 for p in percentiles])
bill_avg_percentiles = df['bill_avg'].quantile([p / 100 for p in percentiles])
reamining_contract_percentiles = df['reamining_contract'].quantile([p / 100 for p in percentiles])
download_percentiles = df['download_avg'].quantile([p / 100 for p in percentiles])
upload_percentiles = df['upload_avg'].quantile([p / 100 for p in percentiles])

print("Percentyle dla subscription_age:\n", subscription_age_percentiles)
print("Percentyle dla bill_avg:\n", bill_avg_percentiles)
print("Percentyle dla reamining_contract:\n", reamining_contract_percentiles)
print("Percentyle dla download_avg:\n", download_percentiles)
print("Percentyle dla upload_avg:\n", upload_percentiles)


# In[10]:


# Obliczenie macierzy korelacji wraz z jej wizualicją

correlation_matrix = df.corr()

print("Macierz korelacji:\n", correlation_matrix)

# Wykres macierzy korelacji

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Macierz korelacji")
plt.show()


# In[11]:


# Koduje kolumnę 'churn' i jednocześnie zastąpuje zakodowane wartości etykietami tekstowymi tzn: cyfra 0 zastępowana "pozostaje", a cyfra 1 zastępowana 'odchodzi'.

# Inicjalizacja LabelEncoder
label_encoder = LabelEncoder()

# Tworzenie kopii DataFrame
df_standard =  df.copy()

# Zakodowanie etykiet w kolumnie 'churn'
df_standard['churn_encoded'] = label_encoder.fit_transform(df_standard['churn'])

# Zastąpienie zakodowanych wartości etykietami tekstowymi tzn: cyfra 0 zastępowana "pozostaje", a cyfra 1 zastępowana 'odchodzi'.
df_standard['churn_encoded'] = df['churn'].replace({0: 'pozostaje', 1: 'odchodzi'})

# Wyświetlenie DataFrame po dodaniu kolumny z zakodowanymi danymi
print("\nDataFrame po dodaniu kolumny Label Encoding:\n", df_standard)


# **WALIDACJA KRZYŻOWA** - im wyższe wyniki walidacji krzyżowej tym lepsza generalizację modelu, czyli jego zdolność do poprawnego przewidywania na nowych, niewidzianych wcześniej danych.
# 
# **Wynik F1 (F1 Score)** to miara skuteczności modelu, która uwzględnia zarówno precyzję (precision), jak i czułość (recall). Jest szczególnie przydatna w przypadkach, gdy masz do czynienia z niezbalansowanymi danymi.
# 
# **Precyzja (Precision)**: Odsetek trafnych pozytywnych przewidywań spośród wszystkich pozytywnych przewidywań (true positives / (true positives + false positives)).
# 
# **Czułość (Recall)**: Odsetek trafnych pozytywnych przewidywań spośród wszystkich rzeczywistych pozytywnych przypadków (true positives / (true positives + false negatives)).
# 
# **Dokładność (accuracy)** to miara wydajności modelu, która wskazuje, jak dobrze model klasyfikuje dane w porównaniu do wszystkich danych. Jest to stosunek poprawnych przewidywań (zarówno prawdziwie pozytywnych, jak i prawdziwie negatywnych) do całkowitej liczby przewidywań.

# In[18]:


# MODEL LOSOWEGO LASU

print("RandomForestClassifier")

# Przygotowanie danych wejściowych i wyjściowych: wykluczamy kolumny: 'churn', 'churn_encoded' i 'id'. Określamy kolumnę docelową (target), którą chcemy przewidzieć (churn).

X = df_standard.drop(columns=['churn', 'churn_encoded', 'id'])
y = df_standard['churn']

# Skalowanie danych (opcjonalne, ale zalecane) - aby miały średnią 0 i odchylenie standardowe 1.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Podział na zestaw treningowy i testowy ( zestaw treningowy (X_train, y_train) i testowy (X_test, y_test) w stosunku 80/20 oraz random_state=42, który zapewnia powtarzalność wyników.)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Inicjalizacja modelu
model = RandomForestClassifier(random_state=42)

# Walidacja krzyżowa
RFC_cross_val_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
print("Średnia dokładność z walidacji krzyżowej:", RFC_cross_val_scores.mean())

# Uczenie modelu
model.fit(X_train, y_train)

# Predykcja na zbiorze testowym
y_pred = model.predict(X_test)

# Ocena modelu
RFC_accuracy = accuracy_score(y_test, y_pred)
RFC_recall = recall_score(y_test, y_pred)
RFC_precision = precision_score(y_test, y_pred)
RFC_f1 = f1_score(y_test, y_pred)

print("\nOcena modelu:")
print("Dokładność (Accuracy):", RFC_accuracy)
print("Czułość (Recall):", RFC_recall)
print("Precyzja (Precision):", RFC_precision)
print("Wynik F1 (F1 Score):", RFC_f1)


# In[ ]:


# Model Regresji liniowej

print('LogisticRegression')

# Przygotowanie danych wejściowych i wyjściowych: wykluczamy kolumny: 'churn', 'churn_encoded' i 'id'. Określamy kolumnę docelową (target), którą chcemy przewidzieć (churn).

X = df_standard.drop(columns=['churn', 'churn_encoded', 'id'])
y = df_standard['churn']

# Skalowanie danych:
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Podział na zestaw treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Inicjalizacja modelu regresji logistycznej
LR_model = LogisticRegression(
    penalty='l2', solver='lbfgs', random_state=42, max_iter=1000)

# Walidacja krzyżowa
LR_cross_val_scores = cross_val_score(
    LR_model, X_train, y_train, cv=5, scoring='accuracy')
print("Średnia dokładność z walidacji krzyżowej:", LR_cross_val_scores.mean())

# Uczenie modelu
LR_model.fit(X_train, y_train)

# Predykcja na zbiorze testowym
y_pred = LR_model.predict(X_test)

# Ocena modelu
LR_accuracy = accuracy_score(y_test, y_pred)
LR_recall = recall_score(y_test, y_pred)
LR_precision = precision_score(y_test, y_pred)
LR_f1 = f1_score(y_test, y_pred)

print("\nOcena modelu:")
print("Dokładność (Accuracy):", LR_accuracy)
print("Czułość (Recall):", LR_recall)
print("Precyzja (Precision):", LR_precision)
print("Wynik F1 (F1 Score):", LR_f1)


# In[14]:


# SVC Model
print('SVC')

# Przygotowanie danych wejściowych i wyjściowych: wykluczamy kolumny: 'churn', 'churn_encoded' i 'id'
X = df_standard.drop(columns=['churn', 'churn_encoded', 'id'])
y = df_standard['churn']

# Skalowanie danych
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Podział na zestaw treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Inicjalizacja modelu SVC ze zwiększoną liczbą iteracji
SVC_model = SVC(C=0.01, random_state=42, max_iter=1000)

# Walidacja krzyżowa
SVC_cross_val_scores = cross_val_score(
    SVC_model, X_train, y_train, cv=5, scoring='accuracy')
print("Średnia dokładność z walidacji krzyżowej:", SVC_cross_val_scores.mean())

# Uczenie modelu
SVC_model.fit(X_train, y_train)

# Predykcja na zbiorze testowym
y_pred = SVC_model.predict(X_test)

# Ocena modelu
SVC_accuracy = accuracy_score(y_test, y_pred)
SVC_recall = recall_score(y_test, y_pred)
SVC_precision = precision_score(y_test, y_pred)
SVC_f1 = f1_score(y_test, y_pred)

print("\nOcena modelu:")
print("Dokładność (Accuracy):", SVC_accuracy)
print("Czułość (Recall):", SVC_recall)
print("Precyzja (Precision):", SVC_precision)
print("Wynik F1 (F1 Score):", SVC_f1)


# In[15]:


# Model drzewa decyzyjnego
print('GradientBoostingClassifier')

# Przygotowanie danych wejściowych i wyjściowych: wykluczamy kolumny: 'churn', 'churn_encoded' i 'id'
X = df_standard.drop(columns=['churn', 'churn_encoded', 'id'])

# Skalowanie danych
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Podział na zestaw treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Inicjalizacja Gradient Boosting Classifier
GBC_model = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
    max_depth=1, random_state=0)

# Walidacja krzyżowa
GBC_cross_val_scores = cross_val_score(
    GBC_model, X_train, y_train, cv=5, scoring='accuracy')
print("Średnia dokładność z walidacji krzyżowej:", GBC_cross_val_scores.mean())

# Uczenie modelu
GBC_model.fit(X_train, y_train)

# Predykcja na zbiorze testowym
y_pred = GBC_model.predict(X_test)

# Ocena modelu
GBC_accuracy = accuracy_score(y_test, y_pred)
GBC_recall = recall_score(y_test, y_pred)
GBC_precision = precision_score(y_test, y_pred)
GBC_f1 = f1_score(y_test, y_pred)

print("\nOcena modelu:")
print("Dokładność (Accuracy):", GBC_accuracy)
print("Czułość (Recall):", GBC_recall)
print("Precyzja (Precision):", GBC_precision)
print("Wynik F1 (F1 Score):", GBC_f1)


# In[ ]:


print('PORÓWNANIE MODELI:')

# Dane wyników dla każdego modelu
data = {
    "Model": ["RandomForestClassifier", "LogisticRegression", "Support Vector Classifier", "GradientBoostingClassifier"],
    "Cross-Validation Accuracy Mean": [RFC_cross_val_scores, LR_cross_val_scores, SVC_cross_val_scores, GBC_cross_val_scores],
    "Accuracy": [RFC_accuracy, LR_accuracy, SVC_accuracy, GBC_accuracy],
    "Recall": [RFC_recall, LR_recall, SVC_recall, GBC_recall],
    "Precision": [RFC_precision, LR_precision, SVC_precision,  GBC_precision],
    "F1 Score": [RFC_f1, LR_f1, SVC_f1, GBC_f1]
}


# Tworzenie DataFrame z danymi
df_results = pd.DataFrame(data)

# # Wyświetlenie tabeli wyników
print("Tabela wyników:")
print(df_results)

# Wyświetlenie tabeli z liniami oddzielającymi wiersze i kolumny
# print(tabulate(df_results, headers="keys", tablefmt="grid"))

# Utworzenie wykresu słupkowego dla każdej z miar
metrics = ["Accuracy", "Recall", "Precision", "F1 Score"]
df_metrics = df_results.melt(id_vars="Model", value_vars=metrics, var_name="Metric", value_name="Score")

plt.figure(figsize=(12, 8))
for i, metric in enumerate(metrics, 1):
    plt.subplot(2, 2, i)
    subset = df_metrics[df_metrics["Metric"] == metric]
    plt.bar(subset["Model"], subset["Score"], color=["skyblue", "salmon", "lightgreen", "purple"])
    plt.title(metric)
    plt.ylim(0, 1)
    plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

