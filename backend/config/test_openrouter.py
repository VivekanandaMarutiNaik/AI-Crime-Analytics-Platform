import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

print("Length:", len(api_key))
print("Starts with:", api_key.startswith("sk-or-v1-"))
print("Prefix count:", api_key.count("sk-or-v1-"))
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model="openai/gpt-4.1-nano",
    messages=[
        {"role": "user", "content": "Say hello"}
    ],
)

print(response.choices[0].message.content)