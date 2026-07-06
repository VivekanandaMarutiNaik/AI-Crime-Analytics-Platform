import random

CRIME_CATEGORIES = {
    "Property Crime": [
        "Vehicle Theft",
        "House Burglary",
        "Chain Snatching",
        "Shop Theft"
    ],
    "Violent Crime": [
        "Assault",
        "Robbery",
        "Murder",
        "Attempt to Murder"
    ],
    "Crime Against Women": [
        "Domestic Violence",
        "Sexual Harassment",
        "Stalking"
    ],
    "Cyber Crime": [
        "UPI Fraud",
        "Phishing",
        "OTP Scam"
    ],
    "Economic Crime": [
        "Cheating",
        "Forgery",
        "Financial Fraud"
    ],
    "Public Order": [
        "Rioting",
        "Illegal Gambling",
        "Illegal Liquor"
    ],
    "Rural Crime": [
        "Crop Theft",
        "Cattle Theft",
        "Sand Mining"
    ]
}


def get_random_crime():
    category = random.choice(list(CRIME_CATEGORIES.keys()))
    crime = random.choice(CRIME_CATEGORIES[category])
    return category, crime

def get_victim_gender(crime_category):
    if crime_category == "Crime Against Women":
        return "Female"

    return random.choice(["Male", "Female"])

def get_crime_severity(crime_category):
    severity_map = {
        "Violent Crime": "Critical",
        "Property Crime": "Medium",
        "Cyber Crime": "Medium",
        "Crime Against Women": "High",
        "Crime Against Children": "High",
        "Economic Offence": "High",
        "Traffic Offence": "Low",
        "Narcotics": "High",
        "Missing Person": "Medium",
        "Other": "Low"
    }

    return severity_map.get(crime_category, "Medium")
def get_fir_status(severity):
    if severity == "Critical":
        return "Yes"

    elif severity == "High":
        return random.choices(
            ["Yes", "No"],
            weights=[95, 5]
        )[0]

    elif severity == "Medium":
        return random.choices(
            ["Yes", "No"],
            weights=[75, 25]
        )[0]

    else:
        return random.choices(
            ["Yes", "No"],
            weights=[40, 60]
        )[0]
def get_response_time(severity):
    if severity == "Critical":
        return random.randint(5, 15)

    elif severity == "High":
        return random.randint(10, 30)

    elif severity == "Medium":
        return random.randint(20, 60)

    else:
        return random.randint(30, 120)
def get_cctv_availability(crime_type):
    high_cctv = {
        "Vehicle Theft",
        "Chain Snatching",
        "Mobile Theft",
        "Robbery",
        "Burglary",
        "ATM Fraud"
    }

    low_cctv = {
        "Cyber Fraud",
        "Domestic Violence",
        "Human Trafficking",
        "Missing Person"
    }

    if crime_type in high_cctv:
        return random.choices(
            ["Yes", "No"],
            weights=[80, 20]
        )[0]

    elif crime_type in low_cctv:
        return random.choices(
            ["Yes", "No"],
            weights=[20, 80]
        )[0]

    else:
        return random.choices(
            ["Yes", "No"],
            weights=[50, 50]
        )[0]
def get_time_slot(crime_type):

    night = {
        "Burglary",
        "Vehicle Theft",
        "Robbery",
        "Arson"
    }

    evening = {
        "Chain Snatching",
        "Mobile Theft",
        "Assault"
    }

    daytime = {
        "Cyber Fraud",
        "Cheque Fraud",
        "ATM Fraud",
        "Extortion"
    }

    if crime_type in night:
        return random.choice(["Night", "Late Night"])

    elif crime_type in evening:
        return random.choice(["Evening", "Night"])

    elif crime_type in daytime:
        return random.choice(["Morning", "Afternoon"])

    return random.choice([
        "Morning",
        "Afternoon",
        "Evening",
        "Night"
    ])
def get_random_police_station(police_df, district_id):

    stations = police_df[
        police_df["district_id"] == district_id
    ]

    # Keep only stations with valid coordinates
    stations = stations[
        (stations["latitude"] != 0) &
        (stations["longitude"] != 0)
    ]

    if stations.empty:
        stations = police_df[
            (police_df["latitude"] != 0) &
            (police_df["longitude"] != 0)
        ]

    station = stations.sample(1).iloc[0]

    return {
        "station_name": station["police_station_name"],
        "latitude": float(station["latitude"]),
        "longitude": float(station["longitude"]),
    }