import pandas as pd

df = pd.read_csv("flight_delay_project_dataset.csv", nrows=50000)

print(df.head())
print(df.shape)