from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
import joblib
import os

# Inicjalizacja aplikacji FastAPI i ustawienie katalogu szablonów
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Sprawdzenie ścieżki do modelu w zależności od środowiska
if os.path.exists('model_random_forest.pkl'):
    model_path = 'model_random_forest.pkl'
elif os.path.exists('/app/model_random_forest.pkl'):
    model_path = '/app/model_random_forest.pkl'
else:
    model_path = None

model, scaler = None, None

# Wczytanie modelu i skalera, jeśli plik istnieje
if model_path:
    try:
        loaded = joblib.load(model_path)
        model = loaded.get('model')
        scaler = loaded.get('scaler')
    except EOFError:
        print("Błąd: Plik modelu jest uszkodzony lub niekompletny.")
else:
    print("Błąd: Plik model_random_forest.pkl nie został znaleziony.")

# Definicja modelu danych wejściowych z użyciem Pydantic
class ClientData(BaseModel):
    is_tv_subscriber: int
    is_movie_package_subscriber: int
    subscription_age: float
    bill_avg: float
    remaining_contract: float
    service_failure_count: int
    download_avg: float
    upload_avg: float
    download_over_limit: int

# Trasa główna przekierowująca do formularza
@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/form")

# Trasa do wyświetlenia formularza wejściowego dla przewidywania rezygnacji
@app.get("/form", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Trasa do obsługi przesyłania formularza i przewidywania prawdopodobieństwa rezygnacji
@app.post("/predict_churn", response_class=HTMLResponse)
async def predict_churn(
    request: Request,
    is_tv_subscriber: int = Form(...),
    is_movie_package_subscriber: int = Form(...),
    subscription_age: float = Form(...),
    bill_avg: float = Form(...),
    remaining_contract: float = Form(...),
    service_failure_count: int = Form(...),
    download_avg: float = Form(...),
    upload_avg: float = Form(...),
    download_over_limit: int = Form(...)
):
    # Sprawdzenie dostępności modelu i skalera przed kontynuacją
    if model is None or scaler is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Model lub skaler jest niedostępny. Sprawdź plik modelu."
        })

    try:
        # Przygotowanie i skalowanie danych wejściowych
        input_data = np.array([
            is_tv_subscriber,
            is_movie_package_subscriber,
            subscription_age,
            bill_avg,
            remaining_contract,
            service_failure_count,
            download_avg,
            upload_avg,
            download_over_limit
        ]).reshape(1, -1)

        input_data_scaled = scaler.transform(input_data)

        # Przewidywanie prawdopodobieństw rezygnacji i pozostania
        probabilities = model.predict_proba(input_data_scaled)
        prob_churn = probabilities[0][1]
        prob_stay = probabilities[0][0]

        # Zwrócenie wyniku do szablonu result.html
        return templates.TemplateResponse("result.html", {
            "request": request,
            "probability_stay": f"{prob_stay:.2f}",
            "probability_churn": f"{prob_churn:.2f}"
        })

    except Exception as e:
        print(f"Błąd: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Wystąpił błąd podczas przewidywania. Spróbuj ponownie."
        })

if __name__ == "__main__":
    import uvicorn
    print("Aplikacja działa pod adresem: http://127.0.0.1:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
