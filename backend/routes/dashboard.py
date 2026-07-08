from fastapi import APIRouter
from pathlib import Path
import pandas as pd
from typing import Optional

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

BASE_DIR = Path(__file__).resolve().parents[2]

CRIMES_FILE = BASE_DIR / "datasets" / "raw" / "crime_cases.csv"

CCTV_FILE = BASE_DIR / "datasets" / "processed" / "cctv_master.csv"
HOTSPOTS_FILE = BASE_DIR / "datasets" / "processed" / "crime_hotspots.csv"
COVERAGE_FILE = BASE_DIR / "datasets" / "processed" / "cctv_coverage_analysis.csv"
RECOMMENDATIONS_FILE = (
    BASE_DIR / "datasets" / "processed" / "cctv_installation_recommendations.csv"
)



@router.get("/summary")
def get_dashboard_summary(district: Optional[str] = None):
    crimes = pd.read_csv(CRIMES_FILE)
    cctv = pd.read_csv(CCTV_FILE)
    hotspots = pd.read_csv(HOTSPOTS_FILE)
    coverage = pd.read_csv(COVERAGE_FILE)
    recommendations = pd.read_csv(RECOMMENDATIONS_FILE)

    if district:
        crimes = crimes[crimes["district"] == district]
        cctv = cctv[cctv["district"] == district]

    return {
        "total_crimes": len(crimes),
        "total_cctv": len(cctv),
        "total_hotspots": len(hotspots),
        "covered_hotspots": int(coverage["covered"].sum()),
        "uncovered_hotspots": int((~coverage["covered"]).sum()),
        "critical_recommendations": len(
            recommendations[recommendations["priority"] == "Critical"]
        ),
        "high_recommendations": len(
            recommendations[recommendations["priority"] == "High"]
        ),
        "medium_recommendations": len(
            recommendations[recommendations["priority"] == "Medium"]
        ),
        "low_recommendations": len(
            recommendations[recommendations["priority"] == "Low"]
        ),
    }

@router.get("/charts")
def get_dashboard_charts(district: Optional[str] = None):
    crimes = pd.read_csv(CRIMES_FILE)

    if district:
        crimes = crimes[crimes["district"] == district]

    crime_types = (
        crimes["crime_type"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    crime_types.columns = ["crime_type", "count"]

    crime_severity = (
        crimes["crime_severity"]
        .value_counts()
        .reset_index()
    )
    crime_severity.columns = ["severity", "count"]

    district_distribution = (
        crimes["district"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    district_distribution.columns = ["district", "count"]

    police_station_distribution = (
        crimes["police_station_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    police_station_distribution.columns = [
        "police_station",
        "count",
    ]


    return {
        "crime_types": crime_types.to_dict(orient="records"),
        "crime_severity": crime_severity.to_dict(orient="records"),
        "district_distribution": district_distribution.to_dict(orient="records"),
        "police_station_distribution": police_station_distribution.to_dict(
            orient="records"
        ),
    }

@router.get("/insights")
def get_ai_insights(district: Optional[str] = None):
    crimes = pd.read_csv(CRIMES_FILE)
    coverage = pd.read_csv(COVERAGE_FILE)
    recommendations = pd.read_csv(RECOMMENDATIONS_FILE)

    if district:
        crimes = crimes[crimes["district"] == district]
    
    police_station_distribution = (
        crimes["police_station_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    police_station_distribution.columns = [
        "police_station",
        "count",
    ]

    top_crime = crimes["crime_type"].value_counts().idxmax()
    top_crime_count = int(crimes["crime_type"].value_counts().max())

    top_district = crimes["district"].value_counts().idxmax()
    top_district_count = int(crimes["district"].value_counts().max())

    severity = crimes["crime_severity"].value_counts()
    total = len(crimes)

    covered = int(coverage["covered"].sum())
    uncovered = int((~coverage["covered"]).sum())

    critical = len(
        recommendations[
            recommendations["priority"] == "Critical"
        ]
    )

    return {
        "top_crime": {
            "name": top_crime,
            "count": top_crime_count,
        },
        "top_district": {
            "name": top_district,
            "count": top_district_count,
        },
        "severity_distribution": {
            level: round(count / total * 100, 1)
            for level, count in severity.items()
        },
        "covered_hotspots": covered,
        "uncovered_hotspots": uncovered,
        "critical_recommendations": critical,
    }