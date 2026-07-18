from difflib import get_close_matches

# Karnataka Districts (Kannada + English aliases)

DISTRICTS = {
    # Kannada
    "ಬೆಂಗಳೂರು": "Bengaluru Urban",
    "ಮೈಸೂರು": "Mysuru",
    "ಮೈಸೂರಿನಲ್ಲಿ": "Mysuru",
    "ಧಾರವಾಡ": "Dharwad",
    "ಹುಬ್ಬಳ್ಳಿ": "Dharwad",
    "ಬೆಳಗಾವಿ": "Belagavi",
    "ವಿಜಯಪುರ": "Vijayapura",
    "ಕಲಬುರಗಿ": "Kalaburagi",
    "ಶಿವಮೊಗ್ಗ": "Shivamogga",
    "ದಾವಣಗೆರೆ": "Davanagere",
    "ಮಂಗಳೂರು": "Dakshina Kannada",
    "ಉಡುಪಿ": "Udupi",
    "ಕೊಪ್ಪಳ": "Koppal",
    "ಹಾಸನ": "Hassan",
    "ಮಂಡ್ಯ": "Mandya",
    "ಬಳ್ಳಾರಿ": "Ballari",
    "ರಾಯಚೂರು": "Raichur",
    "ಕೊಡಗು": "Kodagu",
    "ಚಿಕ್ಕಮಗಳೂರು": "Chikkamagaluru",
    "ತುಮಕೂರು": "Tumakuru",

    # English + aliases
    "bagalkote": "Bagalkote",

    "ballari": "Ballari",
    "bellary": "Ballari",

    "belagavi": "Belagavi",
    "belgaum": "Belagavi",
    "belgam": "Belagavi",

    "bengaluru south": "Bengaluru South",
    "bangalore south": "Bengaluru South",

    "bengaluru rural": "Bengaluru Rural",
    "bangalore rural": "Bengaluru Rural",

    "bengaluru urban": "Bengaluru Urban",
    "bangalore urban": "Bengaluru Urban",

    "bengaluru": "Bengaluru Urban",
    "bangalore": "Bengaluru Urban",
    "blr": "Bengaluru Urban",
    "bang": "Bengaluru Urban",
    "bidar": "Bidar",

    "chamarajanagar": "Chamarajanagar",

    "chikkaballapura": "Chikkaballapura",
    "chikkaballapur": "Chikkaballapura",

    "chikkamagaluru": "Chikkamagaluru",
    "chikmagalur": "Chikkamagaluru",

    "chitradurga": "Chitradurga",

    "dakshina kannada": "Dakshina Kannada",
    "mangalore": "Dakshina Kannada",

    "davanagere": "Davanagere",
    "davangere": "Davanagere",

    "dharwad": "Dharwad",
    "hubli": "Dharwad",
    "hubballi": "Dharwad",

    "gadag": "Gadag",

    "hassan": "Hassan",

    "haveri": "Haveri",

    "kalaburagi": "Kalaburagi",
    "gulbarga": "Kalaburagi",
    "kalburgi": "Kalaburagi",

    "kodagu": "Kodagu",
    "coorg": "Kodagu",

    "kolar": "Kolar",

    "koppal": "Koppal",

    "mandya": "Mandya",

    "mysuru": "Mysuru",
    "mysore": "Mysuru",
    "mys": "Mysuru",

    "raichur": "Raichur",

    "shivamogga": "Shivamogga",
    "shimoga": "Shivamogga",

    "tumakuru": "Tumakuru",
    "tumkur": "Tumakuru",

    "udupi": "Udupi",

    "uttara kannada": "Uttara Kannada",
    "karwar": "Uttara Kannada",

    "vijayapura": "Vijayapura",
    "bijapur": "Vijayapura",

    "yadgir": "Yadgir",
}

# Crime Types

CRIMES = {
    # Kannada
    "ಕಳ್ಳತನ": "Theft",
    "ದರೋಡೆ": "Robbery",
    "ಸೈಬರ್ ಅಪರಾಧ": "Cyber Crime",
    "ಕೊಲೆ": "Murder",
    "ಅಪಹರಣ": "Kidnapping",
    "ವಂಚನೆ": "Fraud",
    "ಅಗ್ನಿ": "Fire Accident",
    "ಮಹಿಳಾ": "Women Crime",
    "ಡ್ರಗ್ಸ್": "Drug Offence",

    # English
    "theft": "Theft",
    "stealing": "Theft",

    "robbery": "Robbery",
    "rob": "Robbery",

    "cyber crime": "Cyber Crime",
    "cyber": "Cyber Crime",
    "online fraud": "Cyber Crime",

    "murder": "Murder",
    "homicide": "Murder",

    "kidnapping": "Kidnapping",
    "kidnap": "Kidnapping",
    "abduction": "Kidnapping",

    "fraud": "Fraud",
    "cheating": "Fraud",
    "scam": "Fraud",

    "fire": "Fire Accident",

    "women crime": "Women Crime",
    "women": "Women Crime",
    "rape": "Women Crime",
    "harassment": "Women Crime",

    "drug": "Drug Offence",
    "drugs": "Drug Offence",
    "narcotics": "Drug Offence",
}


def parse_query(text: str):

    text = text.lower()

    result = {
        "district": None,
        "crime_type": None,
        "intent": None
    }

    # -------------------------------------------------
    # District Detection
    # -------------------------------------------------

    # 1. Exact / Alias Match (longest key first)
    for key in sorted(DISTRICTS.keys(), key=len, reverse=True):

        if key in text:
            result["district"] = DISTRICTS[key]
            break


    # 2. Whole-word Match
    if result["district"] is None:

        words = text.split()

        for word in words:

            if word in DISTRICTS:
                result["district"] = DISTRICTS[word]
                break


    # 3. Fuzzy Match
    if result["district"] is None:

        match = get_close_matches(
            text,
            DISTRICTS.keys(),
            n=1,
            cutoff=0.75,
        )

        if match:
            result["district"] = DISTRICTS[match[0]]

    # Fuzzy matching
    if result["district"] is None:
        match = get_close_matches(
            text,
            DISTRICTS.keys(),
            n=1,
            cutoff=0.75
        )

        if match:
            result["district"] = DISTRICTS[match[0]]

    # Crime Detection
    for key, crime in CRIMES.items():
        if key in text:
            result["crime_type"] = crime
            break

    # Intent Detection

    # Top list intent
    if "top" in text:
        result["intent"] = "top"

    # Highest intent
    elif "highest" in text or "most" in text:
        result["intent"] = "highest"

    # Safest intent
    elif "safest" in text or "lowest" in text or "least" in text:
        result["intent"] = "safest"

    elif any(word in text for word in [
        "lowest", "least", "minimum"
    ]):
        result["intent"] = "lowest"

    elif any(word in text for word in [
        "safe", "safest"
    ]):
        result["intent"] = "safest"

    elif any(word in text for word in [
        "recent", "latest", "today", "today's"
    ]):
        result["intent"] = "recent"

    return result