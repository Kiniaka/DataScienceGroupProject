FROM python:3.10-slim

# Ustawienie katalogu roboczego wewnątrz kontenera
WORKDIR /app

# Skopiowanie plików aplikacji do katalogu roboczego
COPY . /app

# Zainstalowanie zależności z requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Eksponowanie portu, na którym działa aplikacja
EXPOSE 8080

# Polecenie do uruchomienia aplikacji FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]