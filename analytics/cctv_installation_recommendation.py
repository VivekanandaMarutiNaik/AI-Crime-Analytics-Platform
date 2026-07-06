import pandas as pd

# Load datasets
crime = pd.read_csv("datasets/raw/crime_cases.csv")

severity_score = {
    "Critical": 100,
    "High": 80,
    "Medium": 60,
}

crime["severity_score"] = crime["crime_severity"].map(severity_score)

cctv = pd.read_csv("datasets/processed/cctv_master.csv")

# Crime statistics by village
crime_stats = (
    crime.groupby(
        [
            "district_id",
            "district",
            "taluk",
            "village",
            "gram_panchayat",
        ]
    )
    .agg(
        crime_count=("crime_id", "count"),
        avg_hotspot_score=("hotspot_score", "mean"),
        avg_severity=("severity_score", "mean"),
    )
    .reset_index()
)

# CCTV count by village
cctv_stats = (
    cctv.groupby(
        [
            "district_id",
            "district",
            "taluk",
            "village",
            "gram_panchayat",
        ]
    )
    .size()
    .reset_index(name="cctv_count")
)

# Merge
recommendations = crime_stats.merge(
    cctv_stats,
    on=[
        "district_id",
        "district",
        "taluk",
        "village",
        "gram_panchayat",
    ],
    how="left",
)

recommendations["cctv_count"] = recommendations["cctv_count"].fillna(0)

# Normalize crime count to a 0–100 score
recommendations["crime_score"] = (
    recommendations["crime_count"]
    / recommendations["crime_count"].max()
) * 100

# CCTV coverage score
recommendations["coverage_score"] = recommendations["cctv_count"].apply(
    lambda x: 100 if x == 0 else
              50 if x == 1 else
              20 if x == 2 else
              0
)

# Final priority score (0–100)
recommendations["priority_score"] = (
    recommendations["crime_score"] * 0.40
    + recommendations["avg_hotspot_score"] * 0.35
    + recommendations["coverage_score"] * 0.15
    + recommendations["avg_severity"] * 0.10
).round(2)

# Recommendation rule
# Assign priority level
recommendations["priority"] = "Low"

recommendations.loc[
    recommendations["priority_score"] >= 90,
    "priority"
] = "Critical"

recommendations.loc[
    (recommendations["priority_score"] >= 75)
    & (recommendations["priority_score"] < 90),
    "priority"
] = "High"

recommendations.loc[
    (recommendations["priority_score"] >= 60)
    & (recommendations["priority_score"] < 75),
    "priority"
] = "Medium"

recommendations["recommend_installation"] = (
    recommendations["priority"] != "Low"
)

recommendations = recommendations.sort_values(
    "priority_score",
    ascending=False,
)

recommendations.to_csv(
    "datasets/processed/cctv_installation_recommendations.csv",
    index=False,
)

print("\nTop 20 CCTV Installation Recommendations:\n")

print(
    recommendations[
        [
            "district",
            "taluk",
            "village",
            "crime_count",
            "avg_hotspot_score",
            "avg_severity",
            "cctv_count",
            "priority_score",
            "priority",
        ]
    ].head(20).to_string(index=False)
)

print("\nPriority Summary:")
print(recommendations["priority"].value_counts())