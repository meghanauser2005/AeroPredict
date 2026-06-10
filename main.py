import pandas as pd

df = pd.read_csv("dataset/flight_delay_project_dataset.csv")

print(df.head())
print(df.columns)
print(df.shape)