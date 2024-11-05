from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
import joblib
import pandas as pd

# Ładowanie modelu i skalera
loaded = joblib.load('model_random_forest.pkl')
model = loaded['model']
scaler = loaded['scaler']

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Definiowanie modelu danych wejściowych


class ClientData(BaseModel):
    is_tv_subscriber: int
    is_movie_package_subscriber: int
    subscription_age: float
    bill_avg: float
    reamining_contract: float
    service_failure_count: int
    download_avg: float
    upload_avg: float
    download_over_limit: int


@app.get("/form", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/predict_churn", response_class=HTMLResponse)
async def predict_churn(
    request: Request,
    is_tv_subscriber: int = Form(...),
    is_movie_package_subscriber: int = Form(...),
    subscription_age: float = Form(...),
    bill_avg: float = Form(...),
    reamining_contract: float = Form(...),
    service_failure_count: int = Form(...),
    download_avg: float = Form(...),
    upload_avg: float = Form(...),
    download_over_limit: int = Form(...)
):
    try:
        # Przetwarzanie danych wejściowych
        input_data = np.array([
            is_tv_subscriber,
            is_movie_package_subscriber,
            subscription_age,
            bill_avg,
            reamining_contract,
            service_failure_count,
            download_avg,
            upload_avg,
            download_over_limit
        ]).reshape(1, -1)

        # Skalowanie danych
        input_data_scaled = scaler.transform(input_data)

        # Predykcja prawdopodobieństw
        probabilities = model.predict_proba(input_data_scaled)
        prob_churn = probabilities[0][1]
        prob_stay = probabilities[0][0]

        # Zwrócenie wyniku
        return templates.TemplateResponse("result.html", {
            "request": request,
            "probability_stay": f"{prob_stay:.2f}",
            "probability_churn": f"{prob_churn:.2f}"
        })

    except Exception as e:
        print(f"Błąd: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})
