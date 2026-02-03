import os

class Settings:
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY: str | None = os.getenv("TAVILY_API_KEY")
    ALLOWED_MODEL_NAMES = [
        "llama3-70b-8192",
        "llama-3.1-8b-instant"
    ]

settings = Settings()
