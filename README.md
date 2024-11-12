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

{'model': tranuj_model, 'scaler': scaler}

## "Code Review":

## "main.py":

## "Importy i Konfiguracja Środowiska":

Importowane są kluczowe biblioteki, takie jak FastAPI do stworzenia API, Jinja2Templates do renderowania szablonów HTML, oraz joblib do zapisu i odczytu modelu.

## "Zapis Modelu i Skalera":

"joblib.dump()":

zapisuje model oraz skalera do jednego pliku (model_random_forest.pkl). To pozwala na łatwe wczytywanie obu elementów w kolejnych etapach aplikacji. Dobre rozwiązanie, szczególnie gdy model i skaler muszą być współdzielone między różnymi aplikacjami lub środowiskami.

## "Ścieżka do Modelu":

Kod sprawdza, czy plik model_random_forest.pkl znajduje się lokalnie lub na ścieżce /app/model_random_forest.pkl. To dobre rozwiązanie na wypadek różnych ścieżek w środowisku lokalnym i produkcyjnym.

Sekcja ładowania modelu i skalera jest zaprojektowana, lecz warto dodać lepszą obsługę błędów, np. logowanie błędów, aby ułatwić diagnozę w przypadku problemów.

"Obsługa Plików Statycznych":

Aplikacja montuje katalog templates jako zasoby statyczne. Jest to przydatne, jeśli w folderze templates znajdują się pliki CSS lub obrazy, jednak może być mylące, ponieważ zwykle pliki statyczne są oddzielone od szablonów HTML.

"Definicja Modelu Danych ClientData":

Model ClientData oparty na Pydantic definiuje wszystkie atrybuty wymagane do prognozowania rezygnacji klienta. Dzięki temu aplikacja sprawdza poprawność danych wejściowych, co poprawia bezpieczeństwo i stabilność.

"Trasy API":

"/form (GET)"

Wyświetla formularz form.html, który umożliwia użytkownikowi wprowadzenie danych klienta.Użycie Jinja2Templates do renderowania szablonu jest dobrym rozwiązaniem.

"/predict_churn (POST)

Główna trasa do prognozowania rezygnacji na podstawie wprowadzonych danych.

"Przetwarzanie Danych i Predykcja":

"Przetwarzanie danych":

Dane wejściowe są konwertowane na numpy array, co umożliwia ich dalsze skalowanie i przetwarzanie.

"Skalowanie danych":

Dane są skalowane za pomocą wcześniej zapisanego scaler, co gwarantuje, że format danych będzie zgodny z tym, na którym trenowano model.

"Predykcja":

Kod wykonuje predykcję prawdopodobieństw rezygnacji (churn) i pozostania (stay), a następnie przekazuje je do result.html w celu wyświetlenia użytkownikowi.
Obsługa błędów w tej sekcji jest podstawowa – wyjątki są logowane do konsoli, ale warto rozważyć bardziej szczegółowe raportowanie błędów do pliku logów.

"Przekierowanie":

Trasa główna / przekierowuje do formularza form, co zapewnia intuicyjny dostęp dla użytkownika zaraz po otwarciu aplikacji.

## "Wnioski i Sugestie"

"Pliki statyczne":

Warto umieścić pliki statyczne (CSS, obrazy) w osobnym katalogu static zamiast w templates. Obecna struktura może powodować dezorientację.

"Obsługa błędów":

Rozbudowanie obsługi błędów o logowanie do plików lub systemu monitoringu może pomóc w śledzeniu ewentualnych problemów w produkcji.

"Dokumentacja":

Dodanie komentarzy do każdej funkcji oraz przykładów, jak używać API, poprawiłoby czytelność kodu.
Ogólnie kod jest dobrze zaprojektowany i zapewnia wszystkie niezbędne funkcjonalności, aby użytkownik mógł wprowadzić dane i uzyskać wynik prognozy rezygnacji klienta.

## "Project3.jpynb"

"Wczytywanie Danych i Wstępna Analiza":

Wczytanie danych oraz ich podstawowa analiza za pomocą funkcji (head, info, describe, isnull) dostarczają kluczowych informacji o strukturze, kompletności i podstawowych statystykach danych. To dobre, pierwsze kroki, aby zrozumieć właściwości zbioru danych.

## "Wizualizacja Histogramów":

Histogramy dają wizualne podsumowanie rozkładu dla każdej zmiennej. To cenne dla wychwycenia asymetrii, potencjalnych wartości odstających i ogólnego rozkładu danych.

## "Standaryzacja i Imputacja (uzupełnianie braków)":

Standaryzacja jest stosowana do kolumn z brakującymi wartościami, a następnie wartości są uzupełniane średnią kolumny. Chociaż jest to efektywne, optymalnym rozwiązaniem byłoby najpierw uzupełnienie braków, a dopiero potem standaryzacja, co da bardziej spójne statystycznie dane.
Końcowe sprawdzenie na obecność braków danych zapewnia, że wszystkie braki zostały uzupełnione, co przygotowuje dane do dalszych analiz.

## "Test Shapiro-Wilka i Wykresy Q-Q":

Test Shapiro-Wilka oraz wykresy Q-Q dla każdej kolumny pomagają ocenić normalność rozkładu danych. Wyjście wskazuje, że większość kolumn nie spełnia założeń normalności (niski poziom p), co sugeruje, że dane mogą wymagać nieliniowych modeli lub przekształceń dla lepszego dopasowania.

Wykresy Q-Q wizualizują odchylenia od rozkładu normalnego i są dobrym uzupełnieniem dla testu Shapiro-Wilka.

## "Percentyle":

Obliczenie percentyli (25%, 50%, 75%) dla kluczowych zmiennych daje informacje o rozkładzie wartości. Może to pomóc w identyfikacji wartości odstających oraz w dalszych analizach rozkładu.

## "Macierz Korelacji":

Macierz korelacji pozwala zidentyfikować zależności pomiędzy zmiennymi, co jest istotne dla zrozumienia współzależności w zbiorze danych.
Wykres heatmap dobrze przedstawia korelacje między zmiennymi i sugeruje potencjalne redundancje lub ważne zależności do dalszej analizy.

## "Kodowanie Zmiennych":

Kolumna churn jest zakodowana za pomocą LabelEncoder, a etykiety numeryczne są zamienione na tekstowe ("pozostaje" i "odchodzi"), co ułatwia interpretację wyników i przyszłe wizualizacje.

## "Budowa i Ocena Modeli":

Random Forest, Regresja Logistyczna, SVC, i Gradient Boosting są używane do modelowania i prognozowania rezygnacji klientów.
Każdy model jest oceniany pod kątem średniej dokładności z walidacji krzyżowej, co daje obiektywną miarę wydajności na zbiorze treningowym.
Modele są oceniane za pomocą kluczowych metryk: Accuracy (dokładność), Recall (czułość), Precision (precyzja) oraz F1 Score. Przedstawione wyniki pozwalają zidentyfikować, które modele najlepiej nadają się do przewidywania rezygnacji klientów.

## "Porównanie Modeli":

Tworzenie tabeli i wykresów słupkowych dla metryk porównuje skuteczność modeli. To efektywne podejście, które wizualnie ukazuje mocne i słabe strony każdego modelu w różnych metrykach.

## "Podsumowanie":

Kolejne kroki prowadzą od wstępnej eksploracji i przygotowania danych do pełnej budowy i ewaluacji modeli. Sugestią może być wcześniejsze uzupełnianie braków danych przed standaryzacją oraz ewentualne przekształcenie nienormalnych zmiennych dla lepszego dopasowania modeli.

## "start.sh"

"Komunikat informacyjny":

Wyświetla informację o oczekiwaniu na start aplikacji.

"Uruchomienie Uvicorn":

Skrypt uruchamia serwer na porcie 8000 i nasłuchuje na 0.0.0.0.

"Sugestia":

W środowisku produkcyjnym nasłuchiwanie na 0.0.0.0 może być ryzykowne – warto chronić je dodatkowo np. zaporą.

## "trenuj_model.py":

Kod trenuj_model.py jest skryptem, który umożliwia importowanie zmiennych z notebooka Jupyter (.ipynb) do pliku .py. Jest to przydatne w scenariuszach, gdzie model i obiekty takie jak scaler są zdefiniowane i trenowane w notebooku, ale potrzebne są w innych skryptach lub aplikacjach.

## "Struktura kodu":

"Importy i Wstępne Konfiguracje":

Importowane są moduły 'nbconvert' i 'nbformat' do konwersji notebooków do formatu Python, 'joblib' do ładowania/zapisu modelu oraz 'StandardScaler' z 'sklearn.preprocessing'.
Te importy są zgodne z funkcjonalnością skryptu i pozwalają na przetwarzanie i konwersję kodu z notebooka.

"Funkcja" 'import_from_ipynb':

"Cel":

Funkcja import_from_ipynb umożliwia załadowanie określonej zmiennej z notebooka .ipynb.

"Kroki w funkcji":

"Załadowanie notebooka":

Notebook jest otwierany i czytany za pomocą 'nbformat.read'.

"Konwersja notebooka do kodu Python":

Używając PythonExporter, konwertuje notebook na kod źródłowy w Pythonie.
Zapis kodu Python do tymczasowego pliku: Kod jest zapisywany w pliku tymczasowym (_tmp_notebook_code.py), co umożliwia jego załadowanie jako moduł w Pythonie.
Załadowanie modułu: Plik tymczasowy jest ładowany jako moduł za pomocą importlib.
Pobranie zmiennej: Z funkcji zwracana jest konkretna zmienna z notebooka, która została zdefiniowana w var_name.
Funkcja jest zwięzła i dobrze przemyślana – pozwala na elastyczne ładowanie dowolnej zmiennej z notebooka.

"Importowanie model i scaler z notebooka":

Kod importuje zmienne model oraz scaler z notebooka Project3.ipynb. Te zmienne są później dostępne w skrypcie i mogą być wykorzystane do dalszych operacji, np. trenowania modelu lub skalowania danych.
Importowanie jest dobrze przemyślane, jednak zależność od tymczasowego pliku _tmp_notebook_code.py może być wrażliwa na ewentualne konflikty plików w systemie. Można rozważyć generowanie losowych nazw dla tymczasowych plików, aby uniknąć konfliktów.

"Sugestie":

"Obsługa błędów":

Warto dodać blok try-except wewnątrz funkcji import_from_ipynb, aby wykrywać błędy związane z nieprawidłowym formatem notebooka lub brakiem zmiennej.

"Wydajność i sprzątanie plików": 

Po załadowaniu zmiennych można rozważyć usunięcie tymczasowego pliku _tmp_notebook_code.py, aby uniknąć pozostawiania zbędnych plików na dysku.


"Dokumentacja":

Dodanie krótkich komentarzy lub docstringów do funkcji import_from_ipynb zwiększyłoby czytelność kodu, szczególnie przy planowaniu, aby inni korzystali z tego skryptu.

"Podsumowanie":

Kod trenuj_model.py, umożliwia efektywne ładowanie zmiennych z notebooka. Jest to przydatny skrypt w sytuacjach, gdy model lub dane są trenowane i przetwarzane w notebookach, ale potrzebne są również w innych plikach.

## "templates"

templates zawiera pliki HTML i CSS potrzebne do obsługi interfejsu użytkownika aplikacji FastAPI. Oto opis zawartości:

"form.html" – Formularz HTML, który umożliwia użytkownikowi wprowadzenie danych wejściowych klienta, takich jak subskrypcje i historia użytkowania. Formularz wysyła dane do serwera w celu przeprowadzenia predykcji.

"result.html" – Szablon HTML wyświetlający wynik predykcji. Prezentuje prawdopodobieństwo pozostania (probability_stay) oraz prawdopodobieństwo rezygnacji (probability_churn) klienta na podstawie wprowadzonych danych.

"error.html" – Szablon strony błędu, który jest wyświetlany, gdy wystąpi problem z przetwarzaniem danych lub działaniem aplikacji. Informuje użytkownika o błędzie i zapewnia, że system nie był w stanie przeprowadzić predykcji. Pomaga użytkownikowi zidentyfikować problem i ewentualnie ponownie spróbować przesłać dane.

"styles.css" – Plik CSS zawierający style dla aplikacji, poprawiające wygląd i układ elementów HTML. Dzięki styles.css formularze, wyniki oraz strony błędów prezentują się estetycznie i są lepiej dostosowane do różnych urządzeń.

## "Uwagi dotyczące templates"
Pliki HTML są renderowane przez FastAPI przy użyciu Jinja2, co umożliwia dynamiczne generowanie treści w odpowiedzi na dane wejściowe użytkownika i wyniki predykcji. Plik styles.css jest włączany do wszystkich szablonów HTML, aby zapewnić spójny styl aplikacji.

## "Dockerfile":

"Obraz bazowy":

FROM python:3.11-slim jest to obraz "slim", więc zajmuje mniej miejsca i przyspiesza pobieranie oraz uruchamianie kontenera.

"Katalog roboczy"

WORKDIR /app ustawia główny katalog roboczy na /app, co jest standardową praktyką, pozwalającą na lepszą organizację plików w kontenerze.
Instalacja zależności

Skopiowanie requirements.txt i instalacja zależności z pip install --no-cache-dir -r requirements.txt jest poprawnym rozwiązaniem.

--no-cache-dir zmniejsza rozmiar obrazu, co jest dobrą praktyką.

"Kopiowanie plików aplikacji"

Plik modelu (model_random_forest.pkl) i folder templates są kopiowane do /app, co jest zgodne z wymaganiami aplikacji.

Linia ADD . /app kopiuje wszystkie pliki do katalogu roboczego, ale warto rozważyć .dockerignore, by uniknąć kopiowania niepotrzebnych plików (np. .git, plików tymczasowych).

"Skrypt startowy"

ADD start.sh /app/start.sh kopiuje skrypt startowy do kontenera, a RUN chmod 777 start.sh nadaje mu pełne prawa.
Zamiast chmod 777, bardziej zalecane jest nadanie uprawnień chmod +x start.sh lub chmod 755 start.sh, co zmniejsza ryzyko naruszenia bezpieczeństwa.

"Eksponowanie portu i uruchamianie aplikacji":

EXPOSE jest zakomentowane, ale jeżeli aplikacja korzysta z określonego portu, dobrze jest go uwidocznić.

Komenda startowa CMD uruchamia start.sh, co jest odpowiednie, jeśli skrypt ten zawiera całą logikę uruchomienia aplikacji.

"Wnioski":

"Aby ulepszyć Dockerfile, można":

Zastosować .dockerignore dla niepotrzebnych plików,

Zmienić chmod 777 na chmod +x dla bezpieczeństwa,

Dodać EXPOSE (jeśli port jest wymagany).

## "docker-compose.yml":

## "Wersja":

Użycie version: "3.8" jest dobrym wyborem, ponieważ jest szeroko wspierane i oferuje wystarczającą elastyczność dla aplikacji typu FastAPI.

##"Usługa app":

"Build":

"context: . i dockerfile": 

Dockerfile wskazują na budowanie obrazu bezpośrednio z pliku Dockerfile w bieżącym katalogu, co jest odpowiednią konfiguracją.

"Nazwa kontenera":

"container_name":

"fastapi_app" określa nazwę kontenera, co jest przydatne do identyfikacji kontenera podczas jego uruchamiania i monitorowania.

"Porty(ports)":

- "8000:8000" mapuje porty hosta i kontenera, umożliwiając dostęp do aplikacji na localhost:8000. To właściwe ustawienie, biorąc pod uwagę domyślną konfigurację FastAPI na porcie 8000.

"Volumes":

- ./model_random_forest.pkl:/app/model_random_forest.pkl udostępnia plik modelu model_random_forest.pkl do użytku w kontenerze, co jest przydatne, jeśli model jest aktualizowany poza kontenerem.

- .:/app udostępnia cały bieżący katalog do /app w kontenerze, co ułatwia rozwój i testowanie, ale w środowisku produkcyjnym lepiej jest ograniczyć to do plików rzeczywiście potrzebnych w kontenerze. Rozważ użycie .dockerignore, by wykluczyć pliki niepotrzebne w środowisku kontenera.

"Env_file":

- .env ładuje zmienne środowiskowe z pliku .env, co jest dobrą praktyką dla lepszej konfiguracji środowiska i bezpieczeństwa.

## "Wnioski":

"docker-compose.yml warto jednak rozważyć":

Wyłączenie udostępniania całego katalogu (- .:/app) na środowisko produkcyjne i użycie .dockerignore dla niepotrzebnych plików.
Przemyślenie, czy plik model_random_forest.pkl jest aktualizowany na tyle często, by wymagał montowania przez volume – jeśli nie, można go kopiować do obrazu.

## "Gotowy szablon README zawiera wszystkie informacje potrzebne do zrozumienia, uruchomienia i ocenienia aplikacji, a także zapewnia dokładny przegląd kodu oraz kluczowe sugestie ulepszające jego funkcjonalność".
