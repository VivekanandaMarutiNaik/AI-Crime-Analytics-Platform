from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from backend.services.ai_analytics import get_ai_answer
from backend.services.groq_ai import (
    extract_query_details,
    translate_to_kannada,
)
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


class AIQuery(BaseModel):
    query: str
    language: str = "en"

@router.post("/query")
async def query_ai(data: AIQuery):

    query_text = data.query

    query_info = extract_query_details(query_text)

    print("AI Parsed:", query_info)

    intent = query_info["intent"]

    answer = get_ai_answer(
        query=query_text,
        intent=intent,
        filters=query_info,
    )

    detected_language = query_info.get("language", "English").lower()

    if answer and (
            data.language.lower() == "kn"
            or detected_language == "kannada"
        ):
            answer = translate_to_kannada(answer)

    if answer:
        return {
            "status": "success",
            "original_text": data.query,
            "intent": intent,
            "answer": answer,
        }

    return {
        "status": "failed",
        "original_text": data.query,
        "intent": intent,
    }