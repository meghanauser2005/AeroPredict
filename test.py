from backend.app import airline_encoder
Month = 1
DayOfWeek = 1
AirlineCode = 8
CRSDepTime = 1120
Distance = 557
WeatherDelay = 0
print(
    dict(
        zip(
            airline_encoder.classes_,
            airline_encoder.transform(airline_encoder.classes_)
        )
    )
)