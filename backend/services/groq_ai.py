import os
import json
from openai import OpenAI
from dotenv import load_dotenv



load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def extract_query_details(query: str):
    prompt = f"""
You are an AI assistant for a Karnataka Crime Analytics Platform.

Understand the user's question in English or Kannada.

Return ONLY valid JSON.

Schema:
{{
  "intent": "",
  "district": "",
  "district2": "",
  "crime_type": "",
  "year": null,
  "language": ""
}}

Possible intents:

crime_summary
crime_trend
crime_analysis
district_comparison
cctv_recommendation
highest_crime
safest_district
risk_prediction
crime_type
unknown

Examples:

User: Crime summary of Mysuru
Intent: crime_summary

User: Crime trend in Bengaluru
Intent: crime_trend

User: Analyze crime in Mysuru
Intent: crime_analysis

User: Why is crime high in Mysuru?
Intent: crime_analysis

User: ಮೈಸೂರಿನ ಅಪರಾಧವನ್ನು ವಿಶ್ಲೇಷಿಸಿ
Intent: crime_analysis

User: Compare Mysuru and Bengaluru
Intent: district_comparison

User: Compare Hassan with Mysuru
Intent: district_comparison

User: ಮೈಸೂರು ಮತ್ತು ಬೆಂಗಳೂರು ಹೋಲಿಸಿ
Intent: district_comparison

User: Predict crime in Mysuru
Intent: risk_prediction

User: Will crime increase in Bengaluru?
Intent: risk_prediction

User: What is the future crime risk in Hassan?
Intent: risk_prediction

User: ಮೈಸೂರಿನಲ್ಲಿ ಅಪರಾಧದ ಅಪಾಯವನ್ನು ಊಹಿಸಿ
Intent: risk_prediction

User: ಬೆಂಗಳೂರಿನಲ್ಲಿ ಅಪರಾಧ ಹೆಚ್ಚಾಗುತ್ತದೆಯೇ?
Intent: risk_prediction

User Query:
{query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    content = response.choices[0].message.content.strip()

    print("\n========== GROQ RESPONSE ==========")
    print(content)
    print("===================================\n")

    # Remove markdown code fences if present
    if content.startswith("```"):
        lines = content.splitlines()

        # Remove opening ``` or ```json
        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        # Remove closing ```
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    return json.loads(content)

def translate_to_kannada(text: str):

    prompt = f"""
Translate the following crime analytics response into professional Kannada.

Rules:
- Keep all numbers exactly the same.
- Keep emojis and formatting.
- Keep line breaks.
- Use official police/government terminology.
- Translate crime names naturally.
- Do not transliterate unless necessary.
- Return only the translated response.

{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content.strip()

def generate_crime_analysis(stats: str):

    prompt = f"""
You are an expert Crime Data Analyst.

Based on the statistics below, write a concise analysis.

Rules:
- Write 6–8 professional sentences.
- Base every observation only on the provided statistics.
- Mention:
  - Total cases
  - Closure rate
  - Most common crime
  - CCTV coverage
  - Hotspot score
  - Police response time
- Explain what these numbers imply.
- Give 2 practical recommendations based only on the provided statistics.
- Do NOT recommend specific percentages, target values, or deadlines unless they are present in the data.
- If CCTV coverage is low, recommend increasing CCTV in hotspot areas.
- If response time is high, recommend improving emergency response efficiency.
- If closure rate is low, recommend strengthening investigations.
- Do not invent facts or numbers.
- Do not use vague suggestions.
- Keep the language suitable for a police dashboard.
- Return only the analysis.

Crime Statistics:

{stats}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content.strip()

def generate_district_comparison(district1, district2, summary1, summary2):
    prompt = f"""
You are an expert Crime Data Analyst.

Compare these two districts.

{district1} Summary:
{summary1}

{district2} Summary:
{summary2}

Rules:
- Write 6-8 professional sentences.
- Compare:
  • Total cases
  • Closure rate
  • CCTV coverage
  • Hotspot score
  • Response time
  • Most common crime
- Clearly mention which district performs better for each metric where appropriate.
- Do not invent numbers.
- Base every statement only on the supplied summaries.
- End with 2 practical recommendations.
- Return only the comparison.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()

def generate_risk_assessment(stats):
    prompt = f"""
You are an expert Crime Risk Analyst.

Analyze the following crime risk statistics.

{stats}

Rules:
- Write 5-7 professional sentences.
- Explain what the risk score indicates.
- Explain the impact of hotspot score.
- Explain whether CCTV coverage appears sufficient.
- Mention crime frequency.
- Do not invent any numbers.
- Base every statement only on the supplied statistics.
Write in this format:

Assessment:
<5-7 professional sentences>

Recommendations:
1. <recommendation>
2. <recommendation>

Do not invent numbers.
Base every statement only on the supplied statistics.
Return only the assessment and recommendations.

"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()