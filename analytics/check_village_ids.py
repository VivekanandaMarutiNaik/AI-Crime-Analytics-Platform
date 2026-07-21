import pandas as pd

crime = pd.read_csv("datasets/raw/crime_cases.csv")

print("Unique village IDs:", crime["village_id"].nunique())

dup = crime.groupby("village_id")["district"].nunique()

print("Village IDs appearing in multiple districts:", (dup > 1).sum())

if (dup > 1).any():
    print("\nExamples:")
    print(dup[dup > 1].head(20))