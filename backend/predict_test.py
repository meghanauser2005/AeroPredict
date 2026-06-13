import pandas as pd
import joblib

# Load model
model = joblib.load("final_model.pkl")

# Class mapping from your encoder
labels = {
    0: "Green (No Delay)",
    1: "Orange (Minor Delay)",
    2: "Red (Major Delay)"
}

tests = [

    {
        "name": "Case 1 - Expected Green",
        "Month": 1,
        "DayOfWeek": 2,
        "IATA_Code_Marketing_Airline": 0,
        "CRSDepTime": 5,
        "Distance": 200,
        "WeatherDelay": 0
    },

    {
        "name": "Case 2 - Expected Orange",
        "Month": 6,
        "DayOfWeek": 4,
        "IATA_Code_Marketing_Airline": 3,
        "CRSDepTime": 18,
        "Distance": 1200,
        "WeatherDelay": 20
    },

    {
        "name": "Case 3 - Expected Red",
        "Month": 12,
        "DayOfWeek": 7,
        "IATA_Code_Marketing_Airline": 5,
        "CRSDepTime": 22,
        "Distance": 3500,
        "WeatherDelay": 40
    }

]

for t in tests:

    df = pd.DataFrame([{
        "Month": t["Month"],
        "DayOfWeek": t["DayOfWeek"],
        "IATA_Code_Marketing_Airline": t["IATA_Code_Marketing_Airline"],
        "CRSDepTime": t["CRSDepTime"],
        "Distance": t["Distance"],
        "WeatherDelay": t["WeatherDelay"]
    }])

    pred = model.predict(df)[0]
    probs = model.predict_proba(df)[0]

    print("\n" + "=" * 60)
    print(t["name"])
    print("=" * 60)

    print("Prediction:", pred)
    print("Label:", labels[pred])

    print("\nProbabilities")
    print(f"Green  : {probs[0]:.4f}")
    print(f"Orange : {probs[1]:.4f}")
    print(f"Red    : {probs[2]:.4f}")