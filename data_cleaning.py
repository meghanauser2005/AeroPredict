import pandas as pd

print("Program Started")

# Load Dataset
df = pd.read_csv("flight_delay_project_dataset.csv")

print("Original Shape:", df.shape)

# Remove missing arrival delay rows
df = df.dropna(subset=['ArrDelay'])

# Fill missing values
df['WeatherDelay'] = df['WeatherDelay'].fillna(0)
df['CarrierDelay'] = df['CarrierDelay'].fillna(0)
df['LateAircraftDelay'] = df['LateAircraftDelay'].fillna(0)

# Create Delay Categories

def categorize_delay(delay):

    if delay < 15:
        return "Green"

    elif delay <= 60:
        return "Orange"

    else:
        return "Red"


df['Delay_Category'] = df['ArrDelay'].apply(categorize_delay)

print("\nNew Shape:", df.shape)

print("\nDelay Categories Count:")

print(df['Delay_Category'].value_counts())

print("\nFirst 5 rows")

print(df.head())

# Save cleaned dataset

df.to_csv("cleaned_flight_data.csv", index=False)

print("\nFile Saved Successfully")