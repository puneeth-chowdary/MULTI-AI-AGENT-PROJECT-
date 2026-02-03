import os
from dotenv import load_dotenv

ENV_PATH = "/Users/reddeppakollu/Multi-AI agent/.env"

print("DEBUG → Trying to load .env from:", ENV_PATH)
print("DEBUG → File exists:", os.path.exists(ENV_PATH))

load_dotenv(ENV_PATH)

print("DEBUG → GROQ_API_KEY after load:", repr(os.getenv("GROQ_API_KEY")))

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
print("DEBUG → GROQ_API_KEY:", repr(settings.GROQ_API_KEY))
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
logger=get_logger(__name__)
app=FastAPI(title="Multi AI Agent API",version="0.1.0")
class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search:bool
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "Multi AI Agent API",
        "version": "0.1.0"
    }
@app.post("/")
def chat_endpoint(request:RequestState):
    logger.info(f"Received request for model: {request.model_name}")
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.error(f"Model {request.model_name} is not allowed.")
        raise HTTPException(status_code=400,detail=f"Model {request.model_name} is not supported.")
    try:
        response=get_response_from_ai_agents(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        logger.info("Response generated successfully.")
        return {"response":response}
    except Exception as e:
        logger.error(f"Error while generating response: {e}")
        raise HTTPException(status_code=500,detail=str(CustomException("Failed to get response from AI agents",e)))