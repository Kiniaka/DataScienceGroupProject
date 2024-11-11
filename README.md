## "Aplikacja FastAPI do Predykcji Rezygnacji Klienta"

## "Opis projektu":
Aplikacja FastAPI, która przewiduje prawdopodobieństwo rezygnacji klienta na podstawie danych o subskrypcji i historii użytkowania. Wyniki są generowane na podstawie modelu uczenia maszynowego wczytanego z pliku model_random_forest.pkl.

## "Wymagania":

Python 3.7 lub nowszy

FastAPI

Uvicorn==0.22.0

scikit-learn==1.5.2

joblib==1.4.2

numpy==1.26.4

pandas==2.2.2

python-multipart

jinja2==3.1.2 (do szablonów HTML)

## "Instalacja":
"Sklonuj repozytorium":

"Skopiuj code" lub go wpisz:

git clone https://github.com/Kiniaka/DataScienceGroupProject.git

## "Wejdź do odpowiedniego katalogu":

"Skopiuj code" lub go wpisz:

cd DataScienceGroupProject

## "Zainstaluj wymagane pakiety":

"Skopiuj code" lub go wpisz:

pip install -r requirements.txt

## "Uruchamianie aplikacji":
Upewnij się, że serwer jest uruchomiony w środowisku zdefiniowanym w .env.

"Uruchom aplikację za pomocą Uvicorn":

"Skopiuj code" lub go wpisz:

uvicorn main:app --reload --port 8000

"lub użyj Docker Compose":

"Skopiuj code" lub go wpisz:

docker-compose up --build

Otwórz przeglądarkę i przejdź na adres: http://127.0.0.1:8000/form

## Użycie":

Wprowadź dane klienta w formularzu dostępnym pod /form.
Po przesłaniu danych wyświetli się prawdopodobieństwo pozostania (probability_stay) oraz prawdopodobieństwo rezygnacji (probability_churn).

## Zmienne środowiskowe":

Zdefiniuj zmienne środowiskowe w pliku .env zgodnie z poniższym wzorcem:
plaintext

"Skopiuj code" lub go wpisz:

MODEL_PATH=model_random_forest.pkl

PORT=8000

DEBUG=True

Uwagi: Umieść model model_random_forest.pkl w katalogu projektu. Plik powinien zawierać wytrenowany model Random Forest oraz skaler, zapisane w formacie:
python

"Skopiuj code" lub go wpisz:

{'model': trained_model, 'scaler': scaler}

## "Code Review":

"main.py"

Kod zapisuje model i skaler za pomocą joblib.dump oraz ładuje je, jeśli plik istnieje. Zapewnia to gotowość modelu do użycia.
Kod sprawdza ścieżkę modelu w dwóch lokalizacjach: lokalnej i /app, co umożliwia działanie zarówno lokalnie, jak i w środowisku produkcyjnym.
ClientData definiuje dane wejściowe jako model Pydantic, co zapewnia walidację typów i upraszcza obsługę danych wejściowych.
Kod przetwarza dane wejściowe w predict_churn, skalując je przed dokonaniem predykcji, co zapewnia spójność w danych wejściowych dla modelu.
Błędy są drukowane do konsoli, a użytkownik jest przekierowywany na stronę błędu (error.html) w razie problemu.
Kod korzysta z templates.TemplateResponse do renderowania wyników i przekazuje wartości prawdopodobieństwa.
Statyczne zasoby są poprawnie montowane w katalogu templates, co ułatwia dostęp do plików statycznych.

"Wczytywanie danych i wstępne sprawdzenia":

Kod ładuje zestaw danych i wykonuje podstawowe sprawdzenia (head, info, describe oraz sprawdzenie braków danych).
Zalety: Dobre, początkowe analizy eksploracyjne.
Sugestia: Warto logować te sprawdzenia zamiast drukować, aby utrzymać porządek w kodzie.

"Uzupełnianie braków danych i normalizacja":

Braki danych są uzupełniane średnią kolumny po przeprowadzeniu normalizacji.
Obserwacja: Kolumny z NaN są najpierw normalizowane, co może prowadzić do niekonsekwencji w interpretacji. Uzupełnienie wartości przed normalizacją dałoby bardziej interpretowalne wyniki.

"Testy statystyczne (Shapiro-Wilka)":
Na każdej kolumnie przeprowadzane są testy normalności.
Obserwacja: Testy normalności przy dużych zbiorach mogą być kosztowne obliczeniowo.
Sugestia: Rozważ użycie wizualizacji, takich jak wykresy Q-Q, w dużych zbiorach danych.

"Macierz korelacji":

Generowana jest macierz korelacji, wizualizowana za pomocą heatmap.
Zalety: Przydatna do analizy relacji między zmiennymi.
Uwaga: Duże macierze mogą być przytłaczające – warto wyświetlać jedynie istotne korelacje.

"import_from_ipynb" i tymczasowy plik:

Funkcja import_from_ipynb załadowuje notebook (.ipynb), konwertuje go na kod Python i importuje jako moduł, umożliwiając pobranie zmiennej.
Zalety: Pozwala na automatyczne przenoszenie zmiennych z notebooka.
Sugestia: Dodaj obsługę wyjątków na wypadek, gdyby zmienna nie istniała w notebooku.
Tymczasowy plik: '_tmp_notebook_code.py' jest praktyczny, ale warto dodać jego czyszczenie po zakończeniu pracy.

"start.sh"

Komunikat informacyjny: Wyświetla informację o oczekiwaniu na start aplikacji.
Uruchomienie Uvicorn: Skrypt uruchamia serwer na porcie 8000 i nasłuchuje na 0.0.0.0.
Sugestia: W środowisku produkcyjnym nasłuchiwanie na 0.0.0.0 może być ryzykowne – warto chronić je dodatkowo np. zaporą.

## "Gotowy szablon README zawiera wszystkie informacje potrzebne do zrozumienia, uruchomienia i ocenienia aplikacji, a także zapewnia dokładny przegląd kodu oraz kluczowe sugestie ulepszające jego funkcjonalność".
