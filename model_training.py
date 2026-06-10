import pandas as pd

from sklearn.model_selection import train_test_split
<<<<<<< HEAD

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.svm import SVC


# Load cleaned data

df = pd.read_csv("cleaned_flight_data.csv")


# Convert Airline column to numbers

le = LabelEncoder()

df['IATA_Code_Marketing_Airline'] = le.fit_transform(
    df['IATA_Code_Marketing_Airline']
)


# Convert target variable
=======
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
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
>>>>>>> upstream/main

target_encoder = LabelEncoder()

df['Delay_Category'] = target_encoder.fit_transform(
    df['Delay_Category']
)

<<<<<<< HEAD

=======
>>>>>>> upstream/main
# Features

X = df[
[
<<<<<<< HEAD
'Month',
'DayOfWeek',
'IATA_Code_Marketing_Airline',
'CRSDepTime',
'Distance',
'DepDelay',
'WeatherDelay',
'CarrierDelay',
'LateAircraftDelay'
]
]


=======
    'Month',
    'DayOfWeek',
    'IATA_Code_Marketing_Airline',
    'CRSDepTime',
    'Distance',
    'WeatherDelay'
]
]

>>>>>>> upstream/main
# Target

y = df['Delay_Category']

<<<<<<< HEAD

# Split dataset

X_train,X_test,y_train,y_test = train_test_split(

X,
y,

test_size=0.2,

random_state=42

)


print("Training Started...\n")


###############################

# Logistic Regression

###############################

lr = LogisticRegression(max_iter=1000)

lr.fit(X_train,y_train)

pred_lr = lr.predict(X_test)

acc_lr = accuracy_score(y_test,pred_lr)

print("Logistic Regression Accuracy:",acc_lr)


###############################

# Random Forest

###############################

rf = RandomForestClassifier()

rf.fit(X_train,y_train)

pred_rf = rf.predict(X_test)

acc_rf = accuracy_score(y_test,pred_rf)

print("Random Forest Accuracy:",acc_rf)


###############################

# SVC

###############################

svc = SVC()

svc.fit(X_train,y_train)

pred_svc = svc.predict(X_test)

acc_svc = accuracy_score(y_test,pred_svc)

print("SVC Accuracy:",acc_svc)


print("\nCompleted")
=======
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
        average='weighted',
        zero_division=0
    ))

    print("Recall   :", recall_score(
        y_test,
        pred,
        average='weighted'
    ))

    print("F1 Score :", f1_score(
        y_test,
        pred,
        average='weighted'
    ))

    print("\nConfusion Matrix")

    print(confusion_matrix(y_test, pred))

print("\nTraining Completed")
>>>>>>> upstream/main
