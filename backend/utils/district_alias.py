import re

DISTRICT_ALIASES = {
    "bangalore": "Bengaluru Urban",
    "bengaluru": "Bengaluru Urban",
    "bangalore urban": "Bengaluru Urban",
    "blr": "Bengaluru Urban",

    "tumkur": "Tumakuru",
    "tumakuru": "Tumakuru",

    "mysore": "Mysuru",
    "mysuru": "Mysuru",

    "bellary": "Ballari",
    "ballari": "Ballari",

    "gulbarga": "Kalaburagi",
    "kalaburagi": "Kalaburagi",

    "bijapur": "Vijayapura",
    "vijayapura": "Vijayapura",

    "mangalore": "Dakshina Kannada",
    "mangaluru": "Dakshina Kannada",

    "chikmagalur": "Chikkamagaluru",
    "chikkamagaluru": "Chikkamagaluru",

    "shimoga": "Shivamogga",
    "shivamogga": "Shivamogga",

    "hubli": "Dharwad",
    "hubballi": "Dharwad",
}


def normalize_district(name: str | None):
    if not name:
        return None

    key = re.sub(r"\s+", " ", name.strip().lower())

    return DISTRICT_ALIASES.get(key, name.strip())