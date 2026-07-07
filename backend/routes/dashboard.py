from fastapi import APIRouter
from pathlib import Path
import pandas as pd

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

BASE_DIR = Path(__file__).resolve().parents[2]

CRIMES_FILE = BASE_DIR / "datasets" / "raw" / "crime_cases.csv"

print("BASE_DIR =", BASE_DIR)
print("Crime file =", CRIMES_FILE)
CCTV_FILE = BASE_DIR / "datasets" / "processed" / "cctv_master.csv"
HOTSPOTS_FILE = BASE_DIR / "datasets" / "processed" / "crime_hotspots.csv"
COVERAGE_FILE = BASE_DIR / "datasets" / "processed" / "cctv_coverage_analysis.csv"
RECOMMENDATIONS_FILE = (
    BASE_DIR / "datasets" / "processed" / "cctv_installation_recommendations.csv"
)

@router.get("/summary")
def get_dashboard_summary():
    crimes = pd.read_csv(CRIMES_FILE)
    cctv = pd.read_csv(CCTV_FILE)
    hotspots = pd.read_csv(HOTSPOTS_FILE)
    coverage = pd.read_csv(COVERAGE_FILE)
    recommendations = pd.read_csv(RECOMMENDATIONS_FILE)

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