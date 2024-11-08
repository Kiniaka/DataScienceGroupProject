FROM python:3.11-slim

# Ustawienie katalogu roboczego wewnątrz kontenera
WORKDIR /app

# Skopiowanie plików aplikacji do katalogu roboczego
ADD requirements.txt /app/requirements.txt
# Zainstalowanie zależności z requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Eksponowanie portu, na którym działa aplikacja
# EXPOSE 8080

# # Polecenie do uruchomienia aplikacji FastAPI
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Skopiowanie katalogu templates i pozostałych plików aplikacji do kontenera
ADD model_random_forest.pkl /app/model_random_forest.pkl
ADD templates /app/templates
ADD . /app

# Skopiowanie skryptu startowego
ADD start.sh /app/start.sh

#Nadanie uprawnień wykonywalności dla pliku
RUN chmod 777 start.sh

# Ustawienie skryptu jako komendy startowej
CMD ["/bin/bash","./start.sh"]