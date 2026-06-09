import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from imblearn.over_sampling import SMOTE

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

y = df['Delay_Category']

print("\nBefore SMOTE")

print(y.value_counts())

# Apply SMOTE

smote = SMOTE(random_state=42)

X, y = smote.fit_resample(X, y)

print("\nAfter SMOTE")

print(pd.Series(y).value_counts())

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

models = {

    "Logistic Regression":
    LogisticRegression(max_iter=3000),

    "Random Forest":
    RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "SVC":
    LinearSVC(max_iter=5000)

}

for name, model in models.items():

    print("\n" + "="*50)
    print(name)
    print("="*50)

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print("Accuracy :", accuracy_score(y_test, pred))

    print("Precision:", precision_score(
        y_test,
        pred,
        average='weighted'
    ))

    print("Recall   :", recall_score(
        y_test,
        pred,
        average='weighted',
        zero_division = 0
    ))

    print("F1 Score :", f1_score(
        y_test,
        pred,
        average='weighted'
    ))

    print("\nConfusion Matrix")

    print(confusion_matrix(y_test, pred))

print("\nSMOTE Training Completed")