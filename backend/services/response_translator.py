TRANSLATIONS = {
    "Theft Cases in": "ಕಳ್ಳತನ ಪ್ರಕರಣಗಳು",
    "Theft Cases Across Karnataka": "ಕರ್ನಾಟಕದಾದ್ಯಂತ ಕಳ್ಳತನ ಪ್ರಕರಣಗಳು",
    "Total Cases": "ಒಟ್ಟು ಪ್ರಕರಣಗಳು",
    "Breakdown": "ವಿಭಾಗವಾರು",
    "District-wise": "ಜಿಲ್ಲಾವಾರು",

    "Vehicle Theft": "ವಾಹನ ಕಳ್ಳತನ",
    "Shop Theft": "ಅಂಗಡಿ ಕಳ್ಳತನ",
    "Crop Theft": "ಬೆಳೆ ಕಳ್ಳತನ",
    "Cattle Theft": "ಜಾನುವಾರು ಕಳ್ಳತನ",
}


def translate_response(text: str):
    translated = text

    for english, kannada in TRANSLATIONS.items():
        translated = translated.replace(english, kannada)

    return translated