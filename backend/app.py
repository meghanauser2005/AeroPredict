from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import requests

# ==========================
# CONFIG
# ==========================

API_KEY = "a0c8cf1bf7c76f75eb0a53c753f9fd46"

airport_coords = {
    "JFK": (40.6413, -73.7781),
    "LAX": (33.9416, -118.4085),
    "ORD": (41.9742, -87.9073),
    "ATL": (33.6407, -84.4277),
    "DFW": (32.8998, -97.0403),
    "SFO": (37.6213, -122.3790),
    "SEA": (47.4502, -122.3088),
    "MIA": (25.7959, -80.2870),
}

# ==========================
# WEATHER FUNCTION
# ==========================

def get_weather_delay(airport):

    coords = airport_coords.get(airport)

    if not coords:
        return 10

    lat, lon = coords

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={API_KEY}"
        )

        response = requests.get(url, timeout=5)
        weather = response.json()

        weather_main = weather["weather"][0]["main"]

        if weather_main == "Thunderstorm":
            delay = 40

        elif weather_main in ["Rain", "Drizzle"]:
            delay = 25

        elif weather_main == "Snow":
            delay = 35

        elif weather_main in ["Mist", "Fog"]:
            delay = 20

        else:
            delay = 5
        
        return delay, weather_main

    except Exception:
        return 10, None


# ==========================
# FASTAPI
# ==========================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# LOAD MODEL
# ==========================

model = joblib.load("final_model.pkl")
airline_encoder = joblib.load("airline_encoder.pkl")

# ==========================
# INPUT MODEL
# ==========================

class FlightInput(BaseModel):
    Month: int
    DayOfWeek: int
    Airline: str
    CRSDepTime: int
    Distance: int
    Airport: str


# ==========================
# ROUTES
# ==========================

@app.get("/")
def home():
    return {
        "message": "Flight Delay Prediction API Running"
    }


@app.post("/predict")
def predict(data: FlightInput):

    airline_encoded = airline_encoder.transform([data.Airline])[0]

    weather_delay, weather_condition = get_weather_delay(data.Airport)

    input_df = pd.DataFrame([{
        "Month": data.Month,
        "DayOfWeek": data.DayOfWeek,
        "IATA_Code_Marketing_Airline": airline_encoded,
        "CRSDepTime": data.CRSDepTime,
        "Distance": data.Distance,
        "WeatherDelay": weather_delay
    }])

    ml_prediction = int(model.predict(input_df)[0])

    print("\n==========")
    print(input_df)
    print("ML Prediction:", ml_prediction)
    print("Weather Delay:", weather_delay)
    print("==========\n")

    prediction = ml_prediction

    if weather_delay >= 35:
        prediction = 2

    elif weather_delay >= 20:
        prediction = max(prediction, 1)

    print("Final Prediction:", prediction)
    

    labels = {
        0: "On Time",
        1: "Minor Delay",
        2: "Major Delay"
    }

    if prediction == 0:
        delay_minutes = weather_delay

    elif prediction == 1:
        delay_minutes = 20 + weather_delay

    else:
        delay_minutes = 60 + weather_delay
    
    reasons = []

    if weather_delay >= 35:
        reasons.append(
            f"Severe weather ({weather_condition}) detected at airport"
        )

    elif weather_delay >= 20:
        reasons.append(
            f"Weather conditions ({weather_condition}) may impact operations"
        )

    if 6 <= data.CRSDepTime <= 10:
        reasons.append(
            "Morning airport traffic may cause congestion"
        )

    if 16 <= data.CRSDepTime <= 21:
        reasons.append(
            "Evening rush hour increases delay probability"
        )

    if data.Distance > 1500:
        reasons.append(
            "Long-haul flight routes are more delay-prone"
        )

    if not reasons:
        reasons.append(
            "Flight conditions appear normal"
        )

    if len(reasons) == 0:
        reasons.append("Flight conditions appear normal")
    
    print("Input Features:")
    print(input_df)
    print("Prediction:", prediction)

    print("Raw Prediction:", prediction)
    print("Label:", labels[prediction])

    return {
        "prediction": int(prediction),
        "label": labels[prediction],
        "delay_minutes": delay_minutes,
        "airport": data.Airport,
        "weather_delay_used": weather_delay,
        "weather_condition": weather_condition,
        "explanation": reasons
    }

@app.post("/predict_test")
def predict_test(
    Month: int,
    DayOfWeek: int,
    AirlineCode: int,
    CRSDepTime: int,
    Distance: int,
    WeatherDelay: int
):

    input_df = pd.DataFrame([{
        "Month": Month,
        "DayOfWeek": DayOfWeek,
        "IATA_Code_Marketing_Airline": AirlineCode,
        "CRSDepTime": CRSDepTime,
        "Distance": Distance,
        "WeatherDelay": WeatherDelay
    }])

    prediction = model.predict(input_df)[0]

    return {
        "prediction": int(prediction),
        "probabilities": model.predict_proba(input_df)[0].tolist()
    }