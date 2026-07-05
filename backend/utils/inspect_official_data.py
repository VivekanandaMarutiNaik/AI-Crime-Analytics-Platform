import pandas as pd

df = pd.read_excel(
    "datasets/official/gp_village_mapping.xlsx",
    header=None,
    engine="openpyxl"
)

for i in range(12):
    print(f"\nROW {i}")
    print(df.iloc[i].tolist())