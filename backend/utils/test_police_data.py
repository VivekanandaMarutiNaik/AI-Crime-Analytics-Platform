import pandas as pd

df = pd.read_csv("datasets/raw/police_stations.csv")

print("Missing values in each column:")
print(df.isnull().sum())

print("\nRows where station_id is missing:")
print(df[df["station_id"].isna()])