#!/bin/bash
# Wyświetlenie adresu aplikacji
echo "Aplikacja działa pod adresem: http://127.0.0.1:8000"
# Uruchomienie serwera Uvicorn dla aplikacji FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

