from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and encoder
model = joblib.load("final_model.pkl")
airline_encoder = joblib.load("airline_encoder.pkl")


class FlightInput(BaseModel):
    Month: int
    DayOfWeek: int
    Airline: str
    CRSDepTime: int
    Distance: int
    WeatherDelay: int


@app.get("/")
def home():
    return {"message": "Flight Delay Prediction API Running"}


@app.post("/predict")
def predict(data: FlightInput):

    airline_encoded = airline_encoder.transform([data.Airline])[0]

    input_df = pd.DataFrame([{
        "Month": data.Month,
        "DayOfWeek": data.DayOfWeek,
        "IATA_Code_Marketing_Airline": airline_encoded,
        "CRSDepTime": data.CRSDepTime,
        "Distance": data.Distance,
        "WeatherDelay": data.WeatherDelay
    }])

    prediction = model.predict(input_df)[0]

    labels = {
        0: "On Time",
        1: "Minor Delay",
        2: "Major Delay"
    }

    if prediction == 0:
        delay_minutes = 10
    elif prediction == 1:
        delay_minutes = 30
    else:
        delay_minutes = 60

    return {
        "prediction": int(prediction),
        "label": labels[prediction],
        "delay_minutes": delay_minutes
    }