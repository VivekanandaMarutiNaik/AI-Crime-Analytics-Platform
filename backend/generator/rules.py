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