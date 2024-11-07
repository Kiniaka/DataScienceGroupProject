# Użycie obrazu bazowego Pythona
FROM python:3.10-slim

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Skopiowanie pliku requirements.txt do katalogu roboczego
COPY requirements.txt /app/requirements.txt

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiowanie katalogu templates i pozostałych plików aplikacji do kontenera
COPY model_random_forest.pkl /app/model_random_forest.pkl
COPY templates /app/templates
COPY . /app

# Skopiowanie skryptu startowego
COPY start.sh /app/start.sh

# Ustawienie skryptu jako komendy startowej
CMD ["./start.sh"]
