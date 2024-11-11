## Aplikacja FastAPI do Predykcji Rezygnacji Klienta

## Opis projektu

Aplikacja FastAPI, która przewiduje prawdopodobieństwo rezygnacji klienta na podstawie danych o subskrypcji i historii użytkowania. Wyniki wyświetlane są na podstawie modelu uczenia maszynowego, wczytanego z pliku model_random_forest.pkl.

## Wymagania

- Python 3.7 lub nowszy,
- FastAPI,
- Uvicorn==0.22.0,
- scikit-learn==1.5.2,
- joblib==1.4.2,
- numpy==1.26.4,
- pandas==2.2.2,
- python-multipart,
- jinja2==3.1.2 (do szablonów HTML).

## Instalacja

1. Sklonuj repozytorium:

   git clone https://github.com/Kiniaka/DataScienceGroupProject.git

2. Wejdz w comend line do odpowiedniego katalogu:

   cd DataScienceGroupProject

3. Zainstaluj wymagane pakiety:

   pip install -r requirements.txt

## Uruchamianie aplikacji

1. Upewnij się, że serwer jest uruchomiony w środowisku zdefiniowanym w `.env`.
2. Uruchom aplikację za pomocą Uvicorn:
    ```bash
    uvicorn main:app --reload --port 8000
lub"
    docker-compose up --build"        
    ```

3. Otwórz przeglądarkę i przejdź na adres: [http://127.0.0.1:8000/form].

## Użycie
- Wprowadź dane klienta w formularzu dostępnym pod `/form`.
- Po przesłaniu danych wyświetli się prawdopodobieństwo pozostania (`probability_stay`) oraz prawdopodobieństwo rezygnacji (`probability_churn`).

## Zmienne środowiskowe
Zdefiniuj zmienne środowiskowe w pliku `.env` zgodnie z poniższym wzorcem:
```dotenv
MODEL_PATH=model_random_forest.pkl
PORT=8000
DEBUG=True


Umieść model model_random_forest.pkl w katalogu projektu. Plik ten powinien zawierać wytrenowany model Random Forest oraz skaler, zapisany w formacie:

{'model': trained_model, 'scaler': scaler}

Upewnij się, że plik .env zawiera wymagane zmienne środowiskowe

## Kod Review
main.py
Kod zapisuje model i skaler za pomocą "joblib.dump" oraz ładuje je, jeśli plik istnieje. To zapewnia, że model jest gotowy do użycia.
Kod sprawdza ścieżkę modelu w dwóch lokalizacjach: lokalnej i /app. To jest odpowiednie, jeśli model może być w różnych miejscach, np. w środowisku produkcyjnym lub lokalnym.
"ClientData" definiuje dane wejściowe jako model Pydantic, co zapewnia walidację typów i uproszcza obsługę danych wejściowych.
Kod przetwarza dane wejściowe w "predict_churn", skalując je przed dokonaniem predykcji. Skorzystanie z scaler.transform pozwala na spójność w danych wejściowych dla modelu.
Błędy są drukowane do konsoli, ale nie ma dedykowanej obsługi błędów dla użytkownika. Strona błędu (error.html) jest wyświetlana w przypadku problemu.
Kod używa templates.TemplateResponse do renderowania wyników i przekazuje wartości prawdopodobieństwa.
Kod poprawnie montuje zasoby statyczne w katalogu templates, co ułatwia dostęp do plików statycznych.

## Ładowanie danych i wstępne sprawdzenia:
Kod ładuje zestaw danych i wykonuje podstawowe sprawdzenia (head, info, describe oraz sprawdzenie braków danych), aby zrozumieć strukturę i jakość danych.
Zalety: Dobre, początkowe analizy eksploracyjne.
Sugestia: Zamiast drukować, warto logować te sprawdzenia, aby utrzymać porządek w notatniku/skrypcie.

## Uzupełnianie braków danych i normalizacja:
Braki danych są uzupełniane średnią kolumny po przeprowadzeniu normalizacji.
Zalety: Logiczne podejście do uzupełniania braków w kolumnach numerycznych.
Obserwacja: Kolumny z NaN są najpierw normalizowane, a potem uzupełniane, co może prowadzić do niekonsekwencji w interpretacji statystycznej. Uzupełnienie wartości przed normalizacją mogłoby dać bardziej interpretowalne wyniki.

## Testy statystyczne (Shapiro-Wilka):
Na każdej kolumnie przeprowadzane są testy normalności, a wyniki są drukowane.
Obserwacja: Testy normalności na tak dużych zestawach danych mogą być kosztowne obliczeniowo i mogą pokazywać niskie wartości "p" z powodu dużego rozmiaru próby.
Sugestia: Rozważ użycie wizualizacji (jak wykresy Q-Q) do oceny normalności w dużych zbiorach danych.

## Macierz korelacji:
Generowana jest macierz korelacji, która jest wizualizowana za pomocą heatmapy.
Zalety: Przydatne, aby zrozumieć relacje między zmiennymi.
Uwaga: Duże macierze mogą być przytłaczające. Rozważ wykres korelacji tylko dla istotnych zależności.

## Kodowanie danych:
Kolumna churn jest kodowana i mapowana na etykiety (pozostaje i odchodzi).
Zalety: Czyni wyniki bardziej zrozumiałymi.
Poprawa: Upewnij się, że mapowanie etykiet jest zgodne z celami analizy (np. spójne etykietowanie w raportach ewaluacyjnych).

## Modelowanie - Walidacja krzyżowa, trenowanie i ewaluacja:
Zalety: Modele są trenowane, walidowane krzyżowo i oceniane przy użyciu kluczowych miar (dokładność, czułość, precyzja, F1 score).
Atuty: Kompleksowa ewaluacja z wieloma klasyfikatorami (Random Forest, Regresja Logistyczna, SVM, Gradient Boosting).
Ulepszenie: Rozdzielenie sekcji modelowania na funkcje dla każdego modelu poprawiłoby modularność kodu.

## Porównanie modeli i wizualizacja:
Generowana jest tabela porównawcza i wykresy słupkowe, aby pokazać wyniki modeli.
Zalety: Świetne do wizualnej oceny i porównania wyników modeli.
Sugestia: Kolory słupków można uprościć dla lepszej czytelności.

##Podsumowanie
Kod obejmuje pełen proces przygotowania danych, modelowania i ewaluacji. Organizacja przepływu pracy w modularne funkcje oraz optymalizacja obliczeniowo kosztownych operacji poprawiłaby czytelność i wydajność kodu.

"import_from_ipynb":
Funkcja import_from_ipynb załadowuje notebook (.ipynb), konwertuje go na kod Python, zapisuje do tymczasowego pliku i importuje jako moduł, umożliwiając pobranie zmiennej o nazwie var_name.
Zalety:
Umożliwia załadowanie zmiennych z Jupyter Notebook bez potrzeby ręcznego kopiowania kodu.
Wykorzystanie nbconvert i nbformat do automatyzacji konwersji notebooka na kod Python jest pomysłowe i efektywne.
Sugestia:
Funkcja może być podatna na błędy, jeśli notebook Project3.ipynb nie zawiera zmiennej var_name. Warto dodać obsługę wyjątków na wypadek, gdyby zmienna var_name nie istniała.
## Tymczasowy plik '_tmp_notebook_code.py':
Plik '_tmp_notebook_code.py' jest używany jako tymczasowy bufor dla kodu przekonwertowanego z notebooka.
Obserwacja:
Użycie tymczasowego pliku jest praktyczne, ale warto dodać czyszczenie tego pliku po zakończeniu pracy, aby uniknąć zaśmiecania projektu.
Sugestia:
Rozważ zastosowanie bibliotek takich jak tempfile do dynamicznego tworzenia i usuwania plików tymczasowych w bezpieczny sposób.
## Załadowanie model i scaler:
Funkcja jest używana do załadowania zmiennych model i scaler z notebooka Project3.ipynb.
Zalety: Pozwala łatwo przenosić modele między różnymi środowiskami (np. notebook i skrypty Python).
Sugestia: Upewnij się, że notebook Project3.ipynb jest spójny z tym skryptem, aby uniknąć potencjalnych błędów przy zmianie ścieżek lub nazw zmiennych.
## Ogólne uwagi:
Obsługa błędów: Warto rozważyć dodanie obsługi wyjątków przy wczytywaniu notebooka i importowaniu zmiennych, co poprawi stabilność kodu.
Wydajność: Załadowanie całego notebooka do pobrania jednej lub dwóch zmiennych może być nadmiarowe. Jeśli model i skaler są często aktualizowane, może warto rozważyć zapisanie ich bezpośrednio do pliku (np. .pkl) zamiast ładowania z notebooka.

"trenuj_model.py" 
## Funkcja import_from_ipynb:
Funkcja import_from_ipynb załadowuje notebook (.ipynb), konwertuje go na kod Python, zapisuje do tymczasowego pliku i importuje jako moduł, umożliwiając pobranie zmiennej o nazwie var_name.
Zalety:
Umożliwia załadowanie zmiennych z Jupyter Notebook bez potrzeby ręcznego kopiowania kodu.
Wykorzystanie nbconvert i nbformat do automatyzacji konwersji notebooka na kod Python jest pomysłowe i efektywne.
Sugestia:
Funkcja może być podatna na błędy, jeśli notebook Project3.ipynb nie zawiera zmiennej var_name. Warto dodać obsługę wyjątków na wypadek, gdyby zmienna var_name nie istniała.

## Tymczasowy plik '_tmp_notebook_code.py':
Plik '_tmp_notebook_code.py' jest używany jako tymczasowy bufor dla kodu przekonwertowanego z notebooka.
Obserwacja:
Użycie tymczasowego pliku jest praktyczne, ale warto dodać czyszczenie tego pliku po zakończeniu pracy, aby uniknąć zaśmiecania projektu.
Sugestia:
Rozważ zastosowanie bibliotek takich jak tempfile do dynamicznego tworzenia i usuwania plików tymczasowych w bezpieczny sposób.

## Załadowanie model i scaler:
Funkcja jest używana do załadowania zmiennych model i scaler z notebooka Project3.ipynb.
Zalety: Pozwala łatwo przenosić modele między różnymi środowiskami (np. notebook i skrypty Python).
Sugestia: Upewnij się, że notebook Project3.ipynb jest spójny z tym skryptem, aby uniknąć potencjalnych błędów przy zmianie ścieżek lub nazw zmiennych.
## Ogólne uwagi:
Obsługa błędów: Warto rozważyć dodanie obsługi wyjątków przy wczytywaniu notebooka i importowaniu zmiennych, co poprawi stabilność kodu.
Wydajność: Załadowanie całego notebooka do pobrania jednej lub dwóch zmiennych może być nadmiarowe. Jeśli model i skaler są często aktualizowane, może warto rozważyć zapisanie ich bezpośrednio do pliku (np. .pkl) zamiast ładowania z notebooka.

"start.sh"

## Komunikat Informacyjny":
Skrypt wyświetla informację dla użytkownika o oczekiwaniu na uruchomienie aplikacji (Application startup complete) oraz adresie aplikacji.
Zalety: Przydatne dla użytkownika, aby wiedział, kiedy aplikacja jest gotowa.

## Uruchomienie Serwera Uvicorn":
Skrypt uruchamia serwer Uvicorn dla aplikacji FastAPI na porcie 8000 i nasłuchuje na wszystkich interfejsach (0.0.0.0).
Zalety: Umożliwia dostęp do aplikacji zarówno lokalnie, jak i z innych urządzeń w tej samej sieci.
Uwaga Bezpieczeństwa: W środowisku produkcyjnym nasłuchiwanie na 0.0.0.0 może być ryzykowne, jeśli nie jest chronione innymi mechanizmami zabezpieczeń (np. zaporą sieciową).

## Uwagi Dodatkowe:
Optymalizacja: Skrypt jest minimalny i dobrze spełnia swoją rolę. Nie wymaga dodatkowych usprawnień.
Obsługa Błędów: Można rozważyć dodanie sprawdzenia, czy uvicorn jest dostępny w środowisku, aby uniknąć problemów w przypadku braku zainstalowanego serwera.

