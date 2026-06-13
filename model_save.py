import pandas as pd
import joblib
import numpy as np

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

print(dict(zip(
    target_encoder.classes_,
    target_encoder.transform(target_encoder.classes_)
)))

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

y = df['Delay_Category']

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)

X, y = smote.fit_resample(X, y)

print(pd.Series(y).value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Random Forest...")

rf = RandomForestClassifier(
    n_estimators= 200,
    max_depth = 20,
    class_weight="balanced",
    random_state=42
)

rf.fit(X_train, y_train)

pred = rf.predict(X_test)

unique, counts = np.unique(pred, return_counts=True)

print("\nPrediction Distribution:")
print(dict(zip(unique, counts)))

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