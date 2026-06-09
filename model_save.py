import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print("Loading Dataset...")

df = pd.read_csv("cleaned_flight_data.csv")

# Encode Airline

airline_encoder = LabelEncoder()

df['IATA_Code_Marketing_Airline'] = airline_encoder.fit_transform(
    df['IATA_Code_Marketing_Airline']
)

# Encode Target

target_encoder = LabelEncoder()

df['Delay_Category'] = target_encoder.fit_transform(
    df['Delay_Category']
)

# Features

X = df[
[
    'Month',
    'DayOfWeek',
    'IATA_Code_Marketing_Airline',
    'CRSDepTime',
    'Distance',
    'WeatherDelay'
]
]

# Target

y = df['Delay_Category']

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Random Forest...")

rf = RandomForestClassifier(
    n_estimators=30,
    max_depth = 10,
    random_state=42
)

rf.fit(X_train, y_train)

pred = rf.predict(X_test)

print("\nAccuracy:")

print(accuracy_score(y_test, pred))

print("\nClassification Report:\n")

print(classification_report(
    y_test,
    pred
))

print("\nConfusion Matrix:\n")

print(confusion_matrix(
    y_test,
    pred
))

# Save Model

joblib.dump(
    rf,
    "final_model.pkl"
)

joblib.dump(
    airline_encoder,
    "airline_encoder.pkl"
)

joblib.dump(
    target_encoder,
    "target_encoder.pkl"
)

print("\nModel Saved Successfully")
print("Encoders Saved Successfully")