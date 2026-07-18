import os
import re

import requests

from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

from pathlib import Path
from backend.services.query_parser import parse_query
from backend.services.ai_analytics import get_ai_answer
from backend.services.response_translator import translate_response

BASE_DIR = Path(__file__).resolve().parents[2]

CRIME_DATA = pd.read_csv(
    BASE_DIR / "datasets" / "raw" / "crime_cases.csv"
)

CCTV_RECOMMENDATIONS = pd.read_csv(
    BASE_DIR / "datasets" / "processed" / "cctv_installation_recommendations.csv"
)

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

router = APIRouter(prefix="/api/ai", tags=["AI"])

CATALYST_TOKEN = os.getenv("CATALYST_ACCESS_TOKEN")
TRANSLATE_URL = os.getenv("CATALYST_TRANSLATE_URL")
CATALYST_ORG_ID = os.getenv("CATALYST_ORG_ID")


class AIQuery(BaseModel):
    query: str
    language: str = "en"

@router.post("/query")
async def query_ai(data: AIQuery):
    print(data.language)
    headers = {
        "Authorization": f"Zoho-oauthtoken {CATALYST_TOKEN}",
        "CATALYST-ORG": CATALYST_ORG_ID,
        "Content-Type": "application/json",
    }

    payload = {
        "text": data.query,
        "src_lang": "kn",
        "tgt_lang": "en"
    }

    response = requests.post(
        TRANSLATE_URL,
        headers=headers,
        json=payload
    )

    translated = response.json()

    # Parse the original Kannada query
    intent = parse_query(data.query)

    answer = get_ai_answer(data.query, intent)

    if answer and data.language == "kn":
        answer = translate_response(answer)

    if answer:
        return {
            "status": "success",
            "original_text": data.query,
            "translated_text": translated.get("translated_text"),
            "intent": intent,
            "answer": answer,
        }
    
    
    return {
        "status": translated.get("status"),
        "original_text": data.query,
        "translated_text": translated.get("translated_text"),
        "intent": intent
    }