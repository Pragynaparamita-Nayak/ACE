from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import traceback

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("GROQ KEY FOUND:", api_key is not None)

try:
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3,
        api_key=api_key
    )
    print("Groq initialized successfully")

except Exception as e:
    print("===== REAL LLM ERROR =====")
    traceback.print_exc()
    raise