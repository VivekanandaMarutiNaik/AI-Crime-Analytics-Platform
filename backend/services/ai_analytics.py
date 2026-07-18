import pandas as pd
from pathlib import Path

import re


BASE_DIR = Path(__file__).resolve().parents[2]

CRIME_DATA = pd.read_csv(
    BASE_DIR / "datasets" / "raw" / "crime_cases.csv"
)

CCTV_DATA = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "cctv_master.csv"
)

CCTV_RECOMMENDATIONS = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "cctv_installation_recommendations.csv"
)


def get_ai_answer(text: str, intent: dict):

    text = text.lower()

    # -------------------------------------------------
    # District Crime Summary
    # -------------------------------------------------
    if (
        "summary" in text
        or "report" in text
        or "overview" in text
        or "details" in text
    ):

        district = intent.get("district")

        if district:
            return get_district_summary(
                CRIME_DATA,
                district,
            )

        return "❌ Please specify a valid district."
    
    # -------------------------------------------------
    # District Statistics
    # -------------------------------------------------
    elif (
        "statistics" in text
        or "stats" in text
        or "analytics" in text
    ):

        district = intent.get("district")

        if district:
            return get_district_statistics(
                CRIME_DATA,
                district,
            )

        return "❌ Please specify a valid district."
    
    # -------------------------------------------------
    # Crime Trend Analysis
    # -------------------------------------------------
    elif (
        "trend" in text
        or "increase" in text
        or "decrease" in text
        or "growth" in text
    ):

        district = intent.get("district")

        if district:
            return get_crime_trend(
                CRIME_DATA,
                district,
            )

        return "❌ Please specify a valid district."
    


    # -------------------------------------------------
    # District needing Maximum CCTV
    # -------------------------------------------------
    elif (
        ("cctv" in text or "camera" in text)
        and (
            "need" in text
            or "needs" in text
            or "require" in text
            or "required" in text
            or "maximum" in text
            or "recommend" in text
            or "installation" in text
        )
    ):

        return get_max_cctv_requirement(
            CCTV_RECOMMENDATIONS
        )

    # -------------------------------------------------
    # Highest CCTV Coverage
    # -------------------------------------------------
    elif (
        ("cctv" in text or "camera" in text)
        and (
            "coverage" in text
            or "covered" in text
            or "available" in text
            or "active" in text
            or "best" in text
            or "highest" in text
            or "most" in text
        )
    ):

        return get_highest_cctv_coverage(
            CCTV_DATA
        )

        # -------------------------------------------------
    # Top N Queries
    # -------------------------------------------------
    elif intent.get("intent") == "top":

        top_n = extract_top_n(text)

        # Top crime types
        if (
            "crime" in text
            or "crimes" in text
            or "type" in text
            or "types" in text
            or "category" in text
            or "categories" in text
        ):
            return get_top_crime_types(
                CRIME_DATA,
                n=top_n,
            )

        # Otherwise return top crime districts
        return get_top_crime_districts(
            CRIME_DATA,
            n=top_n,
        )
    
    # -------------------------------------------------
    # Highest Crime District
    # -------------------------------------------------
    elif (
        ("highest" in text or "most" in text)
        and "crime" in text
        and "district" in text
        and "cctv" not in text
        and "camera" not in text
    ):

        highest = (
            CRIME_DATA.groupby("district")
            .size()
            .sort_values(ascending=False)
            .reset_index(name="crime_count")
            .iloc[0]
        )

        return (
            f"📊 Highest Crime District\n\n"
            f"🏙 District : {highest['district']}\n"
            f"📌 Cases : {highest['crime_count']:,}"
        )

    # -------------------------------------------------
    # Safest District
    # -------------------------------------------------
    elif (
        "safest" in text
        or (
            ("lowest" in text or "least" in text)
            and "district" in text
        )
    ):

        safest = (
            CRIME_DATA.groupby("district")
            .size()
            .sort_values()
            .reset_index(name="crime_count")
            .iloc[0]
        )

        return (
            f"🛡️ Safest District\n\n"
            f"🏙 District : {safest['district']}\n"
            f"📌 Cases : {safest['crime_count']:,}"
        )

    # -------------------------------------------------
    # Crime Type Queries
    # -------------------------------------------------
    elif intent.get("crime_type"):

        crime = intent["crime_type"]
        district = intent.get("district")

        # If district is specified
        if district:

            filtered = CRIME_DATA[
                (CRIME_DATA["district"].str.lower() == district.lower())
                &
                (
                    CRIME_DATA["crime_type"]
                    .str.contains(crime, case=False, na=False)
                )
            ]

            if filtered.empty:
                return f"❌ No {crime} cases found in {district}."

            crime_counts = (
                filtered.groupby("crime_type")
                .size()
                .sort_values(ascending=False)
            )

            answer = (
                f"📍 {crime} Cases in {district}\n\n"
                f"📌 Total Cases : {len(filtered):,}\n\n"
                f"Breakdown:\n"
            )

            for crime_type, count in crime_counts.items():
                answer += f"• {crime_type}: {count}\n"

            return answer

        # No district specified
        filtered = CRIME_DATA[
            CRIME_DATA["crime_type"]
            .str.contains(crime, case=False, na=False)
        ]

        if filtered.empty:
            return f"❌ No {crime} cases found."

        district_counts = (
            filtered.groupby("district")
            .size()
            .sort_values(ascending=False)
        )

        answer = (
            f"📍 {crime} Cases Across Karnataka\n\n"
            f"📌 Total Cases : {len(filtered):,}\n\n"
            f"District-wise:\n"
        )

        for district_name, count in district_counts.items():
            answer += f"• {district_name}: {count}\n"

        return answer
    # -------------------------------------------------
# AI Risk Prediction
# -------------------------------------------------
    elif (
        "risk" in text
        or "predict" in text
        or "prediction" in text
        or "hotspot" in text
        or "danger" in text
    ):

        return get_risk_prediction(
            CRIME_DATA,
            CCTV_DATA,
            CCTV_RECOMMENDATIONS,
        )

    return None



def get_top_crime_districts(crime_df, n=3):
    """
    Returns the top N crime districts.
    """

    top = (
        crime_df.groupby("district")
        .size()
        .sort_values(ascending=False)
        .head(n)
        .reset_index(name="crime_count")
    )

    total = len(crime_df)

    answer = f"🏆 Top {len(top)} Crime Districts\n\n"

    for i, row in top.iterrows():
        share = (row["crime_count"] / total) * 100

        answer += (
            f"{i+1}. {row['district']}\n"
            f"   📌 Cases : {row['crime_count']:,}\n"
            f"   📊 Share : {share:.2f}%\n\n"
        )

    return answer

def extract_top_n(query, default=3):
    """
    Extract Top N from queries like:
    Top 5 districts
    Highest 10 crime districts
    """

    match = re.search(r"\b(\d+)\b", query)

    if match:
        n = int(match.group(1))

        # Prevent silly values
        return max(1, min(n, 31))

    return default

def get_top_crime_types(crime_df, n=5):
    """
    Returns the top N crime types.
    """

    top = (
        crime_df.groupby("crime_type")
        .size()
        .sort_values(ascending=False)
        .head(n)
        .reset_index(name="case_count")
    )

    total = len(crime_df)

    answer = f"🚔 Top {len(top)} Crime Types\n\n"

    for i, row in top.iterrows():

        share = (row["case_count"] / total) * 100

        answer += (
            f"{i+1}. {row['crime_type']}\n"
            f"   📌 Cases : {row['case_count']:,}\n"
            f"   📊 Share : {share:.2f}%\n\n"
        )

    return answer

def get_district_summary(crime_df, district):

    district_df = crime_df[
        crime_df["district"].str.lower() == district.lower()
    ]

    if district_df.empty:
        return f"❌ No crime data found for '{district}'."

    total_cases = len(district_df)

    closed_cases = (
        district_df["case_status"]
        .astype(str)
        .str.lower()
        .eq("closed")
        .sum()
    )

    ongoing_cases = total_cases - closed_cases

    closure_rate = (closed_cases / total_cases) * 100

    avg_response = district_df["response_time_minutes"].mean()

    fastest_response = district_df["response_time_minutes"].min()

    cctv_cases = (
        district_df["cctv_available"]
        .astype(str)
        .str.lower()
        .eq("yes")
        .sum()
    )

    cctv_percentage = (cctv_cases / total_cases) * 100

    high_severity = (
        district_df["crime_severity"]
        .astype(str)
        .str.lower()
        .eq("high")
        .sum()
    )

    hotspot_score = district_df["hotspot_score"].mean()

    male_victims = (
        district_df["victim_gender"]
        .astype(str)
        .str.lower()
        .eq("male")
        .sum()
    )

    female_victims = (
        district_df["victim_gender"]
        .astype(str)
        .str.lower()
        .eq("female")
        .sum()
    )

    top_crimes = (
        district_df.groupby("crime_type")
        .size()
        .sort_values(ascending=False)
        .head(3)
    )

    most_common_crime = top_crimes.index[0]

    answer = (
        f"📍 Crime Summary: {district}\n\n"

        f"📌 Total Cases : {total_cases:,}\n"
        f"✅ Closed Cases : {closed_cases:,}\n"
        f"🟡 Ongoing Cases : {ongoing_cases:,}\n"
        f"📊 Closure Rate : {closure_rate:.1f}%\n\n"

        f"👥 Victims\n"
        f"   ♂ Male : {male_victims:,}\n"
        f"   ♀ Female : {female_victims:,}\n\n"

        f"🚨 High Severity Cases : {high_severity:,}\n"

        f"📹 CCTV Coverage : {cctv_percentage:.1f}%\n"

        f"🔥 Average Hotspot Score : {hotspot_score:.2f}\n\n"

        f"⏱ Average Response : {avg_response:.1f} min\n"
        f"⚡ Fastest Response : {fastest_response:.1f} min\n\n"

        f"🏆 Most Common Crime : {most_common_crime}\n\n"

        f"🚔 Top Crime Types\n"
    )

    for i, (crime, count) in enumerate(top_crimes.items(), 1):
        answer += f"\n{i}. {crime} ({count})"

    return answer
def get_max_cctv_requirement(recommendation_df):
    """
    Returns the district with the highest CCTV installation priority.
    """

    district_summary = (
        recommendation_df.groupby("district")
        .agg(
            recommended_locations=("recommend_installation", "sum"),
            crime_count=("crime_count", "sum"),
            existing_cctv=("cctv_count", "sum"),
            avg_hotspot=("avg_hotspot_score", "mean"),
            avg_priority=("priority_score", "mean"),
        )
        .sort_values("avg_priority", ascending=False)
    )

    if district_summary.empty:
        return "❌ No CCTV recommendation data available."

    district = district_summary.index[0]
    top = district_summary.iloc[0]

    return (
        f"📹 CCTV Installation Priority\n\n"
        f"🏙 District : {district}\n"
        f"🚨 Crime Count : {int(top['crime_count']):,}\n"
        f"📹 Existing CCTV : {int(top['existing_cctv']):,}\n"
        f"📍 Recommended Installations : {int(top['recommended_locations']):,}\n"
        f"🔥 Average Hotspot Score : {top['avg_hotspot']:.2f}\n"
        f"⭐ Priority Score : {top['avg_priority']:.2f}\n\n"
        f"🤖 AI Recommendation\n"
        f"Install additional CCTV cameras in {district} first because it has the highest priority score and significant crime activity."
    )

def get_highest_cctv_coverage(cctv_df):
    """
    Returns the district with the highest CCTV coverage.
    """

    coverage = (
        cctv_df.groupby("district")
        .agg(
            total_cameras=("cctv_id", "count"),
            active_cameras=(
                "status",
                lambda x: x.astype(str).str.lower().eq("active").sum()
            ),
        )
    )

    coverage["coverage_percent"] = (
        coverage["active_cameras"]
        / coverage["total_cameras"]
    ) * 100

    coverage = coverage.sort_values(
        by=["coverage_percent", "total_cameras"],
        ascending=False,
    )

    if coverage.empty:
        return "❌ No CCTV data available."

    district = coverage.index[0]
    top = coverage.iloc[0]

    return (
        f"🎥 Highest CCTV Coverage\n\n"
        f"🏙 District : {district}\n"
        f"📹 Total CCTV Cameras : {int(top['total_cameras']):,}\n"
        f"✅ Active Cameras : {int(top['active_cameras']):,}\n"
        f"📊 Coverage : {top['coverage_percent']:.1f}%"
    )

def get_district_statistics(crime_df, district):

    district_df = crime_df[
        crime_df["district"].str.lower() == district.lower()
    ]

    if district_df.empty:
        return f"❌ No data found for {district}."

    total_cases = len(district_df)

    category_stats = (
        district_df.groupby("crime_category")
        .size()
        .sort_values(ascending=False)
        .head(5)
    )

    severity_stats = (
        district_df["crime_severity"]
        .value_counts()
    )

    answer = (
        f"📊 Crime Statistics : {district}\n\n"
        f"📌 Total Cases : {total_cases:,}\n\n"
        f"🚔 Top Crime Categories\n"
    )

    for i, (cat, count) in enumerate(category_stats.items(), 1):
        answer += f"\n{i}. {cat} ({count})"

    answer += "\n\n🚨 Severity Distribution"

    for sev, count in severity_stats.items():
        answer += f"\n• {sev} : {count}"

    return answer


def get_crime_trend(crime_df, district):

    df = crime_df.copy()

    df["crime_datetime"] = pd.to_datetime(df["crime_datetime"])

    district_df = df[
        df["district"].str.lower() == district.lower()
    ]

    if district_df.empty:
        return f"❌ No crime data found for {district}."

    monthly = (
        district_df
        .groupby(
            district_df["crime_datetime"].dt.to_period("M")
        )
        .size()
        .sort_index()
    )

    if len(monthly) < 2:
        return "❌ Not enough data to calculate crime trend."

    current_month = monthly.iloc[-1]
    previous_month = monthly.iloc[-2]

    change = current_month - previous_month

    change_percent = (
        (change / previous_month) * 100
        if previous_month != 0
        else 100
    )

    trend = "🔺 Increasing" if change > 0 else "🔻 Decreasing"

    growing = (
        district_df[
            district_df["crime_datetime"].dt.to_period("M")
            == monthly.index[-1]
        ]
        .groupby("crime_type")
        .size()
        .sort_values(ascending=False)
        .head(3)
    )

    answer = (
        f"📈 Crime Trend : {district}\n\n"
        f"📅 Current Month Cases : {current_month}\n"
        f"📅 Previous Month Cases : {previous_month}\n\n"
        f"📊 Change : {change:+d} ({change_percent:.1f}%)\n"
        f"📍 Trend : {trend}\n\n"
        f"🚔 Top Crimes This Month\n"
    )

    for i, (crime, count) in enumerate(growing.items(), 1):
        answer += f"\n{i}. {crime} ({count})"

    answer += "\n\n🤖 AI Insight\n"

    if change > 0:
        answer += (
            "Crime has increased compared to the previous month. "
            "Additional surveillance and patrolling are recommended."
        )
    elif change < 0:
        answer += (
            "Crime has decreased compared to the previous month. "
            "Current policing measures appear effective."
        )
    else:
        answer += "Crime levels remained stable compared to the previous month."

    return answer

def get_risk_prediction(crime_df, cctv_df, recommendation_df):

    # Crime count
    crime_counts = (
        crime_df.groupby("district")
        .size()
        .rename("crime_count")
    )

    # Average hotspot score
    hotspot = (
        crime_df.groupby("district")["hotspot_score"]
        .mean()
        .rename("hotspot_score")
    )

    # Existing CCTV
    cctv = (
        cctv_df.groupby("district")
        .size()
        .rename("cctv_count")
    )

    # CCTV recommendation
    recommendations = (
        recommendation_df.groupby("district")
        .agg(
            recommended_locations=("recommend_installation", "sum"),
            priority_score=("priority_score", "mean"),
        )
    )

    df = (
        crime_counts.to_frame()
        .join(hotspot)
        .join(cctv)
        .join(recommendations)
        .fillna(0)
    )

    # Normalize metrics
    df["crime_norm"] = df["crime_count"] / df["crime_count"].max()
    df["hotspot_norm"] = df["hotspot_score"] / df["hotspot_score"].max()
    df["priority_norm"] = (
        df["priority_score"] / df["priority_score"].max()
    )

    # Lower CCTV => Higher Risk
    df["cctv_norm"] = 1 - (
        df["cctv_count"] / df["cctv_count"].max()
    )

    # Weighted Risk Score
    df["risk_score"] = (
        0.40 * df["crime_norm"]
        + 0.30 * df["hotspot_norm"]
        + 0.20 * df["priority_norm"]
        + 0.10 * df["cctv_norm"]
    ) * 100

    df = df.sort_values(
        "risk_score",
        ascending=False,
    )

    district = df.index[0]
    top = df.iloc[0]

    risk_level = (
    "🔴 Very High"
    if top["risk_score"] >= 80
    else "🟠 High"
    if top["risk_score"] >= 60
    else "🟡 Medium"
    if top["risk_score"] >= 40
    else "🟢 Low"
)

    return (
        f"🤖 AI Crime Risk Assessment\n\n"

        f"🏙 District : {district}\n"
        f"🚨 Risk Score : {top['risk_score']:.1f}/100\n"
        f"📍 Risk Level : {risk_level}\n\n"

        f"📊 Risk Indicators\n"
        f"• Crime Count : {int(top['crime_count']):,}\n"
        f"• Average Hotspot Score : {top['hotspot_score']:.2f}\n"
        f"• Existing CCTV : {int(top['cctv_count']):,}\n"
        f"• Recommended CCTV : {int(top['recommended_locations']):,}\n\n"

        f"🧠 AI Assessment\n"
        f"{district} currently has the highest composite crime risk "
        f"based on crime frequency, hotspot intensity, surveillance "
        f"coverage and CCTV deployment priority.\n\n"

        f"🚔 Recommended Actions\n"
        f"1. Increase police patrols in hotspot areas.\n"
        f"2. Install recommended CCTV cameras.\n"
        f"3. Monitor repeat crime locations.\n"
        f"4. Focus on high-frequency crime categories."
    )