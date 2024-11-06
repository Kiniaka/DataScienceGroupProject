from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
import joblib
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load the model and scaler
model_path = 'C:/Project/myProject/DataScienceGroupProject/new/model_random_forest.pkl'
if os.path.exists(model_path):
    try:
        loaded = joblib.load(model_path)
        model = loaded.get('model')
        scaler = loaded.get('scaler')
    except EOFError:
        print("Error: model_random_forest.pkl is corrupted or incomplete.")
        model, scaler = None, None
else:
    print("Error: model_random_forest.pkl file not found.")
    model, scaler = None, None


# Define the input data model
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
    # Check if model and scaler are loaded successfully
    if model is None or scaler is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Model or scaler is not available. Please check the model file."
        })

    try:
        # Process input data
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

        # Scale input data
        input_data_scaled = scaler.transform(input_data)

        # Predict probabilities
        probabilities = model.predict_proba(input_data_scaled)
        prob_churn = probabilities[0][1]
        prob_stay = probabilities[0][0]

        # Return result
        return templates.TemplateResponse("result.html", {
            "request": request,
            "probability_stay": f"{prob_stay:.2f}",
            "probability_churn": f"{prob_churn:.2f}"
        })

    except Exception as e:
        print(f"Error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

