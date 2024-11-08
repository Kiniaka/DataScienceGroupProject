FROM python:3.11.9

# Ustawienie katalogu roboczego wewnątrz kontenera
WORKDIR /app

# Skopiowanie plików aplikacji do katalogu roboczego
COPY requirements.txt /app/requirements.txt
# Zainstalowanie zależności z requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Eksponowanie portu, na którym działa aplikacja
# EXPOSE 8080

# # Polecenie do uruchomienia aplikacji FastAPI
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Skopiowanie katalogu templates i pozostałych plików aplikacji do kontenera
COPY model_random_forest.pkl /app/model_random_forest.pkl
COPY templates /app/templates
COPY . /app

# Skopiowanie skryptu startowego
COPY start.sh /app/start.sh

# Ustawienie skryptu jako komendy startowej
CMD ["./start.sh"]