from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os

# =============================
# CONFIGURATION
# =============================

API_KEY = os.getenv("GEMINI_API_KEY")  # safer than hardcoding
MODEL_NAME = "gemini-flash-lite-latest"

PROFILE_PATH = r"Data_Models\Manju\Resume.txt"

# =============================
# LOAD JOHN CONTEXT
# =============================

try:
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        resume_context = f.read()
except Exception as e:
    resume_context = ""
    print("Could not load profile:", e)

# =============================
# GEMINI CLIENT
# =============================

client = genai.Client(api_key=API_KEY)

# =============================
# FASTAPI SERVER
# =============================

app = FastAPI()

# Fix browser CORS issue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# ROOT ENDPOINT
# =============================

@app.get("/")
def home():
    return {"message": "Manju's AI assistant is running"}

# =============================
# Health check on render ENDPOINT
# =============================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "manju-ai-assistant",
        "version": "1.0"
    }
# =============================
# AI QUESTION ENDPOINT
# =============================

@app.get("/ask")
def ask(question: str):

    prompt = f"""
You are Manju's professional AI assistant.

Use the following information about Manju to answer questions about his experience.

--------------------------------
{resume_context}
--------------------------------

Answer the following question professionally:

{question}
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return {"answer": response.text}

    except Exception as e:

        return {"error": str(e)}