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
def get_random_police_station(police_stations):
    station = police_stations.sample(1).iloc[0]

    return {
        "station_id": int(station["station_id"]),
        "station_name": station["station_name"]
    }