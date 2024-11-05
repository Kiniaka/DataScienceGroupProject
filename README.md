## Aplikacja FastAPI do Predykcji Rezygnacji Klienta

## Opis projektu

Aplikacja FastAPI, która przewiduje prawdopodobieństwo rezygnacji klienta na podstawie danych o subskrypcji i historii użytkowania. Wyniki wyświetlane są na podstawie modelu uczenia maszynowego, wczytanego z pliku model_random_forest.pkl.

## Wymagania

Python 3.7 lub nowszy
FastAPI
Uvicorn
scikit-learn
joblib
numpy
pandas
jinja2 (do szablonów HTML)

## Instalacja

1. Sklonuj repozytorium:

   git clone https://github.com/Kiniaka/DataScienceGroupProject.git

2. Wejdz w comend line do ospowiedniego katalogu:

   cd DataScienceGroupProject

3. Zainstaluj wymagane pakiety:

   pip install -r requirements.txt

Umieść model model_random_forest.pkl w katalogu projektu. Plik ten powinien zawierać wytrenowany model Random Forest oraz skaler, zapisany w formacie:

{'model': trained_model, 'scaler': scaler}

Upewnij się, że plik .env zawiera wymagane zmienne środowiskowe
